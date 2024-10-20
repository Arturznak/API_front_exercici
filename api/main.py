from fastapi import FastAPI,HTTPException, Query, File, UploadFile

from pydantic import BaseModel

import csv

import io

from typing import List, Optional

from fastapi.middleware.cors import CORSMiddleware

import alumnat
import db_alumnat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Pydantic alumne.
class alumne(BaseModel):
    IdAula: int
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str

#Taula alumne
class tablaAlumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    DescAula: str

#Pydantic aula.
class aula(BaseModel):
    DescAula: str
    Edifici: str
    Pis: int

# GET
#Endpoint simple.
@app.get("/")
def read_root():
    return {"Alumnat API"}

#Endpoint que mostra tots els alumnes.
@app.get("/alumne/list", response_model=List[tablaAlumne]) 
def read_alumnes(orderby: Optional[str] = None, contain: Optional[str] = None, skip: int = Query(0, ge=0), limit: Optional[int] = Query (100, gt=0)):
    llista_alumnat = alumnat.alumnat_schema(db_alumnat.read_alumnes())
    if not llista_alumnat: 
        return []
    
    if contain:
        llista_alumnat = [alumne for alumne in llista_alumnat if contain.lower() in alumne["NomAlumne"].lower()]
    
    if orderby == "asc":
        llista_alumnat = sorted(llista_alumnat,key=lambda alumne : alumne["NomAlumne"])
    elif orderby == "desc":
        llista_alumnat = sorted(llista_alumnat,key=lambda alumne : alumne["NomAlumne"], reverse=True)
    
    llista_alumnat = llista_alumnat[skip: skip + limit]
    
    return llista_alumnat

#Endpoint que mostra alumne pel seu id.
@app.get("/alumne/show/{IdAlumne}", response_model=dict)
def read_alumnes_id(IdAlumne: int):
    result = db_alumnat.read_id_alumne(IdAlumne)
    if result is not None:
        alum = alumnat.alumne_schema(result)
    else:
        raise HTTPException(status_code=404, detail="Alumne no trobat")
    return alum

#Endpoint que mostra tots els alumnes y aules.
@app.get("/alumne/listAll", response_model=List[dict])
def read_all():
    try:
        alumnes_list = alumnat.alumnat_schema(db_alumnat.read_alumnes())
        aules_list = alumnat.aules_schema(db_alumnat.readAules())
        
        return [{"alumnes" : alumnes_list, "aules":aules_list}]
    
    except Exception as e: 
        return {"status": -1, "msg": f"Error: {e}"}
    
# POST
#Endpoint per afegir un nou alumne
@app.post("/alumne/add")
async def create_alumnes(data: alumne):
    IdAula = data.IdAula
    NomAlumne = data.NomAlumne
    Cicle = data.Cicle
    Curs = data.Curs
    Grup = data.Grup
    
    aula_exist = db_alumnat.aula_exist(IdAula) 
    
    if not aula_exist: 
        raise HTTPException(status_code=404, detail="Aquesta Id no existeix")
    
    alumne_id = db_alumnat.create_alumnes(IdAula,NomAlumne,Cicle,Curs,Grup)
    
    return {
        "msg": "S'ha afegit correctement"
    }
    
# Endpoint que càrrega alumnes i aules a les bases de dades a través d’un fitxer csv.
@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    
    # verifica que el fitxer es .csv
    if file.filename.endswith('.csv'):
        # el llegeix el .csv
        contents = await file.read()
        
        # el passa a JSON
        csv_data = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(csv_data)
        json_data = [row for row in csv_reader]
        
        for i in json_data:
            DescAula = i.get("DescAula")
            Edifici = i.get("Edifici")
            Pis = i.get("Pis")
            NomAlumne = i.get("NomAlumne")
            Cicle = i.get("Cicle")
            Curs = int(i.get("Curs"))
            Grup = i.get("Grup")

            IdAula = db_alumnat.insert_aules(DescAula, Edifici, Pis)
            
            db_alumnat.insert_alumnes(NomAlumne, Cicle, Curs, Grup, IdAula)
        
        return {
            "resultat": json_data,
            "msg":"Càrrega massiva realitzada correctament"
        }
    
    else:
        return {"error": "Només fichers CSV."}
    

# PUT  

#Endpoint que actualitza els registres de l'alumne segons l'id.
@app.put("/alumne/update/{IdAlumne}")
def update_alumnes(IdAlumne: int, IdAula: int, NomAlumne:str,Cicle:str,Curs:int,Grup:str):
    
    aula_exist = db_alumnat.aula_exist(IdAula)
    
    if not aula_exist:
        raise HTTPException(status_code=404, detail="Aquesta Id no existeix")

    updated_alumne = db_alumnat.update_alumnes(IdAlumne, IdAula, NomAlumne,Cicle,Curs,Grup)

    if (updated_alumne):
        return {
            "msg": "S'ha modificat correctement"
        }
    if updated_alumne == 0:
       raise HTTPException(status_code=404, detail="Alumne no trobat") 

# DELETE
#Endpoint que elimina a un alumne pel id.
@app.delete("/alumne/delete/{IdAlumne}")
def delete_alumnes(IdAlumne:int):
    
    deleted_alumnes = db_alumnat.delete_alumnes(IdAlumne)
    
    if (deleted_alumnes):
        return {
            "msg": "S'ha esborrat correctament"
        }
    if deleted_alumnes == 0:
       raise HTTPException(status_code=404, detail="Alumne per eliminar no trobat")