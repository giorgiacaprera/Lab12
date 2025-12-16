from database.DB_connect import DBConnect

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def get_all_rifugi_grafo(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT * 
                    FROM rifugio, connessione
                    WHERE rifugio.id = connessione.id_rifugio1 
                    OR rifugio.id = connessione.id_rifugio2
                    AND connessione.year <= %s"""
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni_pesate(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM connessione
                    WHERE anno <= %s"""
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result