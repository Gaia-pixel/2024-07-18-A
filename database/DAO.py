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
            query = """SELECT DISTINCT t1.g1 as g1, t1.f1 as f1, t2.g2 as g2, t2.f2 as f2, i.Expression_Corr as peso
                        FROM interactions i,
                          (SELECT g.GeneID AS g1, `Function` AS f1, g.Chromosome, c.Localization
                           FROM genes g
                           JOIN classification c ON g.GeneID = c.GeneID
                           WHERE g.Chromosome BETWEEN %s AND %s) t1,
                           (SELECT g.GeneID AS g2, `Function` AS f2, g.Chromosome, c.Localization
                           FROM genes g
                           JOIN classification c ON g.GeneID = c.GeneID
                           WHERE g.Chromosome BETWEEN %s AND %s) t2
                          WHERE ((i.GeneID1 = t1.g1 AND i.GeneID2 = t2.g2)
                            OR (i.GeneID2 = t1.g1 AND i.GeneID1 = t2.g2))
                          AND t1.g1 <> t2.g2
                          AND t1.Localization = t2.Localization
                          AND t1.Chromosome <= t2.Chromosome"""
            cursor.execute(query, (cMin, cMax, cMin, cMax))

            for row in cursor:
                result.append((row['g1'], row['f1'], row['g2'], row['f2'], row['peso']))

            cursor.close()
            cnx.close()
        return result

