from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import session
from ..import database,schemas,models
from ..database import get_db
router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
@router.get("/")
def get_posts(db:session =Depends(get_db)):
    posts=db.query(models.Post).all()
    #cursor.execute("SELECT * FROM posts")
    #posts=cursor.fetchall()
    return{"posts":posts}
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.CreatePost)
def create_post(post:schemas.Post,db:session = Depends(get_db)):
     new_post=models.Post(title=post.title,content=post.content)
     db.add(new_post)
     db.commit()
     db.refresh(new_post)
     return new_post
@router.get("/{id}")
def get_post(id:int,db:session = Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    #post=find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    #Retrieve an individual post
    #cursor.execute("""SELECT * FROM posts WHERE id=%s;""",(str(id)))
    #new_post=cursor.fetchone()
    return{"Post":post}
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int,db:session=Depends(get_db)):
    #Call dele_post method
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *;""",(str(id),))
    #deleted_post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with{id} not found")
    #cursor.execute("""DELETE FROM posts WHERE id={id}""")
    post.delete()
    db.commit()
    response=status.HTTP_204_NO_CONTENT
    return response
@router.put("/{id}",response_model=schemas.PostUpdate)
def update_post(id:int,new_post:schemas.Post,db:session=Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *;""",
       #            (new_post.title,new_post.content,new_post.published,str(id)))
    #updated_post=cursor.fetchone() 
    #conn.commit()
    new=new_post.dict()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with{id} not found")
    post_query.update(new)
    db.commit()
    return post_query.first()