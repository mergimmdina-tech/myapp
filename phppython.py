from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

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
def get_db_connection():
    conn = mysql.connector.connect(
        # host="sql103.infinityfree.com",
        # user="if0_40195210",
        # password="mqSti6RMjKeweDJ",
        # database="if0_40195210_test_database"


        host = "sql300.infinityfree.com",
        user = "if0_40243036",
        password = "RjBUIgImvy4B",
        database = "if0_40243036_dbfundit"

        # host="localhost",
        # user="root",
        # password="Gimi2025",
        # database="databazaefundit"
    )
    return conn

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

@app.get("/s")
def fa():
    return "hello world"

#------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Mirë se erdhe në API!"}

@app.get("/njemesazh")
def text():
    return "hello world"

lista_personave=[]

class Person(BaseModel):
    name: str
    age: int

p1= Person(name="filan fisteky", age=25)
lista_personave.append(p1)

@app.get("/persons")
def array_persons():
    return lista_personave

@app.get("/persons/{age}")
def array_persons(age: int):
    for person in lista_personave:
        if person.age == age:
            return person

@app.post("/persons")
def array_persons(p: Person):
    lista_personave.append(p)
    return {"message": "U shtua me sukses", "person": p.dict()}

# fshij ndonje person nga lista
@app.delete("/persons/{name}")
def delete_person(name: str):
    for person in lista_personave:
        if person.name == name:
            lista_personave.remove(person)
            return {"message": f"{name} u fshi me sukses!"}
    return {"message": f"{name} nuk u gjet në listë."}


# fshij personat nga lista
@app.delete("/persons")
def delete_person():
    lista_personave.clear()
    return {"message": "Të gjitha personat u fshinë me sukses!"}

@app.put("/persons/{name}")
def update_person(name: str, age: int):
    for person in lista_personave:
        if person.name == name:
            person.age = age
            return {"message": f"Mosha e {name} u përditësua me sukses!", "person": person.dict()}
    return {"message": f"{name} nuk u gjet në listë."}

























