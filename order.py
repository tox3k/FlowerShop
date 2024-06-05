class Order:
    def __init__(self, id, client, phone, price, timestamp, products) -> None:
        self.id: int = id
        self.client: str = client
        self.phone: str = phone
        self.price: str = price
        self.timestamp: str = timestamp
        self.products: list = products
    
    
    def __str__(self) -> str:
        return f'{self.client}\t{self.price}'