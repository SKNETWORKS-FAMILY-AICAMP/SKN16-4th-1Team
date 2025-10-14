from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path

from .common import (
    store,
    get_current_user,
    DiaryCreate,
    DiaryOut,
    DiaryListOut,
    DiaryUpdate,
    now,
    next_id,
)


router = APIRouter(prefix="/api/diaries", tags=["diaries"])


@router.post("", response_model=DiaryOut)
def create_diary(payload: DiaryCreate, user=Depends(get_current_user)):
    diary_id = next_id("diary")
    diary = {
        "id": diary_id,
        "user_id": user["id"],
        "date": payload.date,
        "title": payload.title,
        "content": payload.content,
        "created_at": now(),
    }
    store["diaries"][diary_id] = diary
    store["diaries_by_user"].setdefault(user["id"], []).append(diary_id)
    return DiaryOut(**{k: diary[k] for k in ["id", "date", "title", "content", "created_at"]})


@router.get("", response_model=DiaryListOut)
def list_diaries(
    month: str = Query(..., description="YYYY-MM"),
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, le=50),
    user=Depends(get_current_user),
):
    items_ids = [
        d for d in store["diaries_by_user"].get(user["id"], [])
        if store["diaries"][d]["date"].startswith(month)
    ]
    offset = int(cursor) if cursor and cursor.isdigit() else 0
    page = items_ids[offset: offset + limit]
    next_cursor = str(offset + limit) if offset + limit < len(items_ids) else None
    items = [
        DiaryOut(**{k: store["diaries"][i][k] for k in ["id", "date", "title", "content", "created_at"]})
        for i in page
    ]
    return {"items": items, "next_cursor": next_cursor}


@router.get("/{id}", response_model=DiaryOut)
def get_diary(id: str = Path(...), user=Depends(get_current_user)):
    diary = store["diaries"].get(id)
    if not diary or diary["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Diary not found")
    return DiaryOut(**{k: diary[k] for k in ["id", "date", "title", "content", "created_at"]})


@router.put("/{id}", response_model=DiaryOut)
def update_diary(id: str, payload: DiaryUpdate, user=Depends(get_current_user)):
    diary = store["diaries"].get(id)
    if not diary or diary["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Diary not found")
    updates = payload.model_dump(exclude_none=True)
    diary.update(updates)
    return DiaryOut(**{k: diary[k] for k in ["id", "date", "title", "content", "created_at"]})


@router.delete("/{id}")
def delete_diary(id: str, user=Depends(get_current_user)):
    diary = store["diaries"].get(id)
    if not diary or diary["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Diary not found")
    store["diaries"].pop(id, None)
    ids = store["diaries_by_user"].get(user["id"], [])
    store["diaries_by_user"][user["id"]] = [x for x in ids if x != id]
    store["cartoons"].pop(id, None)
    return {"ok": True}
