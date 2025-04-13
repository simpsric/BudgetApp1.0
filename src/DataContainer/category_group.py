from decimal import Decimal
from typing import List, Optional
from transaction_category import TransactionCategory
from common_types import category_enum_t, month_enum_t, transaction_enum_t
from transaction import Transaction
class CategoryGroup:
    def __init__(
        self,
        name: str,
    ):
        self.name = name
        self.sub_groups: List['CategoryGroup'] = []
        self.categories: List[TransactionCategory] = []
        self._total_planned: Optional[Decimal] = None
        self._total_actual: Optional[Decimal] = None

    def add_sub_group(self, group: 'CategoryGroup') -> None:
        """Add a sub-category group."""
        self.sub_groups.append(group)
        
        # Update totals
        self._total_planned = self.total_planned
        self._total_actual = self.total_actual
        
    def remove_sub_group(self, group: 'CategoryGroup') -> None:
        """Remove a sub-category group."""
        if group not in self.sub_groups:
            raise ValueError("Sub-group not found in category group")
        
        # Update totals before removing group
        self._total_planned = self.total_planned - group.total_planned
        self._total_actual = self.total_actual + group.total_actual
        
        self.sub_groups.remove(group)
        
    def get_sub_groups(self) -> List['CategoryGroup']:
        """Get the sub-category groups."""
        return self.sub_groups

    def get_sub_group(self, name: str) -> 'CategoryGroup':
        """Get a sub-category group by name."""
        for group in self.sub_groups:
            if group.name == name:
                return group
        
        raise ValueError("Sub-group not found in category group")
    
    def get_categories(self) -> List[TransactionCategory]:
        """Get the transaction categories."""
        categories = []
        for category in self.categories:
            categories.append(category.get_name())
        for group in self.sub_groups:
            categories.extend(group.get_categories())
        return categories
    
    def get_category(self, name: str) -> TransactionCategory:
        """Get a transaction category by name."""
        for category in self.categories:
            if category.name == name:
                return category

        raise ValueError("Category not found in category group")

    def add_category(self, category: TransactionCategory) -> None:
        """Add a transaction category."""
        self.categories.append(category)
        # Update totals
        self._total_planned = self.total_planned
        self._total_actual = self.total_actual

    def remove_category(self, category: TransactionCategory) -> None:
        """Remove a transaction category."""
        if category not in self.categories:
            raise ValueError("Category not found in category group")
        
        # Update totals before removing category
        self._total_planned = self.total_planned - category.planned_amount
        self._total_actual = self.total_actual + category.actual_amount
        
        self.categories.remove(category)
        
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the category group."""
        found = False
        # Check if the transaction is in the categories list
        for category in self.categories:
            if category.get_name() == transaction.get_category():
                category.add_transaction(transaction)
                found = True
                break
        
        # Check if the transaction is in the sub-groups list
        for group in self.sub_groups:
            for category in group.categories:
                if category.get_name() == transaction.get_category():
                    group.add_transaction(transaction)
                    found = True
                    break
        
        # Update totals
        if found:
            self._total_actual = self.total_actual - transaction.get_amount()
        
    def remove_transaction(self, transaction: Transaction) -> None:
        """Remove a transaction from the category group."""
        # var to hold if the transaction was found
        found = False
        
        # Check if the transaction is in the categories list
        for category in self.categories:
            if category.get_category() == transaction.get_category():
                try:
                    category.remove_transaction(transaction)
                    found = True
                    break
                except ValueError:
                    # Transaction not found in this category, continue searching
                    continue
        
        # Check if the transaction is in the sub-groups list
        for group in self.sub_groups:
            for category in group.categories:
                if category.get_category() == transaction.get_category():
                    try:
                        category.remove_transaction(transaction)
                        found = True
                        break
                    except ValueError:
                        # Transaction not found in this category, continue searching
                        continue
        
        # If the transaction was not found, raise an error
        if not found:
            raise ValueError("Transaction not found in category group") 
        
        # Update totals
        self._total_actual = self.total_actual + transaction.get_amount()
        
    @property
    def total_planned(self) -> Decimal:
        """Calculate total planned amount including all sub-groups and categories."""
        total = Decimal("0.00")
        
        # Add direct categories
        for category in self.categories:
            total += category.planned_amount

        # Add sub-groups
        for group in self.sub_groups:
            total += group.total_planned

        self._total_planned = total

        return self._total_planned

    @property
    def total_actual(self) -> Decimal:
        """Calculate total actual amount including all sub-groups and categories."""
        total = Decimal("0.00")
        
        # Add direct categories
        for category in self.categories:
            total += category.actual_amount

        # Add sub-groups
        for group in self.sub_groups:
            total += group.total_actual

        self._total_actual = total

        return self._total_actual
    
    def get_name(self) -> str:
        """Get the name of the category group."""
        return self.name

    def get_remaining(self) -> Decimal:
        """Calculate remaining amount in the group."""
        return self._total_planned - self._total_actual

    def get_percent_used(self) -> float:
        """Calculate percentage of planned amount used."""
        if self._total_planned == Decimal("0.00"):
            return 0.0 if self._total_actual == Decimal("0.00") else float('inf')
        return float(self._total_actual / self._total_planned * 100)

    def __str__(self) -> str:
        def _indent(text: str, level: int = 1) -> str:
            indent = "  " * level
            return "\n".join(indent + line for line in text.split("\n"))

        percent = self.get_percent_used()
        percent_str = f"{percent:.1f}%" if percent != float('inf') else "∞%"
        
        result = [f"\nGroup: {self.name}",
                 f"Planned: ${self.total_planned:.2f}",
                 f"Actual: ${self.total_actual:.2f}",
                 f"Remaining: ${self.get_remaining():.2f}",
                 f"Used: {percent_str}"]

        if self.categories:
            result.append("\nCategories:")
            for category in self.categories:
                result.append(_indent(str(category)))

        if self.sub_groups:
            result.append("\nSub-groups:")
            for group in self.sub_groups:
                result.append(_indent(str(group)))

        return "\n".join(result)

    def __repr__(self) -> str:
        return (f"CategoryGroup(name='{self.name}', "
                f"sub_groups={self.sub_groups!r}, "
                f"categories={self.categories!r})")


if __name__ == "__main__":
    from datetime import date

    def run_tests():
        print("Creating test category structure...")
        
        # Create main group
        housing = CategoryGroup(name="Housing")

        # Create sub-groups
        utilities = CategoryGroup(name="Utilities")
        maintenance = CategoryGroup(name="Maintenance")

        # Create categories
        rent = TransactionCategory(
            name="Rent",
            category=housing.get_name(),
            budget_month=month_enum_t.MARCH,
            planned_amount=Decimal("2000.00")
        )

        electricity = TransactionCategory(
            name="Electricity",
            category=utilities.get_name(),
            budget_month=month_enum_t.MARCH,
            planned_amount=Decimal("150.00")
        )

        water = TransactionCategory(
            name="Water",
            category=utilities.get_name(),
            budget_month=month_enum_t.MARCH,
            planned_amount=Decimal("80.00")
        )

        repairs = TransactionCategory(
            name="Repairs",
            category=maintenance.get_name(),
            budget_month=month_enum_t.MARCH,
            planned_amount=Decimal("200.00")
        )

        # Build the structure
        utilities.add_category(electricity)
        utilities.add_category(water)
        maintenance.add_category(repairs)
        
        housing.add_category(rent)
        housing.add_sub_group(utilities)
        housing.add_sub_group(maintenance)


        print(f"Initial structure:\n{housing}\n")

        # Add some transactions
        transactions = [
            (rent, "Monthly Rent", Decimal("2000.00")),
            (electricity, "Power Bill", Decimal("145.50")),
            (water, "Water Bill", Decimal("75.25")),
            (repairs, "Fix Leaky Faucet", Decimal("85.00"))
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
            print(f"\nAdding transaction: {transaction}")
            housing.add_transaction(transaction)
            print(f"\nAdded transaction: {transaction}")

        print(f"\nFinal structure:\n{housing}")

        # Test totals
        print("\nTesting totals:")
        print(f"Total Planned: ${housing.total_planned:.2f}")
        print(f"Total Actual: ${housing.total_actual:.2f}")
        print(f"Remaining: ${housing.get_remaining():.2f}")
        print(f"Percent Used: {housing.get_percent_used():.1f}%")

    # Run the tests
    #try:
    run_tests()
    #except Exception as e:
    #    print(f"Error during testing: {e}")
