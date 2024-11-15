
import random
from datetime import datetime


class Account:
    def __init__(self, balance=2000, pin="0000"):
        self.balance = balance
        self.pin = pin

    def check_pin(self, input_pin):
        """Check if the provided PIN matches the account PIN."""
        return self.pin == input_pin

    def withdraw(self, amount):
        """Withdraw the specified amount if sufficient balance exists."""
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def check_balance(self):
        """Return the current balance."""
        return self.balance


class Transaction:
    def __init__(self, account):
        self.account = account

    def withdraw(self, amount):
        """Attempt to withdraw an amount from the account."""
        if self.account.withdraw(amount):
            return True, f"Transaction successful! You withdrew €{amount}."
        return False, "Insufficient funds. Please try again."

    def get_balance(self):
        """Retrieve the account balance."""
        return self.account.check_balance()


class Receipt:
    def __init__(self, transaction_type, amount, remaining_balance):
        self.transaction_type = transaction_type
        self.amount = amount
        self.remaining_balance = remaining_balance

    def generate(self):
        """Generate a receipt with transaction details."""
        now = datetime.now()
        return (
            f"Receipt:\n"
            f"Date: {now.strftime('%Y-%m-%d')}\n"
            f"Time: {now.strftime('%H:%M:%S')}\n"
            f"Transaction: {self.transaction_type}\n"
            f"Amount: €{self.amount}\n"
            f"Remaining Balance: €{self.remaining_balance}\n"
        )


class ATM:
    def __init__(self):
        self.account = Account()
        self.transaction = Transaction(self.account)
        self.user_authenticated = False
        self.default_withdrawal_options = [20, 50, 100, 200, 500]

    def authenticate(self):
        """Authenticate the user by checking the PIN."""
        attempts = 3
        while attempts > 0:
            input_pin = input("Enter your PIN: ")
            if self.account.check_pin(input_pin):
                print("Authentication successful!")
                self.user_authenticated = True
                return
            else:
                attempts -= 1
                print(f"Invalid PIN. {attempts} attempts remaining.")
        print("Too many incorrect attempts. Card blocked.")
        exit()

    def display_menu(self):
        """Display transaction options."""
        print("\nWelcome to the ATM!")
        options = ["Cash Withdrawal",
        "Balance Inquiry",
        "PIN Change",
        "Utility Bill Payment",
        "Other Services",
        "Fund Transfer",
        "Mini Statement",
        "Fast Cash",
        "Exit"]
        for i, option in enumerate(options, start=1):
           print(f"{i}. {option}")

    def display_withdrawal_options(self):
        """Display predefined withdrawal amount options."""
        print("\nSelect a withdrawal amount:")
        for i, amount in enumerate(self.default_withdrawal_options, 1):
            print(f"{i}. €{amount}")
        print(f"{len(self.default_withdrawal_options) + 1}. Enter custom amount")
        choice = input("Enter your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.default_withdrawal_options):
            return self.default_withdrawal_options[int(choice) - 1]
        elif choice == str(len(self.default_withdrawal_options) + 1):
            return self.enter_custom_amount()
        else:
            print("Invalid choice. Returning to main menu.")
            return None

    def enter_custom_amount(self):
        """Allow the user to input a custom withdrawal amount."""
        try:
            custom_amount = int(input("Enter custom amount (multiples of 10): €"))
            if custom_amount > 0 and custom_amount % 10 == 0:
                return custom_amount
            else:
                print("Invalid amount. Please enter a valid multiple of 10.")
                return self.enter_custom_amount()
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.enter_custom_amount()

    def handle_withdrawal(self):
        """Handle cash withdrawal."""
        amount = self.display_withdrawal_options()
        if amount is not None:
            success, message = self.transaction.withdraw(amount)
            print(message)
            if success:
                receipt_choice = input("Do you want a receipt? (yes/no):").strip().lower()
                if receipt_choice == "yes":
                    receipt = Receipt("Withdrawal", amount, self.account.check_balance())
                    print("\n" + receipt.generate())
                print("\n")
                self.finish_transaction(amount)

    def handle_balance_inquiry(self):
        """Handle balance inquiry."""
        balance = self.transaction.get_balance()
        print(f"Your current balance is: €{balance}")

    def start(self):
        """Main loop to handle ATM operations."""
        self.authenticate()
        while self.user_authenticated:
            self.display_menu()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.handle_withdrawal()
            elif choice == "2":
                self.handle_balance_inquiry()
            elif choice == "9":
                print("\n")
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    def finish_transaction(self,amount):
        print(f"Dispensing €{amount}...")
        print("Transaction Complete. Please retrieve your card.")
        print("Thank's for banking with us")
        self.user_authenticated = False
        self.reset_atm()

    def reset_atm(self):
        self.transaction.withdrawal_amount = 0
        print("\nATM ready for next transaction.")



# Run the ATM
if __name__ == "__main__":
    atm = ATM()
    atm.start()
