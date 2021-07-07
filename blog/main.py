from blog import hashing
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import delete, true
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED


from . import  models, schemas, hashing
from .database import SessionLocal, engine
import blog
app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED, tags=['blog'])
def create(request: schemas.Blog, db: Session= Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', status_code=200, response_model= List[schemas.ShowBlog], tags=['blog'])
def all(db: Session= Depends(get_db)):
    blogs= db.query(models.Blog).all()

    return blogs


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def destroy(id: int, db: Session=Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='this id not found')
    
    blog.delete(synchronize_session= False)  
    db.commit()
    return {'message':'Done'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update(id: int, request: schemas.Blog, db: Session=Depends(get_db)):
    # blog= db.query(models.Blog).filter(models.Blog.id == id).update({
    #     'title': request.title,
    #     'body': request.body
    # })
    blog= db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='this id not found')
    else:
        blog.update(request)
    db.commit()
    return blog

@app.get('/blog/{id}', status_code=200, response_model= schemas.ShowBlog, tags=['blog'])
def show(id: int, response: Response, db: Session= Depends(get_db)):
    blog= db.query(models.Blog).filter(
        models.Blog.id == id
    ).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {
        #     'message': f"id {id} not found"
        # }
    return blog




######### User


@app.post('/user', response_model=schemas.ShowUser, tags=['user'])
def create_user(request: schemas.User, db: Session= Depends(get_db)):
    hashedPassword = hashing.Hash.bcript(request.password)
    new_user= models.User(
        name= request.name,
        email= request.email,
        password= hashedPassword

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['user'])
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.id == id
    ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail='this user not found')
    return user