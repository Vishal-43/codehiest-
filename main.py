from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from database import engine, SessionLocal, Base
from models import Project, Task

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@app.get("/projects", response_class=HTMLResponse)
def list_projects(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": projects}
    )


@app.get("/projects/new", response_class=HTMLResponse)
def new_project_page(request: Request):
    return templates.TemplateResponse("new_project.html", {"request": request})


@app.post("/projects/new")
def create_project(
    name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    project = Project(name=name, description=description)
    db.add(project)
    db.commit()
    return RedirectResponse("/projects", status_code=303)


@app.get("/projects/{project_id}", response_class=HTMLResponse)
def project_detail(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return RedirectResponse("/projects", status_code=303)

    completed = sum(task.is_complete for task in project.tasks)
    total = len(project.tasks)
    progress = int((completed / total) * 100) if total else 0

    return templates.TemplateResponse(
        "project_detail.html",
        {
            "request": request,
            "project": project,
            "progress": progress
        }
    )


@app.post("/projects/{project_id}/tasks")
def add_task(
    project_id: int,
    title: str = Form(...),
    db: Session = Depends(get_db)
):
    task = Task(title=title, project_id=project_id)
    db.add(task)
    db.commit()
    return RedirectResponse(f"/projects/{project_id}", status_code=303)


@app.post("/tasks/{task_id}/complete")
def mark_complete(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.is_complete = True
        db.commit()
        return RedirectResponse(f"/projects/{task.project_id}", status_code=303)

    return RedirectResponse("/projects", status_code=303)
