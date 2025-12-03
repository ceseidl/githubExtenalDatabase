import pathlib
import pytest
from app import insert_log, fetch_logs

# expected_values.txt deve estar ao lado deste arquivo
TXT_FILE = pathlib.Path(__file__).with_name("valores.txt")

# Connection string direta (troque {SUA_SENHA} pela senha real)
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:petro.database.windows.net,1433;"
    "DATABASE=opensearch;"
    "UID=seidl;"
    "PWD=82Portao503!;"
    "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

@pytest.fixture(scope="module")
def expected_values():
    lines = [line.strip() for line in TXT_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [tuple(line.split(",")) for line in lines]

def test_insert_and_compare(expected_values):
    # Insere os valores do TXT no banco
    for id_val, contexto_val in expected_values:
        insert_log(CONNECTION_STRING, id_val, contexto_val)

    # Busca os registros do banco
    db_values = fetch_logs(CONNECTION_STRING)

    # Verifica se os valores esperados estão contidos nos valores do banco
    for val in expected_values:
        assert val in db_values, f"Valor {val} não encontrado no banco."
