from abc import ABC, abstractmethod
import datetime as dt


# Classes:
class PessoaFisica:
    def __init__(self, cpf, nome, data_nascimento):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento


class Cliente(PessoaFisica):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(cpf, nome, data_nascimento)
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas

    @classmethod
    def criar_cliente(cls, cpf, nome, data_nascimento, endereco):
        return cls(cpf, nome, data_nascimento, endereco) 

    # Metodo para adicionar contas a lista de conta do cliente
    def adicionar_conta(self, conta):
        self._contas.append(conta)

    # Metodo do professor de Python para exibir da forma Cliente: cpf:
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self._cpf}')>"


class ContaCorrente:
    _limite = 500
    _limite_saques = 3
    _limite_transacoes = 10

    def __init__(self):
        pass
    
    @staticmethod
    def visualizar_limite(_limite):
        return _limite
    
    @staticmethod
    def visualizar_limite_saques(_limite_saques):
        return _limite_saques


class Historico:
    def __init__(self):
        self._transacoes = {}

    @property
    def transacoes(self):
        return self._transacoes
    

    # Adiciona uma transação a lista de transações do historico
    def adicionar_transacao(self, transacao):
        self._transacoes[dt.datetime.now()] = transacao


    # Dois métodos passados pelo professor para exibir os dados importantes:
    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Transacao(ABC):
    @abstractmethod
    def registrar(self):
        pass


class Deposito:
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        status_transacao = conta.depositar(self._valor)

        if status_transacao:
            conta.historico.adicionar_transacao(self)
            return True
        else:
            return False


class Saque:
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        status_transacao = conta.sacar(self._valor)

        if status_transacao:
            conta.historico.adicionar_transacao(self)
            return True
        else:
            return False


class Conta(ContaCorrente):
    def __init__(self, cliente, numero):
        super().__init__()
        self._cliente = cliente
        self._numero = numero
        self._historico = Historico()
        self._agencia = '0001'
        self._saldo = 0.0
          
    @property
    def saldo(self):
        return self._saldo
    

    @property
    def historico(self):
        return self._historico
    
    @property
    def numero(self):
        return self._numero
    

    # Classe para criar uma conta
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    

    # Retorna verdadeiro ou falso se for possível sacar/depositar
    def sacar(self, valor):
        valor = abs(valor)
        # Validar se tem saldo suficiente pra sacar o valor desejado
        if self._saldo >= valor:
            transacoes_hoje = {data: transacao for data, transacao in self._historico.transacoes.items() if (data.date() == dt.date.today())}
            # Validar se o limite de transações diários não foi excedido
            if len(transacoes_hoje) < self._limite_transacoes:
                saques_hoje = {data: transacao for data, transacao in self._historico.transacoes.items() if (data.date() == dt.date.today()) and type(transacao) == Saque}
                # Validar se o limite de saques diarios não foi excedido
                if len(saques_hoje) < self._limite_saques:
                    if valor <= self._limite:
                        # Se todas as condições forem atingidas retorna true e subtrai o valor  sacado do saldo
                        self._saldo -= valor

                        return True  
        return False
    

    def depositar(self, valor):
        transacoes_hoje = {data: transacao for data, transacao in self._historico.transacoes.items() if (data.date() == dt.date.today())}
        # Valida se o limite de transações diarios não foi excedido
        if (valor > 0) and (len(transacoes_hoje) < self._limite_transacoes):
            self._saldo += valor
            return True    
        return False


# Decorador para criar Log 
def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Abrindo o arquivo no modo de escrever na primeira linha em branco
        with open('log.txt', 'a') as arquivo:
            # Escrevendo as informações necessárias:
            arquivo.write(
                f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. Retornou {resultado}\n"
            )
        return resultado

    return envelope


# Parte do menu:
def menu():
    clientes = {}
    contas = {}

    @log_transacao
    def criar_cliente(clientes):
        '''Solicita os dados e depois instancia um objeto do tipo Cliente, que é adicionado ao dicionario de clientes
        composição: nome, data_nascimento, cpf, endereço{logradouro, bairro, cidade/sigla Estado}, cpf deve ser unico'''

        try:
            cpf = int(input('Digite o cpf (somente números) do cliente: '))

            
            if cpf not in clientes.keys():
                nome = input('Digite o nome: ')
                data_nascimento = input('Digite a data de Nascimento: ')
                logradouro = input('Digite a rua: ')
                bairro = input('Digite o bairro: ')
                cidade = input('Digite a cidade: ')
                estado = input('Digite a sigla do estado: ')
                endereco = f'{logradouro}, {bairro}, {cidade}/{estado}'

                clientes[cpf] = Cliente.criar_cliente(cpf, nome, data_nascimento, endereco)

                print('Cliente cadastrado com sucesso!\n')
            else:
                print('CPF já cadastrado')
        except:
            print('CPF inválido')

    @log_transacao
    def criar_conta(clientes, contas):
        '''Criar Conta Corrente
        composição: agencia = 0001, numero da conta = sequencia=1, usuario {cada usuario pode ter mais de uma conta} uma conta tem apenas 1 usuario'''


        try:
            cpf = int(input('Digite o CPF: '))
            
            if cpf in clientes.keys():

                ultima_conta_criada = max(contas.keys(), default=0)
                num_conta = ultima_conta_criada + 1
                contas[num_conta] = Conta.nova_conta(clientes[cpf], num_conta)
                clientes[cpf].adicionar_conta(contas[num_conta])
    
                print('Conta cadastrada com sucesso!\n')
            else:
                print('CPF inválido / Cliente não cadastrado\n')
        except:
            print('CPF inválido / Cliente não cadastrado\n')

    @log_transacao
    def depositar(clientes):
        '''Depositar, recebe a lista de clientes, solicita cpf e número de conta para o usuario, se a conta for encontrada dentro do usuario pede o valor e conclui a transação'''
        
        try:
            cpf = int(input('Digite o CPF: '))
            
            if cpf in clientes.keys():
                try:
                    print('Agencia 0001')
                    conta_procurada = int(input('Digite o número da conta: '))
                    contas_do_cpf = clientes[cpf].contas
                    conta_do_usuario = next(conta for conta in contas_do_cpf if conta.numero == conta_procurada)

                    try:
                        valor_deposito = float(input('Digite o valor do deposito: '))
                        deposito = Deposito(valor_deposito)
                        if deposito.registrar(conta_do_usuario):
                            print('\nDepósito realizado com sucesso!\n')
                        else:
                            print('Não foi possível concluir a transação, por gentileza validar o extrato')
                            print('É permitido realizar apenas 10 transações por dia, 3 saques diários no valor de R$500.00')
                    except:
                        print('\nValor inválido, transação não concluida\n')
                except:
                    print('Número de conta inválido')
        except:
            print('CPF inválido/ Cliente não cadastrado')

    @log_transacao
    def sacar(clientes):
        '''Sacar, recebe a lista de clientes, solicita cpf e número de conta
        para o usuario, se a conta for encontrada dentro do usuario pede o 
        valor e conclui a transação'''

        try:
            cpf = int(input('Digite o CPF: '))

            if cpf in clientes.keys():
                try:
                    print('Agencia 0001')
                    conta_procurada = int(input('Digite o número da conta: '))
                    contas_do_cpf = clientes[cpf].contas
                    conta_do_usuario = next(conta for conta in contas_do_cpf if conta.numero == conta_procurada)

                    try:
                        valor_saque = float(input('Digite o valor do saque: '))
                        saque = Saque(valor_saque)
                        if saque.registrar(conta_do_usuario):
                            print('\nSaque realizado com sucesso!\n')
                            print(f'Novo Saldo R${conta_do_usuario.saldo:.2f}')
                        else:
                            print('Não foi possível concluir a transação, por',
                                  'gentileza validar o extrato')
                            print('É permitido realizar apenas 10 transações',
                                  'por dia, 3 saques diários no valor de ',
                                  'R$500.00')
                    except Exception:
                        print('\nValor inválido, transação não concluída\n')
                except Exception:
                    print('Número de conta inválido')
        except Exception:
            print('CPF inválido/ Cliente não cadastrado')

    @log_transacao
    def visualizar_extrato(clientes):
        '''Deve listar todos os depósitos e saques realizados na conta e 
        no final exibir o salto atual. Se não tiverem movimentação exibir
        "Não foram realizadas movimentações".
        Os valores devem ser exibidos "R$####.##"'''

        try:
            cpf = int(input('Digite o CPF: '))

            if cpf in clientes.keys():
                try:
                    print('Agencia 0001')
                    conta_procurada = int(input('Digite o número da conta: '))
                    contas_do_cpf = clientes[cpf].contas
                    conta_do_usuario = next(conta for conta in contas_do_cpf
                                            if conta.numero == conta_procurada)

                    transacoes = conta_do_usuario.historico.transacoes
                    if conta_do_usuario.saldo > 0:
                        for data, transacao in transacoes.items():
                            print(f'{data.strftime("%d/%m/%Y %H:%M:%S")} -',
                                  f'{transacao.__class__.__name__} - ',
                                  f'R${transacao._valor:.2f}')
                        print(f'Saldo: R${conta_do_usuario.saldo:.2f}\n')
                    else:
                        print('Nenhuma transação realizada até o momento.\n')
                except Exception:
                    print('Número de conta inválido')
        except Exception:
            print('CPF inválido/ Cliente não cadastrado')

    while True:
        opcao = input('''Digite a opção desejada:
        1 - Sacar
        2 - Depositar
        3 - Visualizar extrato
        4 - Novo cliente
        5 - Nova conta
        0 - Sair\n''')

        if opcao == '1':
            sacar(clientes)
        elif opcao == '2':
            depositar(clientes)
        elif opcao == '3':
            visualizar_extrato(clientes)
        elif opcao == '4':
            criar_cliente(clientes)
        elif opcao == '5':
            criar_conta(clientes, contas)
        elif opcao == '0':
            print('\nObrigada por utilizar nossos serviços\n')
            break
        else:
            print('\nOpção inválida, tente novamente\n')


# Executando a função menu:

menu()
