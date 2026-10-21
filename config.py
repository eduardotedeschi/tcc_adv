"""
Configurações globais da aplicação.
Qualquer caminho, constante de tela ou parâmetro compartilhado deve
morar aqui — nunca espalhado dentro das views/controllers.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
DOCUMENTOS_GERADOS_DIR = os.path.join(BASE_DIR, "documentos_gerados")
DATABASE_PATH = os.path.join(BASE_DIR, "database", "sistema_advogados.db")

APP_TITLE = "Sistema Advogados"
APP_VERSION = "0.1.0 (MVP)"

WINDOW_LARGURA_PCT = 0.75
WINDOW_ALTURA_PCT = 0.80
WINDOW_MIN_SIZE = (1024, 768)

THEME_DEFAULT = "light"  # "light" | "dark" | "auto"
