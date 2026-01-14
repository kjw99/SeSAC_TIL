from payment import Payment
from vending_machine import VendingMachine
from vend_item import VendItem

lst = [
    VendItem("콜라", 10, 1200), 
    VendItem("2프로", 10, 1000), 
    VendItem("파워에이드", 10, 1300)
    ]

vend = VendingMachine(lst, Payment())

vend.show_items()
vend.buy_item(0, "card", 10000)
