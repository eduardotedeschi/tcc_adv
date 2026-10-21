"""
Camada de conexão com o banco de dados.
Nenhuma outra parte do sistema deve importar `sqlite3` diretamente —
tudo passa por aqui, para que trocar de banco no futuro (ex.: Postgres
na nuvem, RF15 do levantamento de requisitos) implique mexer só neste
arquivo.
"""
import sqlite3
from contextlib import contextmanager

from config import DATABASE_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS escritorio (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    senha_hash    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cliente (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL,
    nacionalidade   TEXT,
    estado_civil    TEXT,
    profissao       TEXT,
    rg              TEXT,
    cpf             TEXT NOT NULL UNIQUE,
    cep             TEXT,
    uf              TEXT,
    cidade          TEXT,
    rua             TEXT,
    numero          TEXT,
    bairro          TEXT,
    telefone        TEXT,
    email           TEXT,
    nome_reu        TEXT,
    cnpj_reu        TEXT,
    criado_em       TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS area_direito (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome    TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS modelo_documento (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    tipo                TEXT NOT NULL,   -- Contrato, Declaração, Procuração...
    caminho_arquivo     TEXT NOT NULL,
    area_direito_id     INTEGER,
    FOREIGN KEY (area_direito_id) REFERENCES area_direito(id)
);

CREATE TABLE IF NOT EXISTS tese (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    caminho_arquivo     TEXT NOT NULL,
    area_direito_id     INTEGER,
    FOREIGN KEY (area_direito_id) REFERENCES area_direito(id)
);

CREATE TABLE IF NOT EXISTS documento_gerado (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id          INTEGER NOT NULL,
    modelo_id           INTEGER,
    area_direito_id     INTEGER,          -- opcional (0,1) — só classificação
    nome_documento      TEXT NOT NULL,
    tipo_documento      TEXT,
    caminho_arquivo     TEXT,
    data_gerada         TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id),
    FOREIGN KEY (modelo_id) REFERENCES modelo_documento(id),
    FOREIGN KEY (area_direito_id) REFERENCES area_direito(id)
);

CREATE TABLE IF NOT EXISTS reu_parte_adversa (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                    TEXT NOT NULL,
    cnpj_cpf                TEXT,
    documento_gerado_id     INTEGER NOT NULL,
    FOREIGN KEY (documento_gerado_id) REFERENCES documento_gerado(id)
);

-- Tabela de junção: quais teses (e em que ordem) compõem uma petição.
-- A regra "toda petição precisa de ao menos 1 tese" é validada na camada
-- de aplicação (controllers/gerar_peticao_controller.py), não no banco —
-- SQLite não garante cardinalidade mínima via FOREIGN KEY sozinha.
CREATE TABLE IF NOT EXISTS documento_gerado_tese (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_gerado_id     INTEGER NOT NULL,
    tese_id                 INTEGER NOT NULL,
    ordem                   INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (documento_gerado_id) REFERENCES documento_gerado(id),
    FOREIGN KEY (tese_id) REFERENCES tese(id)
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Cria as tabelas se elas ainda não existirem. Chamado uma vez no main.py."""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


@contextmanager
def db_cursor():
    """
    Uso:
        with db_cursor() as cur:
            cur.execute("SELECT * FROM cliente")
            resultados = cur.fetchall()
    Garante commit automático e fechamento da conexão.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()
