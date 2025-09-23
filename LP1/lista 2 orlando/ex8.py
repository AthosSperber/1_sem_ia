numero = int(input("Digite um número: "))

triangulo = []
x = 1

while x <= numero:
    triangulo.append(x)
    print(triangulo)
    x += 1


for i in range(numero):
    triangulo.append(x)
    print(triangulo)
    x += 1