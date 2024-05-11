#DESAFIO: Criando um sistema bancário
##Desafio criado pelo Guilherme Arthur de Carvalho / @decarvalhogui / Web.Dio.Me

## O sistema deve permitir realizar 3 saques diários com limite de 500 R$
## O sistema só vai ter 1 usuário para não se preocupar com dados da agência e conta
## Caso o usuário não tenha saldo, o saque deve informar que não será possível sacar o dinheiro por falta de saldo
## O Extrato deve listar todos os depósitos e saques realizados na conta

## Esse é meu primeiro código python, incrementei o "Seja Bem vindo {nome}"" e o "Deseja Realizar Outro Saque ? (s/n)"


menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Saldo
[0] Sair


=> """ 

saldo = 0
limite_saque = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

nome = input("Digite seu nome: ")
print(f"Bem-vindo(a), {nome}!")

while True:
    opcao = input(menu)


########### DEPOSITO ###########
    if opcao == "1":
        print("Seja bem vindo a área de Depósito")
        valor_deposito = float(input("Qual o valor deseja Depositar? "))
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito: R$ {valor_deposito:.2f}\n"
            print(f"Valor depositado: R$ {valor_deposito:.2f}")

        else:
           print(f"Operação falhou! O valor informado é inválido")
           #break

  
########## SAQUE ###############

    elif opcao =="2":
        print("Seja bem vindo a área de Saque")

        if saldo == 0:
            print("Operação falhou! Você não tem saldo disponível para saque.")
       
        else:
         while numero_saques < LIMITE_SAQUES: 
      
            valor_saque = float(input("Qual o valor deseja sacar? "))
            excedeu_saldo = valor_saque > saldo
            excedeu_limite = valor_saque > limite_saque


            if excedeu_saldo:
                print(f"""Operação falhou! Você não tem saldo suficiente
Seu saldo é de {saldo} reais.""")
            
            elif excedeu_limite:
                print(f"O valor de saque excede o limtie de R$ {limite_saque:.2f}. Por favor, tente um valor menor.")
            else:
                saldo -= valor_saque
                extrato += f"Saque: R$ {valor_saque:.2f}\n" 
                print(f"Valor sacado: R$ {valor_saque:.2f}")     
                numero_saques += 1
                outro_saque = input("Deseja realizar outro saque? (s/n) ").lower()
                if outro_saque == "n":
                    break

                    print(f"""Seu saldo final é de {saldo} reais.
Obrigado por usar nossos serviços, volte sempre!""")  
                
        if numero_saques >= LIMITE_SAQUES:       
                print(f"""Você atingitou o limite máximo diário de {LIMITE_SAQUES} saques.
Obrigado por usar nossos serviços, {nome}! Volte sempre!""")
              

####### EXTRATO ##########      
    elif opcao =="3":
        print("\n================== Extrato ================== ")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print(f"\nObrigado por usar nossos serviços, {nome}! Volte sempre!")
        print("\n================== Unstoppable Bank ================== ")

########## SALDO ###########
    elif opcao == "4":
        if saldo >= 0:
            print(f"Seu saldo atual é de R$ {saldo:.2f}")
        else:
            print("Seu saldo atual é de R$ 0.00 (Saldo negativo)")    

########## SAIR ###########
    elif opcao == "0":
        print(f"Obrigado por usar nossos serviços, {nome}! Volte sempre!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")



        





