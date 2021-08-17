def get_price(item):
    if item == "burger":
        return 5
    elif item == "fries":
        return 3
    elif item == "coke":
        return 2
    elif item == "nuggets":
        return 6

    return 0


class Order:

    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item):
        self.total += get_price(item)
        self.items.append(item)

    def get_total(self):
        return self.total
