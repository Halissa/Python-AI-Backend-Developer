import datetime as dt

usuarios = []


def criar_usuario(usuarios):
    '''Criar Usuário
    composição: nome, data_nascimento, cpf, endereço{logradouro, bairro, cidade/sigla Estado}, cpf deve ser unico'''

    try:
        cpf = int(input('Digite o cpf (somente números) do usuario: '))

        validar_cpf = next((usuario for usuario in usuarios if usuario['cpf']==cpf), None)

        if validar_cpf == None:
            nome = input('Digite o nome: ')
            data_nascimento = input('Digite a data de Nascimento: ')
            logradouro = input('Digite a rua: ')
            bairro = input('Digite o bairro: ')
            cidade = input('Digite a cidade: ')
            estado = input('Digite a sigla do estado: ')

            usuarios.append({'cpf': cpf, 'data_nascimento': data_nascimento, 'endereco': f'{logradouro}, {bairro}, {cidade}/{estado}', 'contas':[]})
        else:
            print('CPF já cadastrado')
    except:
        print('CPF inválido')
        

def criar_conta(usuarios):
    '''Criar Conta Corrente
    composição: agencia = 0001, numero da conta = sequencia=00001, usuario {cada usuario pode ter mais de uma conta} uma conta tem apenas 1 usuario'''

    try:
        cpf_procurado = int(input('Digite o CPF: '))
        usuario = next(usuario for usuario in usuarios if usuario['cpf']==cpf_procurado)

        ultima_conta_criada = max((conta['conta'] for usuario in usuarios for conta in usuario['contas']), default=0)

        agencia = '0001'
        conta = ultima_conta_criada + 1

        usuario['contas'].append({'agencia':'0001', 'conta': conta, 'movimentacoes':{}})

    except:
        print('CPF inválido / Usuario não cadastrado')


def sacar(usuarios):
    '''Limite de 3 saques/dia de no máximo R$500, se o usuario
    não tiver saldo informar" Não foi possível concluir o saque
    por falta de saldo" '''

    try:
        cpf_procurado = int(input('Digite o CPF: '))
        usuario = next(usuario for usuario in usuarios if usuario['cpf']==cpf_procurado)
        contas_do_usuario = usuario['contas']

        try:
            print('Agencia 0001')
            conta_procurada = int(input('Digite o número da conta: '))

            conta_do_usuario = next(conta for conta in contas_do_usuario if conta['conta']==conta_procurada)

            extrato_saque = conta_do_usuario['movimentacoes']

            if extrato_saque == {}:
                saldo = 0
                saques_diarios = []
            else:
                saldo = sum(extrato_saque.values())
                # Filtra os saques realizados hoje em um dicionario:
                saques_diarios = {data: valor for data, valor in extrato_saque.items() if (data.date() == dt.date.today()) and (valor < 0)}


            if len(saques_diarios) < 3:
                try:
                    valor_saque = abs(float(input('Digite o valor do saque (máx R$500.00): ')))
                    if valor_saque > 500.00:
                        print('\nValor do saque maior que o limite por transação\n')
                    elif valor_saque > saldo:
                        print(f'\nNão foi possível concluir o saque por falta de saldo. Valor disponível: {saldo:.2f}\n')
                    else:
                        extrato_saque[dt.datetime.now()] = -valor_saque
                        print('\nSaque realizado com sucesso!\n')
                except:
                    print('\nValor invalido, transação não concluida\n')
            else:
                print('\nLimite de saques diário já atingido\n')
        except:
            print('Número de conta inválido')
    except:
        print('CPF inválido / Usuario não cadastrado')


def depositar(usuarios):
    '''Depositar: A única exigencia é que o usuário não pode fazer
    depositos negativos, porém a quantidade e valor são ilimitados'''
    try:
        cpf_procurado = int(input('Digite o CPF: '))
        usuario = next(usuario for usuario in usuarios if usuario['cpf']==cpf_procurado)
        contas_do_usuario = usuario['contas']

        try:
            print('Agencia 0001')
            conta_procurada = int(input('Digite o número da conta: '))
            conta_do_usuario = next(conta for conta in contas_do_usuario if conta['conta']==conta_procurada)

            extrato_deposito = conta_do_usuario['movimentacoes']

            try:
                valor_deposito = float(input('Digite o valor do deposito: '))
                if(valor_deposito) <= 0:
                    print('\nValor invalido, transação não concluida\n')
                else:
                    extrato_deposito[dt.datetime.now()] = valor_deposito
                    print('\nDeposito realizado com sucesso!\n')
            except:
                print('\nValor invalido, transação não concluida\n')
        except:
            print('Número de conta inválido')
    except:
        print('CPF inválido / Usuario não cadastrado')


def visualizar_extrato(usuarios):
    '''Deve listar todos os depósitos e saques realizados na conta e 
    no final exibir o salto atual. Se não tiverem movimentação exibir
    "Não foram realizadas movimentações".
    Os valores devem ser exibidos "R$####.##"'''

    try:
        cpf_procurado = int(input('Digite o CPF: '))
        usuario = next(usuario for usuario in usuarios if usuario['cpf']==cpf_procurado)
        contas_do_usuario = usuario['contas']

        try:
            print('Agencia 0001')
            conta_procurada = int(input('Digite o número da conta: '))

            conta_do_usuario = next(conta for conta in contas_do_usuario if conta['conta']==conta_procurada)

            extrato_visualizar = conta_do_usuario['movimentacoes']

            if extrato_visualizar == {}:
                saldo = 0
            else:
                saldo = sum(extrato_visualizar.values())
            
            print('\n*** Extrato bancário ***')
            if extrato_visualizar == {}:
                print('Não foram realizadas movimentações')
            else:
                for data, valor in extrato_visualizar.items():
                    if valor < 0:
                        tipo = 'Saque'
                    else:
                        tipo = 'Deposito'
                    print(f'{tipo}: {data.strftime("%d/%m/%Y")} ... R${valor:.2f}')
            print(f'Sado Atual:R${saldo:.2f}\n')



        except:
            print('Número de conta inválido')

    except:
        print('CPF inválido / Usuario não cadastrado')


while True:
    opcao = input('''Digite a opção desejada:
    1 - Sacar
    2 - Depositar
    3 - Visualizar extrato
    4 - Novo usuario
    5 - Nova conta
    6 - Listar contas
    0 - Sair\n''')
    
    if opcao == '1':
        sacar(usuarios)
    elif opcao == '2':
        depositar(usuarios)
    elif opcao == '3':
        visualizar_extrato(usuarios)
    elif opcao == '4':
        criar_usuario(usuarios)
    elif opcao == '5':
        criar_conta(usuarios)
    elif opcao == '0':
        print('\nObrigada por utilizar nossos serviços\n')
        break
    else:
        print('\nOpção inválida, tente novamente\n')
    