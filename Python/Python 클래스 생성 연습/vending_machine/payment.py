class Payment:
    def cash_calculate(self, input_money, payment_money):
        change = input_money - payment_money
        units = [10000, 5000, 1000, 500, 100]
        result = {}

        for unit in units:
            count = change // unit
            result[unit] = count
            change %= unit
        
        print(f"거스름돈은 ", end="")

        for unit, count in result.items():
            if count > 0:
                print(f"{unit}원: {count}개, ", end="")
        print("입니다.")

    def cash_payment(self, input_money, payment_money):
        print(f"총 {input_money}원 받았습니다.")
        print(f"현금 결제 {payment_money}원 결제 완료되었습니다.")
        self.cash_calculate(input_money, payment_money)
    
    def card_payment(self, money):
        print(f"카드 결제 {money}원 결제 완료되었습니다.")
        