numero_produto = 1
lista_compra = []

preço_produto = float(input("Digite o preço do produto {}, para finalizar digite 0:  ".format(numero_produto)))

while preço_produto != 0:
    lista_compra.append(preço_produto)
    numero_produto += 1
    preço_produto = float(input("Digite o preço do produto {}, para finalizar digite 0:  ".format(numero_produto)))


if sum(lista_compra) >= 100:
    desconto = sum(lista_compra) * 0.10
    print("O valor total da compra é R$ {:.2f}, com desconto de R$ {:.2f}, o valor final é R$ {:.2f}".format(sum(lista_compra), desconto, sum(lista_compra) - desconto))
else:
    print("O valor total da compra é R$ {:.2f}, sem desconto".format(sum(lista_compra)))
    