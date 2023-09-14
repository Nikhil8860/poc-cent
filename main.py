fruits = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
price = [1.25, 0.75, 0.50, 2.00, 3.50, 4.00, 1.75]

fruits_price = [(i, j) for i, j in zip(fruits, price) if 1 < j <= 3]
print(sorted(fruits_price, key=lambda x:x[1], reverse=True))
