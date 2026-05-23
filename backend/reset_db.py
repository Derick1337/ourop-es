import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(__file__), "ouropaes.db")


def limpar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pontos")
    conn.commit()
    conn.close()
    print("Base de dados limpa com sucesso! O CRM está pronto para a apresentação.")


if __name__ == "__main__":
    limpar_banco()