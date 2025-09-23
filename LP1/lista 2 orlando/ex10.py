numero = int(input("Digite um número: "))
listaprimos = []

for i in range(1, numero + 1):
    primo = 1
    for j in range(2, i):
        if i % j == 0:
            primo = 0
    
    if primo == 1:
        listaprimos.append(i)

print(listaprimos)