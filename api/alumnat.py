#Funció que transforma l'informació de la taula alumne a diccionari
def alumne_schema(fetchAlumnes) -> dict:
    return {"NomAlumne": fetchAlumnes[0],
            "Cicle": fetchAlumnes[1],
            "Curs": fetchAlumnes[2],
            "Grup": fetchAlumnes[3],
            "DescAula": fetchAlumnes[4]
            }

            
#Funció que transforma l'informació de la taula aula a diccionari.
def aula_schema(aules) -> dict:
    return {
        "IdAula": aules[0],
        "DescAula": aules[1],
        "Edifici": aules[2],
        "Pis":aules[3],
        "CreatedAt":aules [4],
        "UpdatedAt":aules[5]
    }

#Funció que transorma una llista de la taula alumne a una llista de diccionaris.
def alumnat_schema(fetchAlumnes) -> dict:
    return [alumne_schema(alumne) for alumne in fetchAlumnes]

#Funció que transorma una llista de la taula aula a una llista de diccionaris.
def aules_schema(aules) -> dict:
    return [aula_schema(aula) for aula in aules]