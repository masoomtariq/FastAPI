from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

# Base blog model for input data
class Blog(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []
    published: bool = False

# Model that includes creation time
class CreatedBlog(Blog):
    created_at: datetime

# Model that includes both creation and edit times
class EditedBlog(CreatedBlog):
    edited_at: datetime

# Create the FastAPI app instance with metadata
app = FastAPI(
    title="Blog Post",
    description="This is the API that is used to create, retrieve, update, and delete blog posts.",
    version='1.0.0'
)

# In-memory 'database' to store blog posts
# Keys are integer IDs, values are blog post models
post_db: Dict[int, CreatedBlog | EditedBlog] = {}

# Utility function to validate blog post existence by ID
def validate_id(id: int):
    if id not in post_db:
        raise HTTPException(status_code=404, detail="Invalid ID.")

# Root/homepage endpoint
@app.get('/')
def root_page():
    return {"message": "Welcome to the Homepage."}

# GET blog post by ID
@app.get('/blog_post/id/{id}')
def search_by_id(id: int):
    validate_id(id)
    return {
        "message": f"The blog post was found at ID '{id}'",
        "blog_post": post_db[id]
    }

# GET blog post(s) by title using query parameter
@app.get('/blog_post/search_by_title')
def search_by_title(title: str):
    # Filter posts that match the given title
    results = {id: post for id, post in post_db.items() if post.title == title}

    if not results:
        raise HTTPException(status_code=404, detail=f"No blog post found with the title '{title}'")

    return {
        "message": f"Blog post(s) found with the title '{title}'",
        "results": results
    }

# POST endpoint to upload/create a new blog post
@app.post('/blog_post/upload')
def create_blog(blog: Blog):
    # Generate a new ID
    id = len(post_db) + 1

    # Add creation timestamp
    response = CreatedBlog(
        title=blog.title,
        content=blog.content,
        tags=blog.tags,
        published=blog.published,
        created_at=datetime.utcnow()
    )

    post_db[id] = response

    return {"message": "Post created successfully", "post": response}

# PUT endpoint to edit an existing blog post by ID
@app.put('/blog_post/edit')
def edit_blog(id: int, post: Blog):
    validate_id(id)
    created_time = post_db[id].created_at

    # Create edited post with original creation time and new edited time
    edited_post = EditedBlog(
        title=post.title,
        content=post.content,
        tags=post.tags,
        published=post.published,
        created_at=created_time,
        edited_at=datetime.utcnow()
    )

    post_db[id] = edited_post

    return {"message": "Post updated successfully", "post": edited_post}

# DELETE endpoint to remove a blog post by ID
@app.delete('/blog_post/delete')
def delete_post(id: int):
    validate_id(id)
    del post_db[id]
    return {"message": f"The blog post with ID '{id}' has been deleted."}

# Run the application using uvicorn (only if this file is executed directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("blog_post:app", reload=True)