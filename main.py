from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import psycopg2
from contextlib import contextmanager

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="tracker_db",
            user="tracker_user",
            password="123",
            host="127.0.0.1"
        )
        yield conn
    except Exception:
        if conn is not None:
            conn.rollback()
        raise
    finally:
        if conn is not None:
            conn.close()

@app.get("/test")
def test():
    return {"Test is goooooood"}

@app.get("/check_users")
def check_users():
    try:
        with get_db_connection() as conn:
            with conn.cursor()  as cur:
                cur.execute("SELECT * FROM users")
                results = cur.fetchall()
                if len(results) == 0:
                    return {
                        "status": "empty",
                        "message": "Пользователей не найдено",
                        "users": []
                    }
                else:
                    return {
                        "status": "ok",
                        "count": len(results),
                        "users": results
                    }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось посмотреть юзеров: {e}")

@app.get("/check_tasks")
def check_tasks():
    try:
        with get_db_connection() as conn:
            with conn.cursor()  as cur:
                cur.execute("SELECT * FROM tasks")
                results = cur.fetchall()
                if len(results) == 0:
                    return {
                        "status": "empty",
                        "message": "Задач не найдено",
                        "tasks": []
                    }
                else:
                    return {
                        "status": "ok",
                        "count": len(results),
                        "tasks": results
                    }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось посмотреть задачи: {e}")

@app.get("/add_user")
def form_open_user():
    file_path = os.path.join(os.path.dirname(__file__), "templates/form_user.html")
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, media_type="text/html")

@app.post("/add_user/form_data")
def add_user(
    username: str = Form(),
    email: str = Form()
):
    try:
        with get_db_connection() as conn:
            with conn.cursor()  as cur:
                cur.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
                conn.commit()
                return {"Пользователь добавлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось создать пользователя: {e}")

@app.get("/add_task")
def form_open_task(request: Request):
    try:
        with get_db_connection() as conn:
            with conn.cursor()  as cur:
                cur.execute("SELECT id, username FROM users")
                results = cur.fetchall()
                return templates.TemplateResponse(request, "form_task.html", {"users": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить список юзеров: {e}")

@app.post("/add_task/form_data")
def add_task(
    title: str = Form(),
    description: str = Form(),
    is_completed: str | None = Form(None),
    user_id: int = Form()
):
    try:
        db_is_completed = True if is_completed == "true" else False
        with get_db_connection() as conn:
            with conn.cursor()  as cur:
                cur.execute("INSERT INTO tasks (title, description, is_completed, user_id) VALUES (%s, %s, %s, %s)", (title, description, db_is_completed, user_id))
                conn.commit()
                return {"Задача добавлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось создать задачу: {e}")

@app.get("/users/{user_id}/tasks")
def check_users_taksk(user_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor()  as cur:
                cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
                results = cur.fetchall()
                conn.commit()
                if len(results) == 0:
                    return {
                        "status": "empty",
                        "message": "Задач не найдено",
                        "tasks": []
                    }
                else:
                    return {
                        "status": "ok",
                        "count": len(results),
                        "tasks": results
                    }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось посмотреть задачи пользователя: {e}")

@app.get("/delete_task/{task_id}")
def delete_task(task_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor()  as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                conn.commit()
                return {"Задача удалена"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось удалить задачу: {e}")
