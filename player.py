product_name = {
0: "rock",
1: "clay",
2: "wood",
3: "sheep",
4: "hay"
}


class Player:
    def __init__(self, color, ai=False):
        self.color = color
        self.ai = ai
        self.turn = 0
        self.available_buildings = {"village": 5, "town": 4, "road": 15}
        self.built = {"village": 0, "town": 0, "road": 0}
        self.products = {"wood": 0, "clay": 0, "sheep": 0, "hay": 0, "rock": 0}
        self.possible_trades = {"wood": 3, "clay": 3, "sheep": 3, "hay": 3, "rock": 3}
        self.development_cards = {"knight": 0, "victory_point": 0}

    @property
    def score(self):
        score = 0
        score += self.built["village"]
        score += self.built["town"] * 2
        score += self.development_cards["victory_point"]
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

    def can_afford(self, price):
        for resource in price:
            if self.products[resource] < price[resource]:
                return False
        return True

    def can_change(self, product):
        if self.products[product] >= self.possible_trades[product]:
            return True
        return False

    def player_json(self):
        json = {
                    "color": self.color,
                    "av_buildings": self.available_buildings,
                     "built": self.built,
                     "products": self.products,
                     "possible_trades": self.possible_trades,
                     "development_cards": self.development_cards,
                     "score": self.score,
                     "cards_total": self.cards_total,
                     "ai": self.ai
        }
        return json

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.player_json() == other.player_json()

    def __hash__(self):
        return hash(self.color)