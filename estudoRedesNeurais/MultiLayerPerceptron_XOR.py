# porta logica XOR usando MLP simples

import math
import random

    ##Funções auxiliares


# Função de ativação (sigmóide para suavizar a saída entre 0 e 1)
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# Derivada da sigmóide (usada no backpropagation)
def sigmoid_derivative(x):
    return x * (1 - x)


    ##Dados de treino - XOR

training_data = [
    ([0, 0], [0]),
    ([0, 1], [1]),
    ([1, 0], [1]),
    ([1, 1], [0])
]


    ##Parâmetros da rede

input_neurons = 2     # número de entradas (X1, X2)
hidden_neurons = 2    # número de neurônios na camada oculta
output_neurons = 1    # saída (resultado do XOR)

learning_rate = 0.5
epochs = 10000        # número de vezes que a rede vai treinar


    ##Inicialização dos pesos

# Pesos da camada de entrada → camada oculta
# matriz 2x2 (2 entradas × 2 neurônios ocultos)
weights_input_hidden = [[random.uniform(-1, 1) for _ in range(hidden_neurons)] for _ in range(input_neurons)]

# Pesos da camada oculta → saída
# matriz 2x1 (2 neurônios ocultos × 1 saída)
weights_hidden_output = [[random.uniform(-1, 1) for _ in range(output_neurons)] for _ in range(hidden_neurons)]

# Bias (um para cada neurônio oculto e um para a saída)
bias_hidden = [random.uniform(-1, 1) for _ in range(hidden_neurons)]
bias_output = [random.uniform(-1, 1) for _ in range(output_neurons)]


    ##Treinamento (Backpropagation)

for epoch in range(epochs):
    total_error = 0

    for inputs, desired in training_data:
        # ----------- Feedforward -----------

        # Camada oculta
        hidden_layer = []
        for j in range(hidden_neurons):
            sum_hidden = sum(inputs[i] * weights_input_hidden[i][j] for i in range(input_neurons)) + bias_hidden[j]
            hidden_output = sigmoid(sum_hidden)
            hidden_layer.append(hidden_output)

        # Camada de saída
        final_layer = []
        for k in range(output_neurons):
            sum_output = sum(hidden_layer[j] * weights_hidden_output[j][k] for j in range(hidden_neurons)) + bias_output[k]
            final_output = sigmoid(sum_output)
            final_layer.append(final_output)

        # ----------- Cálculo do erro -----------
        output_errors = [desired[k] - final_layer[k] for k in range(output_neurons)]
        total_error += sum(e**2 for e in output_errors)  # erro quadrático

        # ----------- Backpropagation -----------

        # Erro da saída → delta
        output_deltas = [output_errors[k] * sigmoid_derivative(final_layer[k]) for k in range(output_neurons)]

        # Erro da camada oculta
        hidden_errors = [0] * hidden_neurons
        for j in range(hidden_neurons):
            hidden_errors[j] = sum(output_deltas[k] * weights_hidden_output[j][k] for k in range(output_neurons))

        # Delta da camada oculta
        hidden_deltas = [hidden_errors[j] * sigmoid_derivative(hidden_layer[j]) for j in range(hidden_neurons)]

        # ----------- Atualização dos pesos -----------

        # Atualiza pesos da camada oculta → saída
        for j in range(hidden_neurons):
            for k in range(output_neurons):
                weights_hidden_output[j][k] += learning_rate * output_deltas[k] * hidden_layer[j]

        # Atualiza pesos da entrada → camada oculta
        for i in range(input_neurons):
            for j in range(hidden_neurons):
                weights_input_hidden[i][j] += learning_rate * hidden_deltas[j] * inputs[i]

        # Atualiza bias
        for k in range(output_neurons):
            bias_output[k] += learning_rate * output_deltas[k]
        for j in range(hidden_neurons):
            bias_hidden[j] += learning_rate * hidden_deltas[j]

    # Mostrar progresso a cada 1000 épocas
    if epoch % 1000 == 0:
        print(f"Época {epoch}, Erro total: {total_error:.4f}")


##Testando a rede


print("\n### Testando a rede treinada ###")
for inputs, desired in training_data:
    # Feedforward novamente
    hidden_layer = []
    for j in range(hidden_neurons):
        soma = sum(inputs[i] * weights_input_hidden[i][j] for i in range(input_neurons)) + bias_hidden[j]
        hidden_layer.append(sigmoid(soma))

    final_layer = []
    for k in range(output_neurons):
        soma = sum(hidden_layer[j] * weights_hidden_output[j][k] for j in range(hidden_neurons)) + bias_output[k]
        final_layer.append(sigmoid(soma))

    print(f"Entrada: {inputs} → Saída prevista: {final_layer[0]:.4f} | Desejado: {desired[0]}")
