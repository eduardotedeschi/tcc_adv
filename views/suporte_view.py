"""
Tela de suporte/FAQ (RNF07). Conteúdo estático por enquanto — o time
pode migrar para um arquivo .json/.md se a lista crescer muito.
"""
from tkinter import ttk

PERGUNTAS_FREQUENTES = [
    ("Por que meu CPF não foi aceito?",
     "O sistema valida o CPF pelos dígitos verificadores oficiais. Confira "
     "se os números foram digitados corretamente."),
    ("O CEP não preencheu o endereço automaticamente, o que fazer?",
     "Verifique sua conexão com a internet — o preenchimento depende da "
     "API pública ViaCEP. Você também pode preencher manualmente."),
    ("Qual o formato de variável aceito nos templates .docx?",
     "Use {{campo}}, por exemplo {{nome}} ou {{cpf}}, exatamente como o "
     "nome do campo do cliente cadastrado."),
    ("Consigo gerar uma petição sem selecionar nenhuma tese?",
     "Não. Pelo menos uma tese deve ser marcada no checklist antes de gerar."),
]


class SuporteView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        ttk.Label(self, text="Suporte / FAQ", font=("Helvetica", 18, "bold")).place(relx=0.02, rely=0.02)

        y = 0.1
        for pergunta, resposta in PERGUNTAS_FREQUENTES:
            ttk.Label(self, text=f"• {pergunta}", font=("Helvetica", 11, "bold"),
                      wraplength=850, justify="left").place(relx=0.02, rely=y)
            y += 0.05
            ttk.Label(self, text=resposta, wraplength=850, justify="left").place(relx=0.04, rely=y)
            y += 0.09
