from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                       FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_cromosomi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT g.Chromosome as c
                        FROM genes g"""
            cursor.execute(query)

            for row in cursor:
                result.append(row['c'])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(cMin, cMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT *
                        FROM genes g
                        WHERE g.Chromosome >= %s
                                and g.Chromosome <= %s"""
            cursor.execute(query, (cMin, cMax))

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllArchi(cMin, cMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t1.g1 as g1, t2.g2 as g2, i.Expression_Corr as peso
                        FROM interactions i, 
                                (SELECT g.GeneID as g1, c.Localization as l1
                                FROM genes g, classification c
                                WHERE g.GeneID = c.GeneID
                                    and g.Chromosome >= %s
                                    and g.Chromosome <= %s) t1,
                                (SELECT g.GeneID as g2, c.Localization as l2
                                FROM genes g, classification c
                                WHERE g.GeneID = c.GeneID
                                    and g.Chromosome >= %s
                                    and g.Chromosome <= %s) t2
                        WHERE  t1.g1 != t2.g2
                                and t1.l1 = t2.l2
                                and ((i.GeneID1 = t1.g1 and i.GeneID2 = t2.g2 ) or (i.GeneID1 = t2.g2 and i.GeneID2 = t1.g1))
                                """
            cursor.execute(query, (cMin, cMax, cMin, cMax))

            for row in cursor:
                result.append((row['g1'], row['g2'], row['peso']))

            cursor.close()
            cnx.close()
        return result

