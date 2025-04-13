from decimal import Decimal
from typing import List
from account_line_item import AccountLineItem

class BankAccount:
    def __init__(
        self,
        name: str,
        notes: str = ""  # Optional notes field
    ):
        self.name = name
        self.notes = notes
        self.line_items: List[AccountLineItem] = []
        self.running_total: Decimal = Decimal("0.00")
        self.cleared_amount: Decimal = Decimal("0.00")
        self.uncleared_amount: Decimal = Decimal("0.00")

    def add_line_item(self, line_item: AccountLineItem) -> None:
        """Add a new line item to the account and update balances."""
        self.line_items.append(line_item)
        self.running_total = line_item.get_running_balance()

        # Update cleared/uncleared amounts based on transaction status
        if line_item.is_cleared:
            self.cleared_amount += line_item.get_amount()
        else:
            self.uncleared_amount += line_item.get_amount()
            
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the account and update balances."""
        line_item = AccountLineItem(
            transaction=transaction,
            current_balance=self.running_total,
            account_name=self.name
        )
        self.add_line_item(line_item)
    
    def remove_line_item(self, line_item: AccountLineItem) -> None:
        """Remove a line item from the account and update balances."""
        if line_item not in self.line_items:
            raise ValueError("Line item not found in account")
        self.line_items.remove(line_item)
        self.running_total -= line_item.get_amount()
        
        # Update cleared/uncleared amounts based on transaction status
        if line_item.is_cleared:
            self.cleared_amount -= line_item.get_amount()
        else:
            self.uncleared_amount -= line_item.get_amount()
    
    def get_running_balance(self) -> Decimal:
        return self.running_total

    def get_line_items(self) -> List[AccountLineItem]:
        """Return all line items in chronological order."""
        return sorted(self.line_items, key=lambda x: x.get_date())
    
    def get_name(self) -> str:
        return self.name
    
    def get_notes(self) -> str:
        return self.notes
    
    def get_cleared_amount(self) -> Decimal:
        return self.cleared_amount
    
    def get_uncleared_amount(self) -> Decimal:
        return self.uncleared_amount

    def __str__(self) -> str:
        return (f"Account: {self.name}\n"
                f"Balance: ${self.running_total}\n"
                f"Cleared: ${self.cleared_amount}\n"
                f"Uncleared: ${self.uncleared_amount}")

    def __repr__(self) -> str:
        return (f"BankAccount(name='{self.name}', "
                f"notes='{self.notes}', "
                f"running_total={self.running_total}, "
                f"cleared_amount={self.cleared_amount}, "
                f"uncleared_amount={self.uncleared_amount}, "
                f"line_items={self.line_items!r})")


if __name__ == "__main__":
    from datetime import date
    from transaction import Transaction, month_enum_t, category_enum_t, transaction_enum_t
    
    def run_tests():
        print("Creating test bank account...")
        account = BankAccount(
            name="Test Checking",
            notes="Test account for demonstration"
        )
        print(f"Initial account state:\n{account}\n")

        # Create some test transactions
        transactions = [
            (
                "Salary Deposit",
                date(2024, 3, 15),
                Decimal("5000.00"),
                category_enum_t.INCOME,
                transaction_enum_t.INFLOW,
                True,  # is_cleared
            ),
            (
                "Rent Payment",
                date(2024, 3, 16),
                Decimal("2000.00"),
                category_enum_t.HOUSING,
                transaction_enum_t.OUTFLOW,
                True,  # is_cleared
            ),
            (
                "Grocery Shopping",
                date(2024, 3, 17),
                Decimal("150.00"),
                category_enum_t.FOOD,
                transaction_enum_t.OUTFLOW,
                False,  # is_cleared
            )
        ]

        print("Adding test transactions...")
        for (name, trans_date, amount, category, trans_type, 
             is_cleared) in transactions:
            print(f"Transaction name: {name}")
            # Create transaction
            transaction = Transaction(
                transaction_date=trans_date,
                budget_month=month_enum_t(trans_date.month),
                category=category,
                name=name,
                amount=amount,
                type=trans_type
            )

            # Create line item
            line_item = AccountLineItem(
                transaction=transaction,
                current_balance=account.get_running_balance()
            )
            line_item.is_cleared = is_cleared

            # Add to account
            account.add_line_item(line_item)
            print(f"\nAdded transaction: {line_item}")

        print("\nFinal account state:")
        print(account)

        print("\nAll transactions in chronological order:")
        for item in account.get_line_items():
            print(f"  {item}")

    # Run the tests
    try:
        run_tests()
    except Exception as e:
        print(f"Error during testing: {e}")

