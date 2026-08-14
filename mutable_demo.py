class BuggyCart:
    items = []

    def __init__(self, owner):
        self.owner = owner

    def add_item(self, item):
        self.items.append(item)


class FixedCart:
    def __init__(self, owner):
        self.owner = owner
        self.items = []

    def add_item(self, item):
        self.items.append(item)


if __name__ == "__main__":
    cart1 = BuggyCart("Alice")
    cart2 = BuggyCart("Bob")
    cart1.add_item("apple")
    print(cart2.items)

    fixed1 = FixedCart("Alice")
    fixed2 = FixedCart("Bob")
    fixed1.add_item("apple")
    print(fixed2.items)