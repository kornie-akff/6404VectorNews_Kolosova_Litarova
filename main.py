from fastapi import FastAPI
from routers import auth, users, articles, tags, m2m

app = FastAPI(title="Новостной портал", version="1.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(tags.router)
app.include_router(m2m.router)

@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}