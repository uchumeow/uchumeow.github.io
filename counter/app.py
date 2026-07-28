import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

database_path = Path(os.getenv("DATABASE_PATH", "/data/visitors.db"))
database_path.parent.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(database_path) as database:
    database.execute(
        "CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER NOT NULL)"
    )
    database.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "ALLOWED_ORIGINS",
        "https://uchumeow.github.io,http://localhost:8000,http://127.0.0.1:8000",
    ).split(","),
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def current_count():
    with sqlite3.connect(database_path) as database:
        return database.execute(
            "SELECT count FROM stats WHERE id = 1"
        ).fetchone()[0]


@app.get("/api/count")
def get_count():
    return {"count": current_count()}


@app.post("/api/visit")
def add_visit():
    with sqlite3.connect(database_path) as database:
        database.execute("UPDATE stats SET count = count + 1 WHERE id = 1")
        count = database.execute(
            "SELECT count FROM stats WHERE id = 1"
        ).fetchone()[0]
    return {"count": count}


@app.get("/health")
def health():
    return {"status": "ok"}
