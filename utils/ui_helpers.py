"""
Uso típico:

    from ui_helpers import aplicar_geometria_responsiva

    class TelaPrincipal:
        def __init__(self, root):
            self.root = root
            aplicar_geometria_responsiva(self.root)
            ...

    # Para uma tela secundária (Toplevel), útil em modais de geração
    # de petição, cadastro de teses, etc:

        janela = Toplevel(root)
        aplicar_geometria_responsiva(
            janela,
            largura_pct=0.5,
            altura_pct=0.6,
            min_w=600,
            min_h=400,
        )
"""

from tkinter import Misc


def calcular_geometria_responsiva(
    widget: Misc,
    largura_pct: float = 0.75,
    altura_pct: float = 0.80,
    min_w: int = 1024,
    min_h: int = 768,
) -> tuple[int, int, int, int]:
    """
    Calcula largura, altura e posição (x, y) de uma janela de forma
    proporcional à resolução de tela do usuário, em vez de usar
    valores fixos em pixels.

    Parâmetros
    ----------
    widget : Misc
        Instância de Tk ou Toplevel usada apenas para consultar a
        resolução da tela (winfo_screenwidth / winfo_screenheight).
    largura_pct : float
        Percentual da largura da tela que a janela deve ocupar (0 a 1).
    altura_pct : float
        Percentual da altura da tela que a janela deve ocupar (0 a 1).
    min_w : int
        Largura mínima absoluta em pixels. Garante legibilidade da
        interface em telas pequenas (evita quebra de layout).
    min_h : int
        Altura mínima absoluta em pixels.

    Retorna
    -------
    tuple[int, int, int, int]
        (largura, altura, pos_x, pos_y) já calculados para centralizar
        a janela na tela do usuário.
    """
    screen_w = widget.winfo_screenwidth()
    screen_h = widget.winfo_screenheight()

    largura = max(min_w, int(screen_w * largura_pct))
    altura = max(min_h, int(screen_h * altura_pct))

    # Nunca deixa a janela maior que a própria tela disponível
    largura = min(largura, screen_w)
    altura = min(altura, screen_h)

    # Centraliza a janela na tela
    pos_x = (screen_w - largura) // 2
    pos_y = (screen_h - altura) // 2

    return largura, altura, pos_x, pos_y


def aplicar_geometria_responsiva(
    widget: Misc,
    largura_pct: float = 0.75,
    altura_pct: float = 0.80,
    min_w: int = 1024,
    min_h: int = 768,
    resizable: bool = True,
    travar_maxsize_na_tela: bool = True,
) -> None:
    """
    Aplica geometria responsiva diretamente em uma janela Tk/Toplevel.

    Faz o cálculo (via calcular_geometria_responsiva) e já configura:
    - geometry (tamanho + posição centralizada)
    - resizable
    - minsize (fixo, definido pelo chamador)
    - maxsize (acompanha a resolução real do usuário, se
      travar_maxsize_na_tela=True)

    Parâmetros
    ----------
    widget : Misc
        Janela Tk (root) ou Toplevel a ser configurada.
    largura_pct, altura_pct : float
        Percentuais da tela a ocupar. Ajustar conforme o tipo de tela:
        telas principais podem usar valores maiores (ex.: 0.75-0.85);
        modais/diálogos menores (ex.: 0.4-0.6).
    min_w, min_h : int
        Tamanho mínimo absoluto em pixels, para não quebrar o layout
        interno (campos de CPF, CEP, treeviews, etc.).
    resizable : bool
        Se a janela pode ser redimensionada pelo usuário.
    travar_maxsize_na_tela : bool
        Se True, define maxsize com a resolução real do monitor do
        usuário (em vez de um valor fixo), permitindo aproveitar
        monitores maiores.
    """
    screen_w = widget.winfo_screenwidth()
    screen_h = widget.winfo_screenheight()

    largura, altura, pos_x, pos_y = calcular_geometria_responsiva(
        widget,
        largura_pct=largura_pct,
        altura_pct=altura_pct,
        min_w=min_w,
        min_h=min_h,
    )

    widget.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # resizable espera dois argumentos (largura, altura)
    widget.resizable(resizable, resizable)

    widget.minsize(width=min_w, height=min_h)

    if travar_maxsize_na_tela:
        widget.maxsize(width=screen_w, height=screen_h)