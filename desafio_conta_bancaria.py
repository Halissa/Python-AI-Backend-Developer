saldo = 0

while True:
    opcao = input('''Digite a opcao desejada:
    1 - Sacar
    2 - Depositar
    3 - Visualizar extrato
    0 - Sair\n''')
    
    if opcao == '0':
        print('\nObrigado por utilizar nossos serviços.\n')
        break
    elif opcao == '1':
    #Sacar
        print('\nimplementar Saque\n')
    elif opcao == '2':
        '''Depositar: A única exigencia é que o usuário não pode fazer depositos 
        negativos, porém a quantidade e valor são ilimitados'''
        while True:
            deposito = input('\n Digite o valor do depósito: \n')
            if deposito.isdecimal():
                if float(deposito) > 0:
                    saldo += float(deposito)
                    break
            print('\nValor inválido, tente novamente.\n')

    elif opcao == '3':
    #Visualizar extrato
        print('\nimplementar Visualizar extrato\n')
        print(f'Saldo: {saldo}')
    else:
        print('\nOpção invalida, tente novamente.\n')
