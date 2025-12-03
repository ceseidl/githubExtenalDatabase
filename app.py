
"""
Aplicação simples que conecta ao Azure SQL Database e insere/consulta
na tabela [dbo].[Log]. A conexão vem da variável de ambiente
SQL_CONNECTION_STRING (ODBC completo).
"""
import os
import pyodbc

CONN_STR_ENV = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:petro.database.windows.net,1433;DATABASE=opensearch;UID=seidl;PWD=82Portao503!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


def get_connection():
    conn_str = os.getenv(CONN_STR_ENV)
    if not conn_str:
        raise RuntimeError(
            f"Variável de ambiente {CONN_STR_ENV} não definida. "
            "Configure-a com o connection string ODBC, por exemplo: "
            "DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:petro.database.windows.net,1433;"
            "DATABASE=opensearch;UID=seidl;PWD=...;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )
    return pyodbc.connect(conn_str)


def insert_log(id_value: str, contexto_value: str) -> None:
    """Insere um registro na tabela [dbo].[Log]."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO [dbo].[Log] (id, contexto) VALUES (?, ?)",
            (id_value, contexto_value),
        )
        conn.commit()
    finally:
        conn.close()


def fetch_logs():
    """Retorna todos os registros (id, contexto) como lista de tuplas."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, contexto FROM [dbo].[Log]")
        rows = cursor.fetchall()
        return [(row[0], row[1]) for row in rows]
    finally:
        conn.close()


if __name__ == "__main__":
    # Exemplo rápido para rodar local
    insert_log("demo", "execucao_local")
    print("Registros:", fetch_logs())
