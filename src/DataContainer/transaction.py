from datetime import date
from common_types import *
from decimal import Decimal


class Transaction:
    def __init__(
        self,
        transaction_date: date,
        budget_month: month_enum_t,
        category: category_enum_t,
        name: str,
        amount: Decimal,
        account_name: str,
        type: transaction_enum_t = transaction_enum_t.OUTFLOW
    ):
        # Check decimal places of amount
        if amount.as_tuple().exponent > -2:
            raise ValueError("Amount must have 2 or fewer decimal places")
            
        self._transaction_date = transaction_date
        self._budget_month = budget_month
        self._category = category
        self._name = name
        self._amount = amount
        self._type = type
        self._account_name = account_name
        
    def get_amount(self) -> Decimal:
        return -self._amount if self._type == transaction_enum_t.OUTFLOW else self._amount
    
    def get_type(self) -> transaction_enum_t:
        return self._type
    
    def get_category(self) -> category_enum_t:
        return self._category
    
    def get_account_name(self) -> str:
        return self._account_name
    
    def get_transaction_date(self) -> date:
        return self._transaction_date
    
    def get_budget_month(self) -> month_enum_t:
        return self._budget_month
    
    def get_name(self) -> str:
        return self._name
    
    def __str__(self) -> str:
        amount_str = f"-${self._amount}" if self._type == transaction_enum_t.OUTFLOW else f"${self._amount}"
        return f"{self._name} | {self._transaction_date} | {self._category} | {amount_str}"

    def __repr__(self) -> str:
        return (f"Transaction(transaction_date={self._transaction_date}, "
                f"budget_month={self._budget_month}, "
                f"category={self._category}, "
                f"name='{self._name}', "
                f"amount={self._amount}, "
                f"type={self._type})")
        


if __name__ == "__main__":
    # Create a sample transaction
    test_transaction = Transaction(
        transaction_date=date(2024, 3, 19),
        budget_month=month_enum_t.MARCH,
        category="FOOD",
        name="Grocery Shopping",
        amount=Decimal("123.45"),
        type="OUTFLOW",
        account_name="Checking"
    )
    
    # sample a transaction with an inflow
    test_transaction_2 = Transaction(
        transaction_date=date(2024, 3, 19),
        budget_month=month_enum_t.MARCH,
        category="FOOD",
        name="Grocery Shopping",
        amount=Decimal("123.45"),
        type=transaction_enum_t.INFLOW,
        account_name="Checking"
    )

    # Test string representations
    print("String representation:")
    print(str(test_transaction))
    print("\nRepr representation:")
    print(repr(test_transaction))
    
    # Test string representations
    print("\nString representation:")
    print(str(test_transaction_2))
    print("\nRepr representation:")
    print(repr(test_transaction_2))
    
    # Test getters
    print("\nTesting getters:")
    print(f"Amount: ${test_transaction.get_amount()}")
    print(f"Type: {test_transaction.get_type()}")
    print(f"Category: {test_transaction.get_category()}")
    print(f"Date: {test_transaction.get_transaction_date()}")
    print(f"Budget Month: {test_transaction.get_budget_month()}")
    print(f"Name: {test_transaction.get_name()}")
    
    # Test getters
    print("\nTesting getters:")
    print(f"Amount: ${test_transaction_2.get_amount()}")
    print(f"Type: {test_transaction_2.get_type()}")
    print(f"Category: {test_transaction_2.get_category()}")
    print(f"Date: {test_transaction_2.get_transaction_date()}")
    print(f"Budget Month: {test_transaction_2.get_budget_month()}")
    print(f"Name: {test_transaction_2.get_name()}")
