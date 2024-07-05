

from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,database,models,utils
from sqlalchemy.orm import session
router=APIRouter(
    prefix="/login",
    tags=["Login"]
)
@router.post("/")
def login(user_credentials:schemas.UserCredentials,db:session=Depends(database.get_db)):
    #Retrieve the user based on the email
    user=db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    #Hash the tried password
    #Compare it to the hased password stored in the database
    check=utils.verify(user_credentials.password,user.password)
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    return ("JWT Token generated")
    
    #Return a JWT token if the passwords match