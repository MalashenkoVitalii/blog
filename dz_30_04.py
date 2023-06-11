# створити дві функції з довільними аргументами, створити клас, в класі має бути кілька атрибутів і кілька методів

def suma(*args):
    print(sum(args))
    print(args)
    list_sum = []
    for i in args:
        list_sum.append(i)
    print(sum(list_sum))


suma(4, 6, 8, 2)


n = int(input('Input number '))

fact_func = 1


def fact(n, fact_func):
    for num in range(1,n+1):
        fact_func = num*fact_func
    print(fact_func)


fact(n, fact_func)


class Shop():
    def __init__(self, balance):
        self.balance = balance

    basket = []

    def add_to_basket(self, *args, basket):
        for i in args:
            basket.append(i)
        print(basket, 'in basket')

    def buy(self, balance):
        price = int(input('Price: '))
        balance = balance - price
        print('Balance now: ', balance)


shop = Shop(balance=50)
shop.buy(balance=50)
shop.add_to_basket('cherry', 'banana', 'apple', basket=[])
