from fastapi import APIRouter, Depends, HTTPException

from .common import (
    store,
    get_current_user,
    GenerateRequest,
    CartoonOut,
    RerollRequest,
    new_task,
    maybe_complete_task,
)


router = APIRouter(tags=["cartoons"])


@router.post("/api/diaries/{id}/generate", status_code=202)
def generate_cartoon(id: str, payload: GenerateRequest, user=Depends(get_current_user)):
    diary = store["diaries"].get(id)
    if not diary or diary["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Diary not found")
    task = new_task("generate", diary_id=id)
    store["cartoons"][id] = {"status": "queued", "panels": [], "meta": {}}
    return {"task_id": task["id"], "status": "queued"}


@router.get("/api/cartoons/{diary_id}", response_model=CartoonOut)
def get_cartoon(diary_id: str, user=Depends(get_current_user)):
    diary = store["diaries"].get(diary_id)
    if not diary or diary["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Diary not found")
    cartoon = store["cartoons"].get(diary_id)
    if not cartoon:
        raise HTTPException(status_code=404, detail="Cartoon not found")
    for t in store["tasks"].values():
        if t.get("diary_id") == diary_id:
            maybe_complete_task(t)
    cartoon = store["cartoons"].get(diary_id) or cartoon
    return cartoon


@router.post("/api/cartoons/{diary_id}/reroll", status_code=202)
def reroll_cartoon(diary_id: str, payload: RerollRequest, user=Depends(get_current_user)):
    diary = store["diaries"].get(diary_id)
    if not diary or diary["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Diary not found")
    task = new_task("reroll", diary_id=diary_id)
    store["cartoons"][diary_id] = {"status": "queued", "panels": [], "meta": {}}
    return {"task_id": task["id"]}
