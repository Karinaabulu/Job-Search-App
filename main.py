from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
import shutil
import os
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import schemas
import services

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Job search app is running!"}

@app.post("/verify-nin", response_model=schemas.UserResponse)
def submit_nin(payload: schemas.NINSubmit, db: Session = Depends(get_db)):
    result = services.verify_nin(payload.nin)
    if result is None:
        raise HTTPException(status_code=400, detail="Invalid NIN")

    existing = db.query(models.User).filter(models.User.nin == payload.nin).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists for this NIN")

    new_user = models.User(
        nin=payload.nin,
        full_name=result["full_name"],
        date_of_birth=result["date_of_birth"]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

UPLOAD_DIR = "uploads"

@app.post("/upload-documents/{nin}")
def upload_documents(nin: str, passport: UploadFile = File(...), cv: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.nin == nin).first()
    if not user:
        raise HTTPException(status_code=404, detail="No profile found for this NIN")

    passport_path = os.path.join(UPLOAD_DIR, f"{nin}_passport_{passport.filename}")
    with open(passport_path, "wb") as buffer:
        shutil.copyfileobj(passport.file, buffer)

    cv_path = os.path.join(UPLOAD_DIR, f"{nin}_cv_{cv.filename}")
    with open(cv_path, "wb") as buffer:
        shutil.copyfileobj(cv.file, buffer)

    user.passport_photo_path = passport_path
    user.cv_path = cv_path
    db.commit()
    db.refresh(user)

    return {"message": "Documents uploaded successfully", "passport_path": passport_path, "cv_path": cv_path}