qnt = int(input("quantas notas deseja informar?"))
x = 0
soma = 0
y = 0
lista = [] 

while x < qnt:
    lista.append(float(input('Qual é a {} nota que voce quer lançar?'.format(x))))
    x = x+1

while y < len(lista):
    soma = soma + lista[y]
    y += 1 

media = soma/y
print('Média do aluno: {}'.format(media))

if media >= 7:
    print('O Aluno foi aprovado!')
else: print('O Aluno NÃO foi aprovado!')