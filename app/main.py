from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import Equipement
from bdd import configure_db, engine
import socket, paramiko
from pydantic import BaseModel
from typing import Optional


def on_start_up():
    configure_db()

class SSHConnection(BaseModel):
    hostname: Optional[str] = None
    username: str
    password: str
    port: int = 22

    def execute_command(self, command: str) -> tuple[str, str, int]:
        try:
            client = paramiko.SSHClient()
            
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            client.connect(self.hostname, self.port, self.username, self.password, key_filename=self.key_filename)
            stdin, stdout, stderr = client.exec_command(command)
            
            exit_code = stdout.channel.recv_exit_status()
            result = stdout.read().decode(), stderr.read().decode(), exit_code
            client.close()
            return result
        except Exception as e:
            return "", str(e), -1
        
app = FastAPI(on_startup=[on_start_up])


@app.get("/")
def Hello():
    return {"Message":"Bienvenue sur cet API de supervision"},{"status":200}


@app.get("/equipements")
def read_hosts() -> list[Equipement]:
    with Session(engine) as session:
        return session.exec(select(Equipement)).all()


@app.get("/equipement/{host_id}")
def read_host(host_id: int) -> Equipement:
    with Session(engine) as session:
        host = session.get(Equipement, host_id)
        if not host:
            raise HTTPException(404, "equipement not found")
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
            raise HTTPException(404, "equipement not found")
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
            raise HTTPException(404, "equipement not found")
        session.delete(host)
        session.commit()
        return {"ok": True}


@app.post("/ssh/{id}")
def ssh(id: int):
    with Session(engine) as session:
        eqt = session.get(Equipement, id)
        ssh=SSHConnection(hostname=eqt.hostname,username="root",password="bonjour")
        resu=ssh.execute_command("ls")
        print(resu)