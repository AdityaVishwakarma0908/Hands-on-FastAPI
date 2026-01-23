from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel): #schema
    title: str
    content: str

my_posts = [
    {"id": 1, "title": "the greate experience", "content": "Experiencing profound growth through creativity and technical innovation has defined my journey, blending discipline with a passion for meaningful impact."},
    {"id": 2, "title": "the elephant", "content": "Majestic and wise, the elephant symbolizes strength and memory, gracefully navigating the wilderness while fostering deep, enduring connections within its herd."},
    {"id": 3, "title": "indian developement", "content": "India’s digital infrastructure and sustainable initiatives drive rapid growth, empowering diverse communities through innovation, technology, and a resilient, future-ready economy."},
    {"id": 4, "title": "the greate man", "content": "A great man leads with integrity, inspiring others through selfless service and wisdom while leaving a lasting legacy of kindness."},
    {"id": 5, "title": "personality in organization", "content": "Personality shapes organizational culture, influencing how individuals collaborate, lead, and adapt to challenges, ultimately driving collective success and workplace harmony."}
]

def find_post(id):
    for post in my_posts:
        if(post["id"] == id):
            return post

def find_post_index(id):
    for j in range(len(my_posts)):
        if my_posts[j]["id"] == id:
            return j
    return -1

 
@app.get("/")
def root():
    return {"message": "Hay there !!! here is you app "} 

@app.get("/posts")
def get_post():
    return {"data": my_posts} 

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    dict_post = new_post.dict()
    dict_post["id"] = randrange(1,1000000)
    print(dict_post)
    my_posts.append(dict_post)
    
    return {"data": my_posts} 
# title, content

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post_data = find_post(id)
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post id: {id} is not founded")
    print(f"status of id >>> {id}")
    return {"data": post_data}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required id
    post_index = find_post_index(id)
    print(post_index)

    if post_index >=0 : 
        my_posts.pop(post_index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"the id: {id} is not founded! Please try again"
            )