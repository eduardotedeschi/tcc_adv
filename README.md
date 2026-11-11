# Sistema Advogados — MVP de Software Gestor de Documentos Advocatícios

## Como rodar

```bash
cd ... # Entrar na pasta do projeto
python -m venv .venv # Criar o ambiente virtual
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process # Liberar execução de scripts nesta sessão do PowerShell
.\.venv\Scripts\Activate.ps1 # Ativar o ambiente virtual
pip install -r requirements.txt # Instalar as dependências
python main.py # Rodar o sistema
pytest # Rodar os testes automatizados
deactivate # Desativar o ambiente virtual ao terminar
```

## Arquitetura do projeto

O código foi dividido em camadas.

```
sistema_advogados/
├── main.py                 # ponto de entrada único
├── config.py                # caminhos e constantes globais
│
├── views/                   # CAMADA DE APRESENTAÇÃO (tkinter)
│   └── widgets/               # componentes reutilizáveis (combobox etc.)
│
├── controllers/             # REGRAS DE NEGÓCIO ( validações, formatação etc)
│
├── repositories/            # ACESSO A DADOS (só INSERT/UPDATE/DELETE/SELECT)
│
├── models/                  # ESTRUTURA DE DADOS (definição dos dados)
│   
├── database/                # BANCO DE DADOS
│  
├── utils/                   # funções auxiliares
│
├── assets/                  # imagens
├── templates/                # modelos .docx importados pelos usuários
├── documentos_gerados/       # saída dos documentos finais
└── tests/                    # testes automatizados
```

### 6. .gitignore
Já configurado neste projeto para ignorar `.venv/`, `__pycache__/`, o
arquivo `.db` do SQLite (cada integrante gera o seu localmente) e os
arquivos dentro de `templates/`/`documentos_gerados/` (dados de uso,
não código-fonte).
