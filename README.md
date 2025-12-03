# CI com GitHub Actions (Python + Azure SQL)

Este repositório contém uma aplicação Python que escreve e lê da tabela `[dbo].[Log]` no Azure SQL Database e uma pipeline CI que **executa testes com pytest** em cada push/PR. Se os testes falharem, a build é interrompida.

## Estrutura

- `app.py` – conexão via `pyodbc` usando `SQL_CONNECTION_STRING` da variável de ambiente.
- `test_app.py` – insere valores do arquivo `expected_values.txt` e compara com o que está no banco.
- `expected_values.txt` – dois valores esperados no formato `id,contexto`.
- `requirements.txt` – dependências.
- `pytest.ini` – configuração de descoberta de testes.
- `.github/workflows/ci.yml` – workflow do GitHub Actions.

## Pré-requisitos

1. **Driver ODBC 18** no runner. O workflow instala com `apt-get` em `ubuntu-latest` (Linux). Referência oficial da Microsoft para instalação do driver ODBC no Linux.
2. **pyodbc** instalado e connection string com `DRIVER={ODBC Driver 18 for SQL Server}`.

## Como configurar os segredos

No repositório do GitHub:

1. Vá em **Settings → Secrets and variables → Actions → New repository secret**.
2. Crie o segredo `AZURE_SQL_PASSWORD` com a senha do usuário `seidl` do banco.

O workflow monta a variável de ambiente `SQL_CONNECTION_STRING` automaticamente usando esse segredo.

## Executar localmente

1. Crie um ambiente virtual, instale `requirements.txt` e configure `SQL_CONNECTION_STRING` no seu terminal:

```bash
export SQL_CONNECTION_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:petro.database.windows.net,1433;DATABASE=opensearch;UID=seidl;PWD=SuaSenhaAqui;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
pytest -vv
```

## Referências

- Instalação do **ODBC Driver 18** em Linux (Microsoft Learn).
- Guia rápido **pyodbc** para Azure SQL (Microsoft Learn).
- Exemplo de instalação do ODBC em GitHub Actions via `apt-get`.
