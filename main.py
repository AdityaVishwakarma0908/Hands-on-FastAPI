from fastapi import FastAPI
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
    else:
        return "!! POST NOT FOUNDED !!"

 
@app.get("/")
def root():
    return {"message": "Hay there !!! here is you app "} 

@app.get("/posts")
def get_post():
    return {"data": my_posts} 

@app.post("/posts")
def create_posts(new_post: Post):
    dict_post = new_post.dict()
    dict_post["id"] = randrange(1,1000000)
    print(dict_post)
    my_posts.append(dict_post)
    
    return {"data": my_posts} 
# title, content

@app.get("/posts/{id}")
def get_post(id: int):
    post_data = find_post(id)
    print(f"status of id >>> {id}")
    return {"data": post_data} 
