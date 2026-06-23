from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    @staticmethod
    def get_all_states(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.Name
                        from state s, sighting s2 
                        where s.id =s2.state and year(s2.`datetime` )=%s
                        order by s.Name asc """
            cursor.execute(query, (year, ))

            for row in cursor:
                result.append(row["Name"])
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_all_sightings(year, state):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s2.*
                        from state s, sighting s2 
                        where s.id =s2.state and year(s2.`datetime` )=%s and s.Name =%s"""
            cursor.execute(query, (year, state))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result
    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime` ) as year
                        from sighting s 
                        order by year(s.`datetime` ) asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result
