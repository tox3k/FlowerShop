ProductCard_Category = {
    1: 'Цветы штучные',
    2: "Букеты",
    3: 'Открытки',
    4: 'Нет категории'
}


class ProductCard:
    def __init__(self, name, category=4, description='', available_count=100):
        self.name = name
        self.category = category
        self.description = description
        self.available_count = available_count


class ProductCardList:
    def __init__(self):
        self.products = dict[int, ProductCard]
        cnt = 0

    def append(self, item):
        if item not in self.products:
            self.products[self.cnt] = item
        else:
            return ValueError()

    def pop(self, id):
        product = self.products[id]
        self.products.pop(id)
        return product

    def get(self, id):
        return self.products[id]

    def items(self):
        res = []
        for k, v in self.products.items():
            res.append(v)
        return res
