from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel): #schema
    title: str
    content: str
    publish: bool = True

try:
    conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="pass@123", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connected successfully !!")
except Exception as error:
    print("database connection fails !!")
    print("Error:",error)
 
@app.get("/")
def root():
    return {"message": "Hay there !!! here is you app "} 

@app.get("/posts") # getting all the ids
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.get("/posts/{id}") # get a single post
def get_post(id: int, response: Response):
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    post = cursor.fetchone()
    if(post==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id: {id} is not found !!")
    return {"data":post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    dict_post = new_post.dict()
    try:
        cursor.execute(f"""INSERT INTO posts (title, content, publish) 
                       VALUES (%s, %s, %s) RETURNING *""", (dict_post["title"], dict_post["content"], dict_post["publish"]))
        conn.commit()
        created_post = cursor.fetchone()
        return {"data": created_post}
    except Exception as error:
        print("Error:",error)


@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    cursor.execute(f"DELETE FROM posts WHERE id = {id} RETURNING *")
    conn.commit()
    deleting_post = cursor.fetchone()
    if(delete_post==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id: {id} is not avilable")

    return {"data": deleting_post}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, publish = %s 
                      WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.publish, id))
    
    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    conn.commit()

    return {"data": updated_post}

