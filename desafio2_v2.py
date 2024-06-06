import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):  #Nessa classe cliente, recebeu argumento endereço.
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nn@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor >0:
            self._saldo -= valor
            print("\n === Saque realizado com sucesso! ===")
            return True
        
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False
    
    def depositar(self, valor):
        if valor >0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        return True

class ContaCorrente (Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar (self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor >self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excedeu o limite! @@@")

        elif excedeu_saques:
            print ("\n@@@ Operação falhou! Número máximo de saques excedido! @@@")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência: \t{self.agencia}
            C/C: \t\t{self.numero}
            Titular: \t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            { 
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta):
        pass
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        

# Função para exibir o menu e retornar a opção escolhida pelo usuário
def menu():
    menu_text = """\
    ================== MENU ===================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário
    [q] Sair
    => """
    return input(textwrap.dedent(menu_text))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    return cliente.contas[0]

# Função para realizar um depósito
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para realizar um saque
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    
    cliente.realizar_transacao(conta, transacao)

# Função para exibir o extrato
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print ("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            # Usando uma formatação consistente com espaços controlados
            print(f"{transacao['tipo'] + ':':<12} R${transacao['valor']:>8.2f}")

    # Exibindo o saldo com formatação similar
    print(f"\n{'Saldo:':<12} R${conta.saldo:>8.2f}")
    print("==========================================")

# Função para criar um novo usuário
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n @@@ Já existe cliente com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

# Função para criar uma nova conta
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n === Conta criada com sucesso! ===")

# Função para listar todas as contas
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# Função principal
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)       

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta =len(contas) + 1
            criar_conta(numero_conta, clientes, contas)            

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Garantir que o script seja executado diretamente
if __name__ == "__main__":
    main()
    """_summary_
    """