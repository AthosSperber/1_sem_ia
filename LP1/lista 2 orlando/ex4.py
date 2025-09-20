numero = []
pares = []
impares = []

for i in range(10):
    n = int(input("Digite o {} número: ".format(i + 1)))
    numero.append(n)


for x in numero:
    if x % 2 == 0:
        pares.append(x)
    else:
        impares.append(x)

print(f"Quantidade de números pares: {len(pares)}")
print(f"Quantidade de números ímpares: {len(impares)}")
print(f"Soma dos números pares: {sum(pares)}")