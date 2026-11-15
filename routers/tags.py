from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connect import get_db
from db import crud
from dependencies import require_admin
import schemas

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/", response_model=list[schemas.TagOut])
def list_tags(db: Session = Depends(get_db)):
    return crud.get_all_tags(db)

@router.post("/", response_model=schemas.TagOut, status_code=201)
def create_tag(data: schemas.TagCreate, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return crud.create_tag(db, data.tag_name)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.put("/{tag_id}", response_model=schemas.TagOut)
def update_tag(tag_id: int, data: schemas.TagCreate, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return crud.update_tag(db, tag_id, data.tag_name)
    except (ValueError, LookupError) as e:
        raise HTTPException(404, str(e))

@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return {"message": crud.delete_tag(db, tag_id)}
    except LookupError as e:
        raise HTTPException(404, str(e))