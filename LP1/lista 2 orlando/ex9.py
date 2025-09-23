numero = int(input("Digite um número: "))

for i in range(numero, 0, -1):
    linha = []                   # cria uma nova lista para cada linha
    for j in range(1, i + 1):
        linha.append(j)
    print(linha)