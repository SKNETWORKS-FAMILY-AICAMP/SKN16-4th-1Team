from fastapi import APIRouter, Depends, HTTPException

from .common import (
    store,
    get_current_user,
    TaskOut,
    maybe_complete_task,
)


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: str, user=Depends(get_current_user)):
    task = store["tasks"].get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.get("diary_id"):
        diary = store["diaries"].get(task["diary_id"]) or {}
        if diary.get("user_id") != user["id"]:
            raise HTTPException(status_code=404, detail="Task not found")
    maybe_complete_task(task)
    return task
