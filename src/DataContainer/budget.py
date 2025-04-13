from decimal import Decimal
from typing import List, Optional
from category_group import CategoryGroup
from common_types import *
from transaction import Transaction

class Budget:
    """
    A budget for a month and year.
    
    """
    def __init__(
        self,
        budget_month: month_enum_t,
        budget_year: int,
        name: str
    ):
        """Initialize a budget.

        Args:
            budget_month (month_enum_t): The month of the budget.
            budget_year (int): The year of the budget.
            name (str): The name of the budget.
        
        Internal Variables:
            categories (List[CategoryGroup]): The category groups in the budget.
            _total (Optional[Decimal]): The total of the budget.
        """
        self.budget_month = budget_month
        self.budget_year = budget_year
        self.name = name
        self.categories: List[CategoryGroup] = []
        self._total: Optional[Decimal] = None

    def add_category_group(self, group: CategoryGroup) -> None:
        """Add a category group to the budget."""
        self.categories.append(group)
        self._total = None  # Reset cached total
    
    def remove_category_group(self, group: CategoryGroup) -> None:
        """Remove a category group from the budget."""
        if group not in self.categories:
            raise ValueError("Category group not found in budget")
        self.categories.remove(group)
        self._total = None  # Reset cached total

    def get_category_groups(self) -> List[CategoryGroup]:
        """Get all category groups."""
        return self.categories.copy()
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the budget."""
        for group in self.categories:
            if transaction.get_category() in group.get_categories():
                group.add_transaction(transaction)
                break;
        
        # Update the total
        self.update_total()
        
    def update_total(self) -> None:
        """Update the total of the budget."""
        self._total = sum(
            (group.total_actual for group in self.categories),
            Decimal("0.00")
        )

    @property
    def total(self) -> Decimal:
        """Calculate total budget amount from all category groups."""
        if self._total is None:
            self._total = sum(
                (group.total_actual for group in self.categories),
                Decimal("0.00")
            )
        return self._total

    def get_month_year_str(self) -> str:
        """Get formatted month and year string."""
        return f"{self.budget_month.name.title()} {self.budget_year}"

    def __str__(self) -> str:
        def _indent(text: str, level: int = 1) -> str:
            indent = "  " * level
            return "\n".join(indent + line for line in text.split("\n"))

        result = [
            f"Budget: {self.name}",
            f"Period: {self.get_month_year_str()}",
            f"Total: ${self.total:.2f}",
            "\nCategory Groups:"
        ]

        for group in self.categories:
            result.append(_indent(str(group)))

        return "\n".join(result)

    def __repr__(self) -> str:
        return (f"Budget(budget_month={self.budget_month}, "
                f"budget_year={self.budget_year}, "
                f"name='{self.name}', "
                f"categories={self.categories!r})")


if __name__ == "__main__":
    from datetime import date
    from transaction_category import TransactionCategory

    def run_tests():
        print("Creating test budget...")
        
        # Create budget
        budget = Budget(
            budget_month=month_enum_t.MARCH,
            budget_year=2024,
            name="Monthly Budget"
        )
        print(f"Initial budget state:\n{budget}\n")

        # Create category structure
        
        # Housing group
        housing = CategoryGroup(name="Housing")
        utilities = CategoryGroup(name="Utilities")
        
        rent = TransactionCategory(
            name="Rent",
            category=housing.get_name(),
            planned_amount=Decimal("2000.00"),
            budget_month=month_enum_t.MARCH
        )
        
        electricity = TransactionCategory(
            name="Electricity",
            category=utilities.get_name(),
            planned_amount=Decimal("150.00"),
            budget_month=month_enum_t.MARCH
        )
        
        water = TransactionCategory(
            name="Water",
            category=utilities.get_name(),
            planned_amount=Decimal("80.00"),
            budget_month=month_enum_t.MARCH
        )
        
        utilities.add_category(electricity)
        utilities.add_category(water)
        housing.add_category(rent)
        housing.add_sub_group(utilities)

        # Food group
        food = CategoryGroup(name="Food")
        
        groceries = TransactionCategory(
            name="Groceries",
            category=food.get_name(),
            planned_amount=Decimal("500.00"),
            budget_month=month_enum_t.MARCH
        )
        
        dining = TransactionCategory(
            name="Dining Out",
            category=food.get_name(),
            planned_amount=Decimal("200.00"),
            budget_month=month_enum_t.MARCH
        )

        food.add_category(groceries)
        food.add_category(dining)

        # Add groups to budget
        print("Adding category groups...")
        budget.add_category_group(housing)
        budget.add_category_group(food)
        print(f"\nBudget after adding groups:\n{budget}\n")

        # Add some transactions
        transactions = [
            (rent, "Monthly Rent", Decimal("2000.00")),
            (electricity, "Power Bill", Decimal("145.50")),
            (water, "Water Bill", Decimal("75.25")),
            (groceries, "Weekly Groceries", Decimal("125.75")),
            (dining, "Restaurant Dinner", Decimal("45.00"))
        ]

        print("Adding transactions...")
        for category, name, amount in transactions:
            transaction = Transaction(
                transaction_date=date(2024, 2, 19),
                budget_month=month_enum_t.MARCH,
                category=category.get_name(),
                name=name,
                amount=amount,
                type=transaction_enum_t.OUTFLOW,
                account_name="Checking"
            )
            budget.add_transaction(transaction)
            print(f"\nAdded transaction: {transaction}")
            # Reset cached total
            budget.update_total()

        print(f"\nFinal budget state:\n{budget}")

        # Test budget totals
        print("\nTesting budget calculations:")
        print(f"Total spending: ${budget.total:.2f}")
        print(f"Budget period: {budget.get_month_year_str()}")

        # Test category group retrieval
        print("\nRetrieving category groups:")
        groups = budget.get_category_groups()
        for group in groups:
            print(f"  {group.name}: "
                  f"Planned=${group.total_planned:.2f}, "
                  f"Actual=${group.total_actual:.2f}")

    # Run the tests
    try:
        run_tests()
    except Exception as e:
        print(f"Error during testing: {e}")
