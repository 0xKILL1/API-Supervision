from sqlmodel import SQLModel, create_engine

sqlite_file_name = "supervision.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

sqlite_file_name2 = "routeur.db"
sqlite_url2 = f"sqlite:///{sqlite_file_name2}"
engineRouter = create_engine(sqlite_url2, echo=True)

sqlite_file_name3 = "ordinateur.db"
sqlite_url3 = f"sqlite:///{sqlite_file_name3}"
engineOrdinateur = create_engine(sqlite_url3, echo=True)

def configure_db():
    SQLModel.metadata.create_all(engine)


def configure_db_routeur():
    SQLModel.metadata.create_all(engineRouter)


def configure_db_ordinateur():
    SQLModel.metadata.create_all(engineOrdinateur)
