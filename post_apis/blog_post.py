from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class Blog(BaseModel):
    title : str
    content : str
    tags : Optional[List[str]] = []
    published : bool = False

class ResponseBlog(Blog):
    id : int
    created_at : datetime

app = FastAPI(title="Blog Post", description="This is the api that is used to create a blog post", version='1.0.0')

post_db : Dict[int, Dict] = {}

@app.get('/')
def root_page():
    return {"message": "Welcome to the Homepage."}

@app.get('/blog_post')
def 

@app.post('/blog_post/upload')
def create_blog(blog : Blog):

    # if not blog.title or blog.content:
    #     raise HTTPException(status_code=400, detail="Title and the content are required")
    
    id = len(post_db) + 1
    response = ResponseBlog(id = id, title=blog.title, content=blog.content, tags=blog.tags, published=blog.published, created_at=datetime.utcnow())

    post_db.append(response)

    return {"message": "Post created", "post": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("blog_post:app", reload=True)