import datetime as dt

extrato = {}

def sacar(extrato_saque):
    '''Limite de 3 saques/dia de no máximo R$500, se o usuario
    não tiver saldo informar" Não foi possível concluir o saque
    por falta de saldo" '''
    saques_dia = 0
    saldo = 0
    for data, valor in extrato_saque.items():
        #somar toda a movimentação para saber o saldo atual:
        saldo += valor
        # valida se as datas do extrato são == hoje e o valor é < 0
        if (data.date() == dt.date.today()) and (valor < 0.0):
            saques_dia +=1

    if saques_dia < 3:
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


def depositar(extrato_deposito):
    '''Depositar: A única exigencia é que o usuário não pode fazer
    depositos negativos, porém a quantidade e valor são ilimitados'''
    try:
        valor_deposito = float(input('Digite o valor do deposito: '))
        if(valor_deposito) <= 0.0:
            print('\nValor invalido, transação não concluida\n')
        else:
            extrato_deposito[dt.datetime.now()] = valor_deposito
            print('\nDeposito realizado com sucesso!\n')
    except:
        print('\nValor invalido, transação não concluida\n')


def visualizar_extrato(extrato_visualizar):
    '''Deve listar todos os depósitos e saques realizados na conta e 
    no final exibir o salto atual. Se não tiverem movimentação exibir
    "Não foram realizadas movimentações".
    Os valores devem ser exibidos "R$####.##"'''
    saldo = 0
    print('\n*** Extrato bancário ***')
    if extrato_visualizar == {}:
        print('Não foram realizadas movimentações')
    else:
        for data, valor in extrato_visualizar.items():
            saldo +=valor
            if valor < 0:
                tipo = 'Saque'
            else:
                tipo = 'Deposito'
            print(f'{tipo}: {data.date()} ... R${valor:.2f}')
    print(f'Sado Atual:R${saldo:.2f}\n')


while True:
    opcao = input('''Digite a opção desejada:
    1 - Sacar
    2 - Depositar
    3 - Visualizar extrato
    0 - Sair\n''')
    
    if opcao == '1':
        sacar(extrato)
    elif opcao == '2':
        depositar(extrato)
    elif opcao == '3':
        visualizar_extrato(extrato)
    elif opcao == '0':
        print('\nObrigada por utilizar nossos serviços\n')
        break
    else:
        print('\nOpção inválida, tente novamente\n')
    