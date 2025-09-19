import random 
n_secreto = random.randint(1, 50)

print('??_Tente descobrir o número secreto_??')
n_tentativa = int(input('O número está entre 1 e 50...'))

while n_tentativa != n_secreto:
    
    if n_tentativa > n_secreto:
        print("o numero secreto é menor")
    if n_tentativa < n_secreto:
        print("o numero secreto é maior")

    n_tentativa = int(input(':'))
else: print ("Voce acertou!! o numero secreto é {}".format(n_secreto))

