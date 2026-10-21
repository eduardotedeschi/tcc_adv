"""
Máscaras automáticas de formatação (RNF02 do levantamento de requisitos).
Usadas nos binds dos Entry, ex:
    entry.bind("<KeyRelease>", lambda e: aplicar_mascara_cpf(entry))
"""
from tkinter import Entry

from utils.validators import limpar_numeros


def _reposicionar_cursor(entry: Entry, texto_formatado: str) -> None:
    entry.delete(0, "end")
    entry.insert(0, texto_formatado)
    entry.icursor("end")


def mascara_cpf(entry: Entry) -> None:
    numeros = limpar_numeros(entry.get())[:11]
    partes = [numeros[:3], numeros[3:6], numeros[6:9]]
    texto = ".".join(p for p in partes if p)
    if len(numeros) > 9:
        texto += f"-{numeros[9:]}"
    _reposicionar_cursor(entry, texto)


def mascara_cep(entry: Entry) -> None:
    numeros = limpar_numeros(entry.get())[:8]
    texto = numeros[:5]
    if len(numeros) > 5:
        texto += f"-{numeros[5:]}"
    _reposicionar_cursor(entry, texto)


def mascara_telefone(entry: Entry) -> None:
    numeros = limpar_numeros(entry.get())[:11]
    if len(numeros) <= 10:
        texto = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:10]}"
    else:
        texto = f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:11]}"
    _reposicionar_cursor(entry, texto.strip(" -()"))
