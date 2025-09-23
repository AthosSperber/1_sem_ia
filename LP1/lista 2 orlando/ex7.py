altura = int(input("Digite a altura: "))
largura = int(input("Digite a largura: "))

for i in range(altura):
    for j in range(largura):
        print("*", end="")  # end evita a quebra de linha
    print()
