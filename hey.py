import os

class Bank:
    def __init__(self, bankName):
        self.bankName = bankName
        self.atms = []

    def add_atm(self, atm):
        self.atms.append(atm)

class ATM:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.ATMbalance = 100000

    def authenticate(self, card_number, pin):
        return True

class Customer:
    def __init__(self, name, initial_balance, atm):
        self.name = name
        self.balance_file = f"{name.lower()}_balance.txt"
        self.atm = atm
        self.balance = self.read_balance(initial_balance)

    def read_balance(self, initial_balance):
        if os.path.exists(self.balance_file):
            with open(self.balance_file, "r") as file:
                return float(file.readline())
        else:
            return initial_balance

    def update_balance(self, amount):
        with open(self.balance_file, "w") as file:
            file.write(str(self.balance))

    def check_balance(self):
        print(f"------- Your account balance: ${self.balance:.2f} -------")

    def withdraw_cash(self, amount):
        if amount <= self.balance and amount <= self.atm.ATMbalance:
            self.balance -= amount
            self.update_balance(-amount)
            print(f"Withdrawal successful. Remaining balance: ${self.balance}")
        else:
            print("Insufficient funds or ATM does not have enough cash.")

    def deposit_funds(self, amount):
        self.balance += amount
        self.update_balance(amount)
        print(f"Deposit successful. Updated balance: ${self.balance}")

    def getName(self):
        print(f'Welcome {self.name}, We are happy to assist you Today')


class ATMTechnician(ATM):
    def __init__(self, bank_name, technician_id, code):
        super().__init__(bank_name)
        self.technician_id = technician_id
        self.code = code

    def perform_maintenance(self):
        print(f"{self.bank_name} ATM maintenance completed.")

    def fill_with_cash(self, amount):
        print(f"{self.bank_name} ATM filled with ${amount} more.")

        if self.ATMbalance >= 10000:
            self.perform_maintenance()

    def update_ink(self, ink_level):
        print(f"{self.bank_name} ATM ink level updated to {ink_level}%.")

def load_customer_info(file_name):
    customers = {}
    with open(file_name, "r") as file:
        for line in file:
            name, card_number, pin, initial_balance = line.strip().split(",")
            customers[name.lower()] = {"card_number": card_number, "pin": pin, "initial_balance": float(initial_balance)}
    return customers

def main():
    customers = load_customer_info("customer_info.txt")
    
    role = input("Are you a Customer or ATM Technician? Enter 'Customer' or 'ATM Technician': ")
    if role.lower() == "customer":
        my_bank = Bank(bankName="Santander")
        my_atm = ATM(bank_name=my_bank.bankName)
        my_bank.add_atm(my_atm)

        customer_name = input("Enter your name: ").lower()
        if customer_name not in customers:
            print("Customer not found.")
            return

        card_number = input("Enter your card number: ")
        pin = input("Enter your PIN: ")

        customer_info = customers[customer_name]
        if card_number != customer_info["card_number"] or pin != customer_info["pin"]:
            print("Invalid card number or PIN.")
            return

        my_customer = Customer(customer_name.capitalize(), customer_info["initial_balance"], atm=my_atm)

        print("Authentication successful. Welcome to the ATM!")
        my_customer.getName()
        while True:
            print("\nMenu:")
            print("1. Check Balance")
            print("2. Withdraw Cash")
            print("3. Deposit Funds")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                my_customer.check_balance()
            elif choice == "2":
                amount = float(input("Enter withdrawal amount: $"))
                my_customer.withdraw_cash(amount)
            elif choice == "3":
                amount = float(input("Enter deposit amount: $"))
                my_customer.deposit_funds(amount)
            elif choice == "4":
                print("Thank you for using our ATM. Have a great day!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
    elif role.lower() == "atm technician":
        technician_id = input("Enter technician ID: ")
        code = input("Enter code: ")
        if technician_id == "123" and code == "123":
            technician_bank_name = input("Enter bank name: ")
            technician = ATMTechnician(bank_name=technician_bank_name, technician_id=technician_id, code=code)
            while True:
                print("\nATM Technician Menu:")
                print("1. Fill ATM with Cash")
                print("2. Upgrade ATM Software")
                print("3. Update Ink Level")
                print("4. Exit")
                technician_choice = input("Enter your choice: ")

                if technician_choice == "1":
                    amount = float(input("Enter amount to fill ATM with: $"))
                    technician.fill_with_cash(amount)
                elif technician_choice == "2":
                    technician.perform_maintenance()
                elif technician_choice == "3":
                    ink_level = int(input("Enter new ink level percentage: "))
                    technician.update_ink(ink_level)
                elif technician_choice == "4":
                    print("Exiting ATM Technician mode.")
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
        else:
            print("Authentication failed. Incorrect technician ID or code.")

if __name__ == "__main__":
    main()
