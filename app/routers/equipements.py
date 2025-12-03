from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
import re
from ..models import Ordinateur, Routeur
from ..bdd import configure_db, get_session
from ..services.ssh_service import SSHConnection

ping_regex = re.compile(r"(?P<res>\d) received")

router = APIRouter(prefix="/supervision",tags=["Gestion des équipements"])

class CommandeRequest(BaseModel):
    commandes: str

@router.get("/Ordinateurs")
def read_Ordinateurs(session: Session = Depends(get_session)) -> list[Ordinateur]:
    return session.exec(select(Ordinateur)).all()


@router.get("/Ordinateur/{host_id}")
def read_Ordinateur(host_id: int, session: Session = Depends(get_session)) -> Ordinateur:
    ordinateur = session.get(Ordinateur, host_id)
    if not ordinateur:
        raise HTTPException(404, "Ordinateur not found")
    return ordinateur


@router.post("/Ordinateur")
def create_Ordinateur(ordinateur: Ordinateur, session: Session = Depends(get_session)) -> Ordinateur:
    session.add(ordinateur)
    session.commit()
    session.refresh(ordinateur)
    return ordinateur


@router.put("/Ordinateur/{host_id}")
def update_Ordinateur(host_id: int, updated_host: Ordinateur, session: Session = Depends(get_session)):
    ordinateur = session.get(Ordinateur, host_id)
    if not ordinateur:
        raise HTTPException(404, "Ordinateur not found")
    ordinateur.hostname = updated_host.hostname
    ordinateur.ip = updated_host.ip
    session.add(ordinateur)
    session.commit()
    session.refresh(ordinateur)
    return ordinateur


@router.delete("/Ordinateur/{host_id}")
def delete_Ordinateur(host_id: int, session: Session = Depends(get_session)):
    ordinateur = session.get(Ordinateur, host_id)
    if not ordinateur:
        raise HTTPException(404, "Ordinateur not found")
    session.delete(ordinateur)
    session.commit()
    return {"ok": True}
    

@router.get("/Routeurs")
def read_Routeurs(session: Session = Depends(get_session)) -> list[Routeur]:
    return session.exec(select(Routeur)).all()


@router.get("/Routeur/{host_id}")
def read_Routeur(host_id: int, session: Session = Depends(get_session)) -> Routeur:
    routeur = session.get(Routeur, host_id)
    if not routeur:
        raise HTTPException(404, "Routeur not found")
    return routeur


@router.post("/Routeur")
def create_Routeur(routeur: Routeur, session: Session = Depends(get_session)) -> Routeur:
    session.add(routeur)
    session.commit()
    session.refresh(routeur)
    return routeur


@router.put("/Routeur/{host_id}")
def update_Routeur(host_id: int, updated_host: Routeur, session: Session = Depends(get_session)):
    routeur = session.get(Routeur, host_id)
    if not routeur:
        raise HTTPException(404, "Routeur not found")
    routeur.hostname = updated_host.hostname
    routeur.ip = updated_host.ip
    session.add(routeur)
    session.commit()
    session.refresh(routeur)
    return routeur


@router.delete("/Routeur/{host_id}")
def delete_Routeur(host_id: int, session: Session = Depends(get_session)):
    routeur = session.get(Routeur, host_id)
    if not routeur:
        raise HTTPException(404, "Routeur not found")
    session.delete(routeur)
    session.commit()
    return {"ok": True}

@router.post("/ssh/Routeur/{id}")
def ssh_routeur(id: int, cmd: CommandeRequest, session: Session = Depends(get_session)):
    eqt = session.get(Routeur, id)
    if not eqt:
        raise HTTPException(404, "Equipement non trouvé")
        
    ssh_conn = SSHConnection(
        hostname=eqt.hostname if eqt.hostname else eqt.ip,
        username=eqt.username,
        password=eqt.password
        )
    
    output, error, code = ssh_conn.execute_command(cmd.commandes)
        
    return {
        "output": output,
        "error": error,
        "exit_code": code
    }

@router.post("/ssh/Ordinateur/{id}")
def ssh_ordinateur(id: int, cmd: CommandeRequest, session: Session = Depends(get_session)):
    eqt = session.get(Ordinateur, id)
    if not eqt:
        raise HTTPException(404, "Equipement non trouvé")
        
    ssh_conn = SSHConnection(
        hostname=eqt.hostname if eqt.hostname else eqt.ip,
        username=eqt.username,
        password=eqt.password,
        port=2222
        )
    
    output, error, code = ssh_conn.execute_command(cmd.commandes)
        
    return {
        "output": output,
        "error": error,
        "exit_code": code
    }