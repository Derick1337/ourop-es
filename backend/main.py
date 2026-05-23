from __future__ import annotations

import os
import sqlite3
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = os.path.join(os.path.dirname(__file__), "ouropaes.db")

app = FastAPI(title="Ouropaes Campo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PontoBase(BaseModel):
    nome: str
    cnpj: Optional[str] = ""
    razao: Optional[str] = ""
    tipo: str = "prospect"
    prod: Optional[str] = ""
    forn: Optional[str] = ""
    preco: Optional[str] = ""
    equip: Optional[str] = ""
    dem: str = "Alta"
    cls: str = "A"
    obs: Optional[str] = ""
    feedback: Optional[str] = ""
    estrategia: Optional[str] = ""
    prazo: Optional[str] = ""
    x: Optional[float] = None
    y: Optional[float] = None


class PontoCreate(PontoBase):
    pass


class PontoUpdate(PontoBase):
    pass


class PontoOut(PontoBase):
    id: int


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pontos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cnpj TEXT,
                razao TEXT,
                tipo TEXT NOT NULL,
                prod TEXT,
                forn TEXT,
                preco TEXT,
                equip TEXT,
                dem TEXT,
                cls TEXT,
                obs TEXT,
                feedback TEXT,
                estrategia TEXT,
                prazo TEXT,
                x REAL,
                y REAL
            )
            """
        )
        conn.commit()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/pontos", response_model=List[PontoOut])
def list_pontos() -> List[PontoOut]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM pontos ORDER BY id DESC").fetchall()
    return [PontoOut(**dict(r)) for r in rows]


@app.post("/pontos", response_model=PontoOut)
def create_ponto(payload: PontoCreate) -> PontoOut:
    data = payload.model_dump()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO pontos (
                nome, cnpj, razao, tipo, prod, forn, preco, equip, dem, cls,
                obs, feedback, estrategia, prazo, x, y
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                data["nome"],
                data["cnpj"],
                data["razao"],
                data["tipo"],
                data["prod"],
                data["forn"],
                data["preco"],
                data["equip"],
                data["dem"],
                data["cls"],
                data["obs"],
                data["feedback"],
                data["estrategia"],
                data["prazo"],
                data["x"],
                data["y"],
            ),
        )
        conn.commit()
        new_id = cur.lastrowid
    return PontoOut(id=new_id, **data)


@app.put("/pontos/{ponto_id}", response_model=PontoOut)
def update_ponto(ponto_id: int, payload: PontoUpdate) -> PontoOut:
    data = payload.model_dump()
    with get_conn() as conn:
        row = conn.execute("SELECT id FROM pontos WHERE id = ?", (ponto_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Ponto nao encontrado")
        conn.execute(
            """
            UPDATE pontos SET
                nome = ?, cnpj = ?, razao = ?, tipo = ?, prod = ?, forn = ?, preco = ?,
                equip = ?, dem = ?, cls = ?, obs = ?, feedback = ?, estrategia = ?,
                prazo = ?, x = ?, y = ?
            WHERE id = ?
            """,
            (
                data["nome"],
                data["cnpj"],
                data["razao"],
                data["tipo"],
                data["prod"],
                data["forn"],
                data["preco"],
                data["equip"],
                data["dem"],
                data["cls"],
                data["obs"],
                data["feedback"],
                data["estrategia"],
                data["prazo"],
                data["x"],
                data["y"],
                ponto_id,
            ),
        )
        conn.commit()
    return PontoOut(id=ponto_id, **data)


@app.delete("/pontos/{ponto_id}", status_code=204)
def delete_ponto(ponto_id: int) -> Response:
    with get_conn() as conn:
        conn.execute("DELETE FROM pontos WHERE id = ?", (ponto_id,))
        conn.commit()
    return Response(status_code=204)
