from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class Blog(BaseModel):
    title : str
    content : str
    tags : Optional[List[str]] = []
    published : bool = False

class CreatedBlog(Blog):
    created_at : datetime
    
class EditedBlog(CreatedBlog):
    edited_at : datetime

app = FastAPI(title="Blog Post", description="This is the api that is used to create a blog post", version='1.0.0')

post_db : Dict[int, Dict] = {}

def validate_id(id):
    if id not in post_db:
        raise HTTPException(status_code=404, detail="Invalid Id.")

@app.get('/')
def root_page():
    return {"message": "Welcome to the Homepage."}

@app.get('/blog_post/{id}')
def search_by_id(id: int):
    validate_id(id)
    
    return {"message": f"The blog_post has been found at the ID '{id}'", "Blog_post": post_db[id]}

@app.get('/blog_post/{title}')
def search_by_title(title: str):
    results = {id: post for id, post in post_db.items() if post.title == title}

    if not results:
        raise HTTPException(status_code=404, detail=f"No blog_post found on the Title '{title}'")
    
    return {"message": f"The Blog_posts found on the Title '{title}'.", "Results": results}

@app.post('/blog_post/upload')
def create_blog(blog : Blog):
    
    id = len(post_db) + 1
    response = CreatedBlog(title=blog.title,
                            content=blog.content,
                            tags=blog.tags,
                            published=blog.published,
                            created_at=datetime.utcnow())

    post_db[id] = response

    return {"message": "Post created", "post": response}

@app.put('/blog_post/edit')
def edit_blog(id: int, post: Blog):
    
    validate_id(id)
    created_time = post_db[id].created_at

    edited_post = EditedBlog(title=post.title,
                             content=post.content,
                             tags=post.tags,
                             published=post.published)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("blog_post:app", reload=True)