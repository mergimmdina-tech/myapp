
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# import mysql.connector

# app = FastAPI()

# Lejon kërkesa nga frontend lokal
#komentin ketu posht largoje deri te  (allow headers)
# app.add_middleware(
#     CORSMiddleware,
#   # allow_origins=["https://mergimapp.infinityfreeapp.com/index.php"],  # mund ta limitosh vetëm për localhost
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
#komentin ketu posht largoje deri te  (return conn)
# def get_db_connection():
#     conn = mysql.connector.connect(
#         # host="sql103.infinityfree.com",
#         # user="if0_40195210",
#         # password="mqSti6RMjKeweDJ",
#         # database="if0_40195210_test_database"


#         host = "sql300.infinityfree.com",
#         user = "if0_40243036",
#         password = "RjBUIgImvy4B",
#         database = "if0_40243036_dbfundit"

#         # host="localhost",
#         # user="root",
#         # password="Gimi2025",
#         # database="databazaefundit"
#     )
#     return conn

# @app.post("/delete_all")
# async def delete_all():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM registration_details")
#                                 # registration_details
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"success": True}

#komentin ketu posht largoje deri te vija (--- ...)
# @app.post("/delete_all")
# async def delete_all(request: Request):

#     data = await request.json()
#     d = data.get("d")

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(f"DELETE FROM registration_details WHERE username = '{d}' ")
#                                 # registration_details
#     print("Duke fshirë përdoruesin:", d)

#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"success": True}

# @app.get("/")
# def myfunc():
#     return {"message": "Hello from Mergim’s FastAPI!"}


#------------------------------------------------------------------------------------------------------------------------

# @app.get("/s")
# def fa():
#     return "hello world"

#------------------------------------------------------------------------------------------------------------------------

# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware


# app= FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Mirë se erdhe në API!"}

# @app.get("/njemesazh")
# def text():
#     return "hello world"

# lista_personave=[]

# class Person(BaseModel):
#     name: str
#     age: int

# p1= Person(name="filan fisteky", age=25)
# lista_personave.append(p1)

# @app.get("/persons")
# def array_persons():
#     return lista_personave

# @app.get("/persons/{age}")
# def array_persons(age: int):
#     for person in lista_personave:
#         if person.age == age:
#             return person

# @app.post("/persons")
# def array_persons(p: Person):
#     lista_personave.append(p)
#     return {"message": "U shtua me sukses", "person": p.dict()}

# # fshij ndonje person nga lista
# @app.delete("/persons/{name}")
# def delete_person(name: str):
#     for person in lista_personave:
#         if person.name == name:
#             lista_personave.remove(person)
#             return {"message": f"{name} u fshi me sukses!"}
#     return {"message": f"{name} nuk u gjet në listë."}


# # fshij personat nga lista
# @app.delete("/persons")
# def delete_person():
#     lista_personave.clear()
#     return {"message": "Të gjitha personat u fshinë me sukses!"}

# @app.put("/persons/{name}")
# def update_person(name: str, age: int):
#     for person in lista_personave:
#         if person.name == name:
#             person.age = age
#             return {"message": f"Mosha e {name} u përditësua me sukses!", "person": person.dict()}
#     return {"message": f"{name} nuk u gjet në listë."}



#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


#database -->
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

dburl= "mysql+pymysql://root:Gimi2025@localhost:3306/fastapi_students"
engine= create_engine(
    dburl,
    echo= True
)

SessionLocal= sessionmaker(
    bind= engine,
    autocommit= False,
    autoflush= False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

#models -->
from sqlalchemy import Column, Integer, String

class Person(Base):
    __tablename__= "personsss"

    id = Column(Integer, primary_key=True, index=True)
    name= Column(String(100), nullable= False)
    age= Column(Integer, nullable= False)

#main app-->
from fastapi import FastAPI
from fastapi import Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # për testim
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PersonCreate(BaseModel):
    name: str
    age: int

Base.metadata.create_all(bind= engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/persons")
def get_persons(db: Session = Depends(get_db)):
    persons = db.query(Person).all()
    return persons

@app.get("/persons/{person_id}")
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        return {"message": "Person not found"}
    return person

@app.post("/persons")
def add_person(person: PersonCreate, db: Session = Depends(get_db)):
    try:
        new_person = Person(name=person.name, age=person.age)
        #ketu ke per te be analiza ..
        db.add(new_person)
        db.commit() 
        db.refresh(new_person) 
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    return {"message": "Person added successfully"}

@app.delete("/persons")
def delete_all_persons(db: Session = Depends(get_db)):
    db.query(Person).delete()
    db.commit()
    return {"message": "All persons deleted successfully"}

@app.delete("/persons/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        return {"message": "Person not found"}
    db.delete(person)
    db.commit()
    return {"message": "Person deleted successfully"}

@app.put("/persons/{person_id}")
def update_person(person_id: int, person: PersonCreate, db: Session = Depends(get_db)):
    existing_person = db.query(Person).filter(Person.id == person_id).first()
    if existing_person is None:
        return {"message": "Person not found"}
    existing_person.name = person.name
    existing_person.age = person.age
    db.commit()
    db.refresh(existing_person)
    return {"message": "Person updated successfully", "person": existing_person}































