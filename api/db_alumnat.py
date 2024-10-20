from client import db_client

#Funció que mostra tota de la taula alumne.
def read_alumnes(orderby: str | None = None,  contain: str | None = None, skip: int = 0, limit: int | None = None ):
    try:
        conn = db_client()
        cur = conn.cursor()
        #Consulta per seleccionar tots els registres de la taula alumne
        sql_query = """select alumne.NomAlumne, alumne.Cicle, alumne.Curs, alumne.Grup, aula.DescAula
                    from alumne
                    join aula on alumne.IdAula = aula.IdAula
                    """
        if (orderby == "asc"):
            sql_query += " ORDER BY alumne.NomAlumne ASC"
        elif (orderby == "desc"):
            sql_query += " ORDER BY alumne.NomAlumne DESC"
            
        if(contain):
            sql_query += " WHERE alumne.NomAlumne ILIKE %s"
        
        if(limit is not None):
            sql_query += " LIMIT %s"
            
        if(skip > 0):
            sql_query += " OFFSET %s"
        
        parametres = []
        if contain:
            parametres.append(f"%{contain}%")
        if limit is not None:
            parametres.append(limit)
        if skip > 0 and skip <= 100:
            parametres.append(skip)
            

        cur.execute(sql_query, parametres)
        select_alumne = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return select_alumne

#Funció que mostra tota de la taula aula.
def readAules():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("select * from aula")
        select_aula = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return select_aula

#Funció que mostra tota de la taula alumne pasant l'id.
def read_id_alumne(IdAlumne):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select * from alumne WHERE IdAlumne = %s"
        value = (IdAlumne,)
        cur.execute(query,value)
        select_id = cur.fetchone()

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return select_id

#Funció que afegeix un nou alumne en la taula alumne.
def create_alumnes(IdAula,NomAlumne,Cicle,Curs,Grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "insert into alumne (IdAula,NomAlumne,Cicle,Curs,Grup) VALUES (%s,%s,%s,%s,%s);"
        values=(IdAula, NomAlumne,Cicle,Curs,Grup)
        cur.execute(query,values)
        conn.commit()
        insert_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return insert_id

#Funció que comprova si existeix idAula a la taula aula.
def aula_exist(IdAula):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select count(*) from aula where IdAula = %s"
        cur.execute(query,(IdAula,))
        result = cur.fetchone()
        
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    
    finally:
        conn.close()
    
    return result[0]>0

#Funció que pasant-li un nou id i un nou nom, cambia l'anterior pel nou.
def update_alumnes(IdAlumne, IdAula, NomAlumne,Cicle,Curs,Grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "update alumne SET IdAula = %s, NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s, UpdatedAt = NOW() WHERE IdAlumne = %s;"
        values=(IdAula, NomAlumne,Cicle,Curs,Grup, IdAlumne)
        cur.execute(query,values)
        updated_alumnes = cur.rowcount
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return updated_alumnes

#Funció que elimina alumnes amb l'id.
def delete_alumnes(IdAlumne):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM alumne WHERE IdAlumne = %s;"
        cur.execute(query,(IdAlumne,))
        deleted_alumnes = cur.rowcount
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return deleted_alumnes

#Funció que inserta aules a la base de dades.
def insert_aules(DescAula: str, Edifici: str, Pis: int):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        query = "SELECT IdAula FROM aula WHERE DescAula = %s;"
        cur.execute(query,(DescAula,))
        exist_aula = cur.fetchone()

        if aula_exist(DescAula):
            print(f"L'aula amb DescAula {DescAula} ja existeix.")
            return exist_aula[0]
        else:
            query_insert_aules= """
            INSERT INTO aula (DescAula, Edifici, Pis, CreatedAt, UpdatedAt)
            VALUES (%s,%s,%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING IdAula;
            """
            cur.execute(query_insert_aules, (DescAula, Edifici, Pis))
            IdAula = cur.fetchone()[0]
            conn.commit()
            print(f"Aula {DescAula} afegida correctament")
            return IdAula

    except Exception as e:
        print(f"Error al afegir aula {e}")
    
    finally:
        conn.close()
        
#Funció que inserta alumnes a la base de dades.
def insert_alumnes(NomAlumne: str, Cicle: str, Curs: int, Grup: str, IdAula: int):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        query = """
            SELECT * FROM alumne
            WHERE NomAlumne = %s AND Cicle = %s AND Curs = %s AND Grup = %s AND IdAula = %s;
        """
        cur.execute(query, (NomAlumne, Cicle, Curs, Grup, IdAula))
        alumne_exist = cur.fetchone()
        
        if alumne_exist:
            print(f"L'alumne {NomAlumne} ja existeix en el Cicle {Cicle}, Curs {Curs}, Grup {Grup}.")
        else:
            query_insert_alumnes = """
                INSERT INTO alumne (NomAlumne, Cicle, Curs, Grup, IdAula, CreatedAt, UpdatedAt)
                VALUES (%s,%s,%s,%s,%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
            """
            cur.execute(query_insert_alumnes, (NomAlumne, Cicle, Curs, Grup, IdAula))
            conn.commit()
            print(f"Alumne {NomAlumne} inserit correctament.")
    except Exception as e:
        print(f"Error en afegir alumne {e}")
    
    finally:
        conn.close()