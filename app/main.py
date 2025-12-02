from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import Equipement
from bdd import engine, configure_db

def on_start_up():
    configure_db()

app = FastAPI(on_startup=[on_start_up])


@app.get("/equipements")
def read_hosts() -> list[Equipement]:
    with Session(engine) as session:
        return session.exec(select(Equipement)).all()


@app.get("/equipement/{host_id}")
def read_host(host_id: int) -> Equipement:
    with Session(engine) as session:
        host = session.get(Equipement, host_id)
        if not host:
            raise HTTPException(404, "Host not found")
        return host


@app.post("/equipement")
def create_host(host: Equipement) -> Equipement:
    with Session(engine) as session:
        session.add(host)
        session.commit()
        session.refresh(host)
        return host


@app.put("/equipement/{host_id}")
def update_host(host_id: int, updated_host: Equipement):
    with Session(engine) as session:
        host = session.get(Equipement, host_id)
        if not host:
            raise HTTPException(404, "Host not found")
        host.hostname = updated_host.hostname
        host.ip = updated_host.ip
        session.add(host)
        session.commit()
        session.refresh(host)
        return host


@app.delete("/equipement/{host_id}")
def delete_host(host_id: int):
    with Session(engine) as session:
        host = session.get(Equipement, host_id)
        if not host:
            raise HTTPException(404, "Host not found")
        session.delete(host)
        session.commit()
        return {"ok": True}
