from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

# З'єднання з базою даних
models.Base.metadata.create_all(bind=database.engine)
db = Session()

# Операція створення нового контакту
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Операція отримання списку всіх контактів
@app.get("/contacts/", response_model=List[schemas.Contact])
def get_contacts():
    return db.query(models.Contact).all()

# Операція отримання контакту за ідентифікатором
@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def get_contact(contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

# Операція оновлення існуючого контакту
@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        for attr, value in contact.dict().items():
            setattr(db_contact, attr, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    raise HTTPException(status_code=404, detail="Contact not found")

# Операція видалення контакту
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return {"message": "Contact deleted successfully"}
    raise HTTPException(status_code=404, detail="Contact not found")

