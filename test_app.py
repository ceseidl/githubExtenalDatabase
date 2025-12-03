
import pathlib
import pytest
from app import insert_log, fetch_logs

# expected_values.txt deve estar ao lado deste arquivo
TXT_FILE = pathlib.Path(__file__).with_name("valores.txt")

@pytest.fixture(scope="module")
def expected_values():
    lines = [line.strip() for line in TXT_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [tuple(line.split(",")) for line in lines]

def test_insert_and_compare(expected_values):
    # Insere os valores do TXT no banco
    for id_val, contexto_val in expected_values:
        insert_log(id_val, contexto_val)

    # Busca os registros do banco
    db_values = fetch_logs()

    # Verifica se os valores esperados estão contidos nos valores do banco
    for val in expected_values:
        assert val in db_values, f"Valor esperado {val} não encontrado no banco de dados." 
