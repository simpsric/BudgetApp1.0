from enum import Enum

class month_enum_t(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

class category_enum_t(Enum):
    HOUSING = "HOUSING"
    TRANSPORTATION = "TRANSPORTATION"
    FOOD = "FOOD"
    UTILITIES = "UTILITIES"
    HEALTHCARE = "HEALTHCARE"
    INSURANCE = "INSURANCE"
    SAVINGS = "SAVINGS"
    DEBT = "DEBT"
    PERSONAL = "PERSONAL"
    RECREATION = "RECREATION"
    INCOME = "INCOME"
    OTHER = "OTHER"

class transaction_enum_t(Enum):
    INFLOW = "INFLOW"
    OUTFLOW = "OUTFLOW"