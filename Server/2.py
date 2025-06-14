def calculate_price(n):
    digits = str(n)
    product = 1
    for digit in digits:
        product *= int(digit)
    return product
n = int(input("Enter the value of N: "))
price = calculate_price(n)
print("Output:", price)