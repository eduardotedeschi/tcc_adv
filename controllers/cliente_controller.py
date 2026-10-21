"""
Controller = ponte entre a tela (view) e os dados (repository).
Aqui moram as REGRAS DE NEGÓCIO: validação, formatação antes de salvar,
verificação de duplicidade etc. A view nunca deve montar SQL nem
conhecer a existência do banco — ela só chama métodos daqui.
"""
from typing import List, Tuple

from models.cliente import Cliente
from repositories.cliente_repository import ClienteRepository
from utils.validators import (
    limpar_espacos,
    limpar_numeros,
    validar_campos_obrigatorios,
    validar_cpf,
)


class ClienteController:

    def __init__(self):
        self.repo = ClienteRepository()

    def cadastrar(self, dados: dict) -> Tuple[bool, str]:
        obrigatorios = {
            "Nome": dados.get("nome"),
            "Nacionalidade": dados.get("nacionalidade"),
            "Estado Civil": dados.get("estado_civil"),
            "Profissão": dados.get("profissao"),
            "RG": dados.get("rg"),
            "CPF": dados.get("cpf"),
            "CEP": dados.get("cep"),
            "UF": dados.get("uf"),
            "Cidade": dados.get("cidade"),
            "Rua": dados.get("rua"),
            "Nº Rua": dados.get("numero"),
            "Bairro": dados.get("bairro"),
        }
        faltando = validar_campos_obrigatorios(obrigatorios)
        if faltando:
            return False, f"Preencha os campos obrigatórios: {', '.join(faltando)}."

        cpf_limpo = limpar_numeros(dados["cpf"])
        if not validar_cpf(cpf_limpo):
            return False, "CPF inválido."

        if self.repo.buscar_por_cpf(cpf_limpo):
            return False, "Já existe um cliente cadastrado com este CPF."

        cliente = Cliente(
            nome=limpar_espacos(dados["nome"]),
            cpf=cpf_limpo,
            nacionalidade=dados["nacionalidade"],
            estado_civil=dados["estado_civil"],
            profissao=limpar_espacos(dados["profissao"]),
            rg=limpar_numeros(dados["rg"]),
            cep=limpar_numeros(dados["cep"]),
            uf=limpar_espacos(dados["uf"]).upper(),
            cidade=limpar_espacos(dados["cidade"]),
            rua=limpar_espacos(dados["rua"]),
            numero=limpar_espacos(dados["numero"]),
            bairro=limpar_espacos(dados["bairro"]),
            telefone=limpar_numeros(dados.get("telefone", "")),
            email=limpar_espacos(dados.get("email", "")),
            nome_reu=limpar_espacos(dados.get("nome_reu", "")),
            cnpj_reu=limpar_numeros(dados.get("cnpj_reu", "")),
        )
        self.repo.inserir(cliente)
        return True, "Cliente cadastrado com sucesso."

    def atualizar(self, cliente_id: int, dados: dict) -> Tuple[bool, str]:
        if not self.repo.buscar_por_id(cliente_id):
            return False, "Cliente não encontrado."

        cpf_limpo = limpar_numeros(dados["cpf"])
        if not validar_cpf(cpf_limpo):
            return False, "CPF inválido."

        existente = self.repo.buscar_por_cpf(cpf_limpo)
        if existente and existente.id != cliente_id:
            return False, "Já existe outro cliente com este CPF."

        cliente = Cliente(
            id=cliente_id,
            nome=limpar_espacos(dados["nome"]),
            cpf=cpf_limpo,
            nacionalidade=dados["nacionalidade"],
            estado_civil=dados["estado_civil"],
            profissao=limpar_espacos(dados["profissao"]),
            rg=limpar_numeros(dados["rg"]),
            cep=limpar_numeros(dados["cep"]),
            uf=limpar_espacos(dados["uf"]).upper(),
            cidade=limpar_espacos(dados["cidade"]),
            rua=limpar_espacos(dados["rua"]),
            numero=limpar_espacos(dados["numero"]),
            bairro=limpar_espacos(dados["bairro"]),
            telefone=limpar_numeros(dados.get("telefone", "")),
            email=limpar_espacos(dados.get("email", "")),
            nome_reu=limpar_espacos(dados.get("nome_reu", "")),
            cnpj_reu=limpar_numeros(dados.get("cnpj_reu", "")),
        )
        self.repo.atualizar(cliente)
        return True, "Cliente atualizado com sucesso."

    def deletar(self, cliente_id: int) -> Tuple[bool, str]:
        if not self.repo.buscar_por_id(cliente_id):
            return False, "Cliente não encontrado."
        self.repo.deletar(cliente_id)
        return True, "Cliente removido com sucesso."

    def listar(self) -> List[Cliente]:
        return self.repo.listar_todos()

    def buscar(self, termo: str) -> List[Cliente]:
        if not termo.strip():
            return self.listar()
        return self.repo.buscar(termo)
