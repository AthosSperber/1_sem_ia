y = 1
while y <= 10:
    x = 1                         # precisa reiniciar o x a cada novo y
    while x <= 10:
        print(f"{y} x {x} = {y * x}")
        x += 1
    y += 1