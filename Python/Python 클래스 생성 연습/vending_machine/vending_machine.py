class VendingMachine:
    def __init__(self, items, payment):
        self.items = items
        self.payment = payment
    def show_items(self):
        for i, item in enumerate(self.items):
            print(f"{i}번 물품 {item.name}의 개수 : {item.count}")
    def change_items(self, items):
        self.items = items
    def add_items(self, num):
        for i in len(self.items):
            self.items[i].count += num
    def buy_item(self, item_number, choice_payment, input_money):
        if self.items[item_number].count > 0:
            if choice_payment == "cash":
                self.payment.cash_payment(input_money, self.items[item_number].price)
            elif choice_payment == "card":
                self.payment.card_payment(self.items[item_number].price)
            else:
                print("결제 수단이 잘못되었습니다.")
        else:
            print("구매하려는 물품의 재고가 없습니다.")