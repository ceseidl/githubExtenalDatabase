import pyodbc


def get_connection(conn_str: str):
    if not conn_str or "DRIVER=" not in conn_str:
        raise RuntimeError("Connection string inválida. Forneça o ODBC completo.")
    return pyodbc.connect(conn_str)


def insert_log(conn_str: str, id_value: str, contexto_value: str) -> None:
    """Insere um registro na tabela [dbo].[Log]."""
    conn = get_connection(conn_str)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO [dbo].[Log] (id, contexto) VALUES (?, ?)",
            (id_value, contexto_value),
        )
        conn.commit()
    finally:
        conn.close()


def fetch_logs(conn_str: str):
    """Retorna todos os registros (id, contexto) como lista de tuplas."""
    conn = get_connection(conn_str)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, contexto FROM [dbo].[Log]")
        rows = cursor.fetchall()
        return [(row[0], row[1]) for row in rows]
    finally:
        conn.close()


if __name__ == "__main__":
    # EXEMPLO: troque {SUA_SENHA} pela senha real
    CS = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=tcp:petro.database.windows.net,1433;"
        "DATABASE=opensearch;"
        "UID=seidl;"
        "PWD=82Portao503!;"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    insert_log(CS, "demo", "execucao_local")
    print("Registros:", fetch_logs(CS))
