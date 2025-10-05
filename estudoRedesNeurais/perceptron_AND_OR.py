import math

# ==========================
# Função de ativação
# ==========================
def activation(sum_):
    """Função degrau: retorna 1 se soma >= 0, senão 0"""
    if sum_ >= 0:
        return 1
    else:
        return 0

# ==========================
# Função de treino do perceptron
# ==========================
def train_perceptron(training_data, learning_rate=0.1, epochs=20):
    """
    Treina um perceptron simples em cima de uma tabela verdade.
    """
    # Inicialização dos pesos e bias
    weights = [0.5, 0.5]   # um peso para cada entrada
    bias_weight = 0.5
    bias = 1               # constante do bias

    # Loop de épocas
    for epoch in range(epochs):
        print(f"\n==== Época {epoch+1} ====")
        error_total = 0

        # Loop pelos exemplos de treino
        for idx in range(len(training_data)):
            inputs = training_data[idx][0]   # pega as entradas (ex: [0,1])
            desired = training_data[idx][1] # pega a saída desejada

            # Passo 1: soma ponderada
            weighted_sum = 0
            for i in range(len(weights)):
                weighted_sum += inputs[i] * weights[i]
            weighted_sum += bias * bias_weight

            # Passo 2: saída da rede
            output = activation(weighted_sum)

            # Passo 3: erro
            error = desired - output
            error_total += abs(error)

            # Passo 4: atualização dos pesos
            for i in range(len(weights)):
                weights[i] = weights[i] + (learning_rate * error * inputs[i])

            # Atualização do bias
            bias_weight = bias_weight + (learning_rate * error * bias)

            # Debug de cada exemplo
            print(f"Inputs: {inputs}, Saída: {output}, Desejado: {desired}, Erro: {error}")

        # Se não houver erro na época, o treino para
        if error_total == 0:
            print("\n✅ Rede aprendeu!")
            break

    # Resultado final
    print(f"\nPesos finais: {weights}, Bias: {bias_weight}\n")
    return weights, bias_weight

# ==========================
# Dados de treino
# ==========================
AND = [
    ([0, 0], 0),
    ([0, 1], 0),
    ([1, 0], 0),
    ([1, 1], 1)
]

OR = [
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 1)
]

# ==========================
# Execução
# ==========================
print("### Treinando AND ###")
train_perceptron(AND)

print("### Treinando OR ###")
train_perceptron(OR)
