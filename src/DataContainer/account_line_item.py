from decimal import Decimal
from transaction import Transaction, month_enum_t, category_enum_t, transaction_enum_t
from datetime import date

class AccountLineItem:
    def __init__(
        self,
        transaction: Transaction,
        current_balance: Decimal,
        account_name: str
    ):
        self._transaction = transaction
        self._running_balance = current_balance + transaction.get_amount()
        self._is_cleared = False  # Internal variable with underscore prefix
        self._account_name = account_name
    
    def get_amount(self) -> Decimal:
        return self._transaction.get_amount()
    
    def get_date(self) -> date:
        return self._transaction.get_transaction_date()
    
    def get_type(self) -> transaction_enum_t:
        return self._transaction.get_type()
    
    def get_category(self) -> category_enum_t:
        return self._transaction.get_category()
    
    def get_name(self) -> str:
        return self._transaction.get_name()
    
    def get_budget_month(self) -> month_enum_t:
        return self._transaction.get_budget_month()
    
    def get_account_name(self) -> str:
        return self._account_name
    
    def get_running_balance(self) -> Decimal:
        return self._running_balance

    @property
    def is_cleared(self) -> bool:
        """Get the cleared status of the line item."""
        return self._is_cleared

    @is_cleared.setter
    def is_cleared(self, value: bool) -> None:
        """Set the cleared status of the line item."""
        self._is_cleared = bool(value)  # Ensure the value is boolean

    def __str__(self) -> str:
        status = "✓" if self._is_cleared else "u"
        return f"[{status}] {self._transaction} | Balance: ${self._running_balance}"

    def __repr__(self) -> str:
        return (f"AccountLineItem(transaction={self._transaction!r}, "
                f"running_balance={self._running_balance}, "
                f"is_cleared={self._is_cleared})")


if __name__ == "__main__":    
    # Create a sample transaction
    test_transaction = Transaction(
        transaction_date=date(2024, 3, 19),
        budget_month=month_enum_t.MARCH,
        category=category_enum_t.FOOD,
        name="Grocery Shopping",
        amount=Decimal("123.45"),
        type=transaction_enum_t.OUTFLOW
    )
    

    # Create an account line item
    test_account_line_item = AccountLineItem(
        transaction=test_transaction,
        current_balance=Decimal("1000.00")
    )

    # Test string representations
    print("String representation:")
    print(str(test_account_line_item))
    print("\nRepr representation:")
    print(repr(test_account_line_item))

    # Test getters
    print("\nTesting getters:")
    print(f"Running Balance: ${test_account_line_item.get_running_balance()}")
    print(f"Is Cleared: {test_account_line_item.is_cleared}")

    # Test setter
    test_account_line_item.is_cleared = True
    print(f"Is Cleared: {test_account_line_item.is_cleared}")
    
    print(test_account_line_item)
