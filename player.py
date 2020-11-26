product_name = {
0: "rock",
1: "clay",
2: "wood",
3: "sheep",
4: "hay"
}

class Player:
    def __init__(self, color):
        self.color = color
        self.turn = 0
        self.available_buildings = {"village": 5, "town": 4, "road": 15}
        self.built = {"village": 0, "town": 0, "road": 0}
        self.products = {"rock": 0, "clay": 0, "wood": 0, "sheep": 0, "hay": 0}
        self.possible_trades = {"rock": 3, "clay": 3, "wood": 3, "sheep": 3, "hay": 3}
        self.longest_road = 0
        self.largest_army = 0
        self.development_cards = {"knight": 0, "victory_point": 0}

    @property
    def score(self):
        score = 0
        score += self.built["village"]
        score += self.built["town"] * 2
        score += self.development_cards["victory_point"]
        score += self.longest_road * 2
        score += self.largest_army * 2
        return score

    @property
    def cards_total(self):
        total = 0
        for product in self.products:
            total += self.products[product]
        return total

    def change(self, product, change_to):
        if self.products[product] >= self.possible_trades[product]:
            self.products[product] -= self.possible_trades[product]
            self.products[change_to] += 1

    def gain(self, product, amount=1):
        if product != 9:
            if type(product) is int:
                product = product_name[product]
            self.products[product] += amount

    def give(self, product, amount=1):
        if type(product) is int:
            product = product_name[product]
        self.products[product] -= amount

    def remove_resources(self, resources):
        for resource_name in resources:
            if self.products[resource_name] < resources[resource_name]:
                return False
        for resource_name in resources:
            self.products[resource_name] -= resources[resource_name]

    def rate_trade_request(self, resource):
        pass

    def response_to_trade_request(self, response):
        return response
