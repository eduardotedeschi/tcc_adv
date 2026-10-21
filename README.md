# Sistema Advogados — Protótipo de Software Gestor de Documentos Advocatícios

## Como rodar

```bash
cd C:\Users\tedes\Downloads\sistema_advogados_estrutura_completa\sistema_advogados # Entrar na pasta do projeto
python -m venv .venv # Criar o ambiente virtual (só na primeira vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process # Liberar execução de scripts nesta sessão do PowerShell
.\.venv\Scripts\Activate.ps1 # Ativar o ambiente virtual
pip install -r requirements.txt # Instalar as dependências (só precisa repetir se requirements.txt mudar)
python main.py # Rodar o sistema
pytest # (Opcional) Rodar os testes automatizados
deactivate # Desativar o ambiente virtual ao terminar
```

## Criar branch
```bash
git checkout -b <nome-da-branch> # Cria a branch e já entra nela
git checkout <nome-da-branch> ou git checkout <nome-da-branch> # Muda para a banch
git merge <nome-da-branch> # Junta os commits da branch especificada com a que está no momento
git branch -d <nome-da-branch> # Exlui a branch com segurança
```

## Arquitetura do projeto

O código foi dividido em camadas. A regra de ouro é: **cada camada só
conhece a camada logo abaixo dela.**

```
sistema_advogados/
├── main.py                 # ponto de entrada único
├── config.py                # caminhos e constantes globais
│
├── views/                   # CAMADA DE APRESENTAÇÃO (tkinter)
│   ├── main_window.py        # monta menu e alterna entre telas
│   ├── login_view.py
│   ├── cliente_view.py
│   ├── widgets/               # componentes reutilizáveis (combobox etc.)
│
├── controllers/             # REGRAS DE NEGÓCIO
│   ├── cliente_controller.py  # validações, formatação, decide se pode salvar
│   └── auth_controller.py
│
├── repositories/            # ACESSO A DADOS (SQL)
│   ├── cliente_repository.py  # só INSERT/UPDATE/DELETE/SELECT
│   └── escritorio_repository.py
│
├── models/                  # ESTRUTURA DE DADOS (dataclasses puras)
│   └── cliente.py
│
├── database/
│   └── connection.py        # conexão SQLite + schema
│
├── utils/                   # funções auxiliares sem estado
│   ├── validators.py          # validação de CPF, campos obrigatórios
│   ├── formatters.py          # máscaras de CPF/CEP/telefone
│   ├── cep_service.py         # integração com ViaCEP
│   └── opcoes.py               # listas fixas (nacionalidades etc.)
│
├── assets/                  # imagens (logo.png etc.)
├── templates/                # modelos .docx importados pelos usuários
├── documentos_gerados/       # saída dos documentos finais
└── tests/                    # testes automatizados (pytest)
```

**Por que separar assim?**
Fluxo de uma ação, ex. "cadastrar cliente":

`cliente_view.py` (lê o formulário)
→ `cliente_controller.py` (valida CPF, campos obrigatórios, formata dados)
→ `cliente_repository.py` (executa o INSERT no banco)
→ `models/cliente.py` (o "pacote de dados" que viaja entre as camadas)

Se um dia vocês trocarem tkinter por outra interface, só `views/` muda.
Se trocarem SQLite por outro banco, só `repositories/` e `database/` mudam.
Isso é o que torna o projeto **testável** (dá pra testar `controllers/` e
`utils/` sem abrir nenhuma janela — ver `tests/test_validators.py`) e
**dividido de forma justa entre os 3 integrantes** (cada um pode pegar
uma tela + seu controller + seu repository sem esbarrar no código dos
outros).

## Como replicar o padrão para uma tela nova (ex. Documentos)

1. `models/documento.py` — dataclass `Documento`
2. `repositories/documento_repository.py` — CRUD SQL
3. `controllers/documento_controller.py` — validações (nome obrigatório,
   tipo obrigatório, arquivo precisa existir no disco)
4. `views/documento_view.py` — a tela em si, copiando a estrutura de
   `cliente_view.py`
5. Registrar em `views/main_window.py`, dentro de `self.telas`

## Fluxo de trabalho no GitHub (equipe de 3 pessoas)

### 1. Estrutura de branches
- `main` — sempre estável, é o produto final.
- `develop` — branch de integração, onde as features vão se juntando.
- `feature/<nome-da-tela-ou-tarefa>` — uma branch por tarefa (excluida após execução da tarefa). Exemplos:
  - `feature/tela-documentos`
  - `feature/composicao-peticao`
  - `feature/validacao-cpf`

Nunca commitar direto na `main`. Trabalhar na `develop`/`feature/*` e
integrar via Pull Request.

### 2. Passo a passo do dia a dia
```bash
git checkout develop
git pull origin develop
git checkout -b feature/tela-documentos

# ... trabalha, faz commits pequenos e frequentes ...
git add .
git commit -m "feat: cria repository e controller de documento"

git push origin feature/tela-documentos
```
Depois, abrir um **Pull Request** de `feature/tela-documentos` → `develop`
no GitHub, pedindo revisão de pelo menos 1 dos outros 2 integrantes antes
de dar merge. Isso evita que código quebrado entre na branch principal e
faz com que todos leiam o código dos colegas (bom para o relatório final
e para pegar bugs cedo).

### 3. Convenção de mensagens de commit
Usar prefixos simples:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `refactor:` reorganização sem mudar comportamento
- `docs:` documentação (README, comentários)
- `test:` testes automatizados

Exemplo: `git commit -m "fix: mascara de CEP não aceitava apagar"`

### 4. Issues e board
Utilizar o Issues do GitHub para anotar os requisitos, bugs, ideias etc.

Usar prefixos simples:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `style:` estilo e interface do usuário
- `documentation:` documentação
- `security:` segurança
- `etc`

Exemplo: `feat(exportação): Botões de exportar arquivo (docx ou pdf) na tela "Gerenciar Modelos"`

### 5. Dividindo entre os 3 integrantes
Como a arquitetura é em camadas verticais por funcionalidade, uma boa
divisão é dar uma tela inteira (view + controller + repository) para
cada pessoa:
- **Pessoa A:** Documentos (importar/remover templates .docx)
- **Pessoa B:** Geração de documento + composição de petição
- **Pessoa C:** Clientes/Documentos (listagem, export PDF/DOCX)

Assim ninguém edita o mesmo arquivo ao mesmo tempo (menos conflito de
merge) e cada um "dono" de uma parte facilita a divisão de notas/relatório.

### 6. .gitignore
Já configurado neste projeto para ignorar `.venv/`, `__pycache__/`, o
arquivo `.db` do SQLite (cada integrante gera o seu localmente) e os
arquivos dentro de `templates/`/`documentos_gerados/` (dados de uso,
não código-fonte).
