from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from models import Equipement
from bdd import configure_db, engine
import socket, paramiko
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
import threading
import re,os
import json
from models import Ordinateur, Equipement, Routeur
from bdd import configure_db, engine, get_session

ping_regex = re.compile(r"(?P<res>\d) received")

class CommandeRequest(BaseModel):
    commandes: str

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
            
            client.connect(self.hostname, self.port, self.username, self.password)
            stdin, stdout, stderr = client.exec_command(command)
            
            exit_code = stdout.channel.recv_exit_status()
            result = stdout.read().decode(), stderr.read().decode(), exit_code
            client.close()
            return result
        except Exception as e:
            return "", str(e), -1
        
app = FastAPI(on_startup=[on_start_up])


@app.get("/equipements")
def read_hosts(session: Session = Depends(get_session)) -> list[Equipement]:
    return session.exec(select(Equipement)).all()


@app.get("/equipement/{host_id}")
def read_host(host_id: int, session: Session = Depends(get_session)) -> Equipement:
    host = session.get(Equipement, host_id)
    if not host:
        raise HTTPException(404, "Host not found")
    return host


@app.post("/equipement")
def create_host(host: Equipement, session: Session = Depends(get_session)) -> Equipement:
    return host


@app.put("/equipement/{host_id}")
def update_host(host_id: int, updated_host: Equipement, session: Session = Depends(get_session)):
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
def delete_host(host_id: int, session: Session = Depends(get_session)):
    host = session.get(Equipement, host_id)
    if not host:
        raise HTTPException(404, "Host not found")
    session.delete(host)
    session.commit()
    return {"ok": True}


@app.post("/ssh/{id}")
def ssh(id: int, cmd: CommandeRequest, session: Session = Depends(get_session)):
    eqt = session.get(Equipement, id)
    if not eqt:
        raise HTTPException(404, "Equipement non trouvé")
        
    ssh_conn = SSHConnection(
        hostname=eqt.hostname,
        username=eqt.username,
        password=eqt.password
        )
    output, error, code = ssh_conn.execute_command(cmd.commandes)
        
    return {
        "output": output,
        "error": error,
        "exit_code": code
    }

@app.get("/start/cron/{id}")
def startcron(id: int, session: Session = Depends(get_session)):
    eqt = session.get(Equipement, id)
    if not eqt:
        raise HTTPException(404, "Equipement non trouvé")
    else:
        threading.Thread(target=worker(id)).start()

@app.get("/stop/cron/{id}")
def stopcron(id:int, session: Session = Depends(get_session)):
    eqt = session.get(Equipement, id)
    if not eqt:
        raise HTTPException(404, "Equipement non trouvé")
    else:
        threading.Thread(target=worker(id=id,ip=eqt.ip)).stop()

@app.get("/dispo/{id}")
def stopcron(id:int, session: Session = Depends(get_session)):
    eqt = session.get(Equipement, id)
    if not eqt:
        raise HTTPException(404, "Equipement non trouvé")
    else:
        threading.Thread(target=worker(id=id,ip=eqt.ip)).stop()

def worker(ip:str,id:int):
    ping_reussi=0
    total_ping=0

    cmd = os.popen(f"ping -c 2 {ip}")
    res = cmd.read()
    matchs = ping_regex.search(res)
    if int(matchs.group("res")) == 2:
        ping_reussi+=1
    else:
        total_ping+=1
    calcul=ping_reussi/total_ping
    proba={id:calcul}

    with open("dispo.json","a")as f:
        json.load(proba,f)
    
#async pas thread
#bdd 3 avec equipement ordi et routeur
#faire jwt
#
@app.get("/Ordinateurs")
def read_Ordinateurs(session: Session = Depends(get_session)) -> list[Ordinateur]:
    return session.exec(select(Ordinateur)).all()


@app.get("/Ordinateur/{host_id}")
def read_Ordinateur(host_id: int, session: Session = Depends(get_session)) -> Ordinateur:
    ordinateur = session.get(Ordinateur, host_id)
    if not ordinateur:
        raise HTTPException(404, "Host not found")
    return ordinateur


@app.post("/Ordinateur")
def create_Ordinateur(ordinateur: Ordinateur, session: Session = Depends(get_session)) -> Ordinateur:
    session.add(ordinateur)
    session.commit()
    session.refresh(ordinateur)
    return ordinateur


@app.put("/Ordinateur/{host_id}")
def update_Ordinateur(host_id: int, updated_host: Ordinateur, session: Session = Depends(get_session)):
    ordinateur = session.get(Equipement, host_id)
    if not ordinateur:
        raise HTTPException(404, "Host not found")
    ordinateur.hostname = updated_host.hostname
    ordinateur.ip = updated_host.ip
    session.add(ordinateur)
    session.commit()
    session.refresh(ordinateur)
    return ordinateur


@app.delete("/Ordinateur/{host_id}")
def delete_Ordinateur(host_id: int, session: Session = Depends(get_session)):
    ordinateur = session.get(Ordinateur, host_id)
    if not ordinateur:
        raise HTTPException(404, "Host not found")
    session.delete(ordinateur)
    session.commit()
    return {"ok": True}
    

@app.get("/Routeurs")
def read_Routeurs(session: Session = Depends(get_session)) -> list[Equipement]:
    return session.exec(select(Equipement)).all()


@app.get("/Routeur/{host_id}")
def read_Routeur(host_id: int, session: Session = Depends(get_session)) -> Equipement:
    routeur = session.get(Routeur, host_id)
    if not routeur:
        raise HTTPException(404, "Host not found")
    return routeur


@app.post("/Routeur")
def create_Routeur(routeur: Routeur, session: Session = Depends(get_session)) -> Routeur:
    session.add(routeur)
    session.commit()
    session.refresh(routeur)
    return routeur


@app.put("/Routeur/{host_id}")
def update_Routeur(host_id: int, updated_host: Routeur, session: Session = Depends(get_session)):
    routeur = session.get(Routeur, host_id)
    if not routeur:
        raise HTTPException(404, "Host not found")
    routeur.hostname = updated_host.hostname
    routeur.ip = updated_host.ip
    session.add(routeur)
    session.commit()
    session.refresh(routeur)
    return routeur


@app.delete("/Routeur/{host_id}")
def delete_Routeur(host_id: int, session: Session = Depends(get_session)):
    routeur = session.get(Routeur, host_id)
    if not routeur:
        raise HTTPException(404, "Host not found")
    session.delete(routeur)
    session.commit()
    return {"ok": True}
