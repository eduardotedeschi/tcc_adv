from tkinter import Misc


def calcular_geometria_responsiva(
    widget: Misc,
    largura_pct: float = 0.75,
    altura_pct: float = 0.80,
    min_w: int = 1024,
    min_h: int = 768,
) -> tuple[int, int, int, int]:
    
    screen_w = widget.winfo_screenwidth()
    screen_h = widget.winfo_screenheight()

    largura = max(min_w, int(screen_w * largura_pct))
    altura = max(min_h, int(screen_h * altura_pct))

    largura = min(largura, screen_w)
    altura = min(altura, screen_h)

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

    widget.resizable(resizable, resizable)

    widget.minsize(width=min_w, height=min_h)

    if travar_maxsize_na_tela:
        widget.maxsize(width=screen_w, height=screen_h)