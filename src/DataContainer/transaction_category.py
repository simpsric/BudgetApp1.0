from decimal import Decimal
from typing import List
from transaction import Transaction
from common_types import category_enum_t, month_enum_t
class TransactionCategory:
    def __init__(
        self,
        name: str,
        category: category_enum_t,
        budget_month: month_enum_t,
        planned_amount: Decimal = Decimal("0.00"),
        notes: str = ""
    ):
        self.name = name
        self.category = category
        self.budget_month = budget_month
        self.planned_amount = planned_amount
        self.actual_amount: Decimal = Decimal("0.00")
        self.notes = notes
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction and update the actual amount."""
        if transaction.get_budget_month() != self.budget_month:
            raise ValueError("Transaction budget month does not match category budget month")
        self.transactions.append(transaction)
        self.actual_amount -= transaction.get_amount()
        
    def get_budget_month(self) -> month_enum_t:
        """Get the budget month for the category."""
        return self.budget_month
    
    def get_notes(self) -> str:
        """Get the notes for the category."""
        return self.notes
    
    def get_name(self) -> str:
        """Get the name for the category."""
        return self.name
        
    def remove_transaction(self, transaction: Transaction) -> None:
        """Remove a transaction and update the actual amount."""
        if transaction not in self.transactions:
            raise ValueError("Transaction not found in category")
        self.transactions.remove(transaction)
        self.actual_amount += transaction.get_amount()
        
    def set_planned_amount(self, planned_amount: Decimal) -> None:
        """Set the planned amount for the category."""
        self.planned_amount = planned_amount
        
    def get_planned_amount(self) -> Decimal:
        """Get the planned amount for the category."""
        return self.planned_amount
    
    def get_actual_amount(self) -> Decimal:
        """Get the actual amount for the category."""
        return self.actual_amount

    def get_transactions(self) -> List[Transaction]:
        """Get all transactions in chronological order."""
        return sorted(self.transactions, key=lambda x: x.get_transaction_date())

    def get_remaining_amount(self) -> Decimal:
        """Calculate remaining amount in the budget category."""
        return self.planned_amount - self.actual_amount

    def get_percent_used(self) -> float:
        """Calculate percentage of planned amount used."""
        if self.planned_amount == Decimal("0.00"):
            return 0.0 if self.actual_amount == Decimal("0.00") else float('inf')
        return float(self.actual_amount / self.planned_amount * 100)
    
    def get_category(self) -> category_enum_t:
        """Get the category for the category."""
        return self.category

    def __str__(self) -> str:
        percent = self.get_percent_used()
        percent_str = f"{percent:.1f}%" if percent != float('inf') else "∞%"
        
        return (f"Category: {self.name} ({self.category})\n"
                f"Planned: ${self.planned_amount:.2f}\n"
                f"Actual: ${self.actual_amount:.2f}\n"
                f"Remaining: ${self.get_remaining_amount():.2f}\n"
                f"Used: {percent_str}\n"
                f"Transactions: {len(self.transactions)}\n")

    def __repr__(self) -> str:
        return (f"TransactionCategory(name='{self.name}', "
                f"category={self.category}, "
                f"planned_amount={self.planned_amount}, "
                f"actual_amount={self.actual_amount}, "
                f"notes='{self.notes}', "
                f"transactions={self.transactions!r})")


if __name__ == "__main__":
    from datetime import date
    from transaction import month_enum_t, transaction_enum_t

    def run_tests():
        print("Creating test transaction category...")
        category = TransactionCategory(
            name="Groceries",
            category=category_enum_t.FOOD,
            budget_month=month_enum_t.MARCH,
            planned_amount=Decimal("500.00"),
            notes="Monthly grocery budget"
        )
        print(f"Initial category state:\n{category}\n")

        # Create test transactions
        transactions = [
            (
                "Walmart Groceries",
                date(2024, 3, 15),
                Decimal("150.75"),
                transaction_enum_t.OUTFLOW
            ),
            (
                "Costco Bulk Items",
                date(2024, 3, 16),
                Decimal("245.50"),
                transaction_enum_t.OUTFLOW
            ),
            (
                "Return Damaged Item",
                date(2024, 3, 17),
                Decimal("25.00"),
                transaction_enum_t.INFLOW
            )
        ]

        print("Adding test transactions...")
        for name, trans_date, amount, trans_type in transactions:
            transaction = Transaction(
                transaction_date=trans_date,
                budget_month=month_enum_t(trans_date.month),
                category=category_enum_t.FOOD,
                name=name,
                amount=amount,
                type=trans_type,
                account_name="Checking"
            )
            
            category.add_transaction(transaction)
            print(f"\nAdded transaction: {transaction}")
            print(f"Category state:\n{category}")

        print("\nAll transactions in chronological order:")
        for transaction in category.get_transactions():
            print(f"  {transaction}")

        # Test edge case with zero planned amount
        print("\nTesting category with zero planned amount...")
        zero_category = TransactionCategory(
            name="Miscellaneous",
            category=category_enum_t.OTHER,
            budget_month=month_enum_t.MARCH,
            planned_amount=Decimal("0.00")
        )
        print(f"Zero category state:\n{zero_category}")

    # Run the tests
    try:
        run_tests()
    except Exception as e:
        print(f"Error during testing: {e}")
