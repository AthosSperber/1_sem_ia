limite = int(input("Digite o número limite: "))
if limite > 0:
    soma = 0
    n = 1
    while soma <= limite:
        soma += n
        n += 1
    print(f"A soma dos números naturais ultrapassou o limite de {limite} com o valor: {soma}, somando de 1 até {n-1}.")
else:
    print("Digite um número positivo.")