import math

input = 1               ## entrada
output_desired = 0      ## saída desejada    

input_weight = 0.5      ## peso da entrada
learning_rate = 0.1     ## taxa de aprendizado

def activition_function(sum): ## função de ativação 
    if sum >= 0:
        return 1
    else:
        return 0

print(f'Input (entrada): {input} - Input Weight (peso): {input_weight}')


error = math.inf
interations = 0

bias = 1        ## bias da rede neural (termo de ajuste da função de ativação) 
bias_weight = 0.5

while not error == 0:
    interations += 1
    print(f'\n####### Interation: {interations}')
    print(f'Input Weight (peso): {input_weight}')

    sum = (input * input_weight) + (bias * bias_weight)  ## soma ponderada

    output = activition_function(sum)       ## saída da rede neural

    print(f'Output (saída): {output} - Desired Output (saída desejada): {output_desired}')

    error = output_desired - output

    print(f'Error: {error}')

    if error != 0:
        input_weight = input_weight + (learning_rate * error * input)
        bias_weight = bias_weight + (learning_rate * error * bias)
        print(f'New Input Weight (novo peso): {input_weight}')
print(f"A rede aprendeu!")