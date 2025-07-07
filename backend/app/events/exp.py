#
# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import SessionLocal, engine
# import models
# import schemas
# from pydantic import BaseModel
# from typing import List, Optional
#
# class EventImageBase(BaseModel):
#     image_url: str
#
# class EventImageCreate(EventImageBase):
#     pass
#
# class EventImage(EventImageBase):
#     id: int
#     event_id: int
#
#     class Config:
#         orm_mode = True
#
# class EventBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float = 0.0
#     venue: str
#     total_tickets: int = 5
#
# class EventCreate(EventBase):
#     pass
#
# class Event(EventBase):
#     id: int
#     images: List[EventImage] = []
#
#     class Config:
#         orm_mode = True
# models.Base.metadata.create_all(bind=engine)
#
# app = FastAPI()
#
# # Dependency для отримання сесії бази даних
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# @app.post("/events/", response_model=schemas.Event)
# def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
#     db_event = models.Event(**event.dict())
#     db.add(db_event)
#     db.commit()
#     db.refresh(db_event)
#     return db_event
#
# @app.get("/events/{event_id}", response_model=schemas.Event)
# def read_event(event_id: int, db: Session = Depends(get_db)):
#     db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
#     if db_event is None:
#         raise HTTPException(status_code=404, detail="Event not found")
#     return db_event
#
# @app.put("/events/{event_id}", response_model=schemas.Event)
# def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
#     db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
#     if db_event is None:
#         raise HTTPException(status_code=404, detail="Event not found")
#     for key, value in event.dict().items():
#         setattr(db_event, key, value)
#     db.commit()
#     db.refresh(db_event)
#     return db_event
#
# @app.delete("/events/{event_id}", response_model=schemas.Event)
# def delete_event(event_id: int, db: Session = Depends(get_db)):
#     db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
#     if db_event is None:
#         raise HTTPException(status_code=404, detail="Event not found")
#     db.delete(db_event)
#     db.commit()
#     return db_event
#
# @app.post("/events/{event_id}/images/", response_model=schemas.EventImage)
# def create_event_image(event_id:
#
#
# class EventCreate(EventBase):
#     images: List[EventImageCreate] = []
#
#
# @app.post("/events/", response_model=schemas.Event)
# def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
#     db_event = models.Event(**event.dict(exclude={"images"}))  # Виключаємо зображення з даних події
#     db.add(db_event)
#     db.commit()
#     db.refresh(db_event)
#
#     # Додаємо зображення, якщо вони є
#     if event.images:
#         for image in event.images:
#             db_image = models.EventImage(event_id=db_event.id, **image.dict())
#             db.add(db_image)
#         db.commit()  # Зберігаємо зображення в базі даних
#
#     return db_event