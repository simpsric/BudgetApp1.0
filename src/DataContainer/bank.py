from typing import List
from bank_account import BankAccount

class Bank:
    def __init__(
        self,
        name: str
    ):
        self.name = name
        self.accounts: List[BankAccount] = []

    def add_account(self, account: BankAccount) -> None:
        """Add a new bank account to this bank."""
        if account in self.accounts:
            raise ValueError("Account already exists in bank")
        self.accounts.append(account)
        
    def remove_account(self, account: BankAccount) -> None:
        """Remove a bank account from this bank."""
        if account not in self.accounts:
            raise ValueError("Account not found in bank")
        self.accounts.remove(account)

    def get_account(self, account_name: str) -> BankAccount | None:
        """Get a bank account by its name. Returns None if not found."""
        for account in self.accounts:
            if account.get_name() == account_name:
                return account
        return None
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the bank."""
        for account in self.accounts:
            if account.get_name() == transaction.get_account_name():
                account.add_transaction(transaction)
                return
            
        raise ValueError("Account not found in bank")

    def get_accounts(self) -> List[BankAccount]:
        """Get all bank accounts."""
        return self.accounts.copy()  # Return a copy to prevent direct list modification

    def __str__(self) -> str:
        account_summary = "\n".join(f"  {account}" for account in self.accounts)
        return (f"Bank: {self.name}\n"
                f"Accounts:\n{account_summary}")

    def __repr__(self) -> str:
        return f"Bank(name='{self.name}', accounts={self.accounts!r})"


if __name__ == "__main__":
    from decimal import Decimal
    from datetime import date
    from transaction import Transaction, month_enum_t, category_enum_t, transaction_enum_t
    from account_line_item import AccountLineItem

    def run_tests():
        print("Creating test bank...")
        bank = Bank(name="Test Bank")
        print(f"Initial bank state:\n{bank}\n")

        # Create test accounts
        checking = BankAccount(
            name="Primary Checking",
            notes="Main checking account"
        )
        savings = BankAccount(
            name="Savings",
            notes="Emergency fund"
        )

        # Add accounts to bank
        print("Adding test accounts...")
        bank.add_account(checking)
        bank.add_account(savings)
        print(f"\nBank state after adding accounts:\n{bank}\n")

        # Create some test transactions
        print("Adding test transactions to checking account...")
        transactions = [
            (
                "Initial Deposit",
                date(2024, 3, 15),
                Decimal("10000.00"),
                category_enum_t.INCOME,
                transaction_enum_t.INFLOW,
                True,  # is_cleared
            ),
            (
                "Transfer to Savings",
                date(2024, 3, 16),
                Decimal("5000.00"),
                category_enum_t.SAVINGS,
                transaction_enum_t.OUTFLOW,
                True,  # is_cleared
            )
        ]

        for (name, trans_date, amount, category, trans_type, 
             is_cleared) in transactions:
            
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
                current_balance=checking.get_running_balance()
            )
            line_item.is_cleared = is_cleared

            # Add to checking account
            checking.add_line_item(line_item)
            print(f"\nAdded transaction to checking: {line_item}")

        # Add savings transaction
        savings_transaction = Transaction(
            transaction_date=date(2024, 3, 16),
            budget_month=month_enum_t.MARCH,
            category=category_enum_t.SAVINGS,
            name="Transfer from Checking",
            amount=Decimal("5000.00"),
            type=transaction_enum_t.INFLOW
        )

        savings_line_item = AccountLineItem(
            transaction=savings_transaction,
            current_balance=savings.get_running_balance()
        )
        savings_line_item.is_cleared = True
        savings.add_line_item(savings_line_item)
        print(f"\nAdded transaction to savings: {savings_line_item}")

        print("\nFinal bank state:")
        print(bank)

        # Test account retrieval
        print("\nTesting account retrieval:")
        retrieved_checking = bank.get_account("Primary Checking")
        print(f"Retrieved checking account: {retrieved_checking is not None}")
        
        nonexistent = bank.get_account("Nonexistent Account")
        print(f"Retrieved nonexistent account: {nonexistent is not None}")

    # Run the tests
    try:
        run_tests()
    except Exception as e:
        print(f"Error during testing: {e}")
