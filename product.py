class Product:
    def __init__(self, id,  name, description, price, count, image) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.count = count
        self.image = image
    
    def __str__(self) -> str:
        return self.name + self.description + 'Price ' + str(self.price) + 'Count ' +  str(self.count)