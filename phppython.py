from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# Lejon kërkesa nga frontend lokal
app.add_middleware(
    CORSMiddleware,
  # allow_origins=["https://mergimapp.infinityfreeapp.com/index.php"],  # mund ta limitosh vetëm për localhost
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.post("/delete_all")
async def delete_all(request: Request):

    data = await request.json()
    d = data.get("d")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM registration_details WHERE username = '{d}' ")
                                # registration_details
    print("Duke fshirë përdoruesin:", d)

    conn.commit()
    cursor.close()
    conn.close()
    return {"success": True}

@app.get("/")
def myfunc():
    return {"message": "Hello from Mergim’s FastAPI!"}























