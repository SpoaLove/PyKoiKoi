from enum import Enum, IntEnum


class Category(Enum):
    HIKARI = 1
    TANE = 2
    TANZAKU = 3
    KASU = 4
    SAKAZUKI = 5
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name

class Month(IntEnum):
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

class Card:
    def __init__(self, month: Month, category: Category, image_name: str) -> None:
        self.month = month
        self.category = category
        self.image_name = image_name
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f'{self.month}:{self.category}'

    def __repr__(self) -> str:
        return str(self)

deck = [
    # January
    Card(Month.JANUARY, Category.HIKARI, 'sm_Hana-01-01.jpg'),
    Card(Month.JANUARY, Category.TANZAKU, 'sm_Hana-01-02.jpg'),
    Card(Month.JANUARY, Category.KASU, 'sm_Hana-01-03.jpg'),
    Card(Month.JANUARY, Category.KASU, 'sm_Hana-01-04.jpg'),
    # February
    Card(Month.FEBRUARY, Category.TANE, 'sm_Hana-02-01.jpg'),
    Card(Month.FEBRUARY, Category.TANZAKU, 'sm_Hana-02-02.jpg'),
    Card(Month.FEBRUARY, Category.KASU, 'sm_Hana-02-03.jpg'),
    Card(Month.FEBRUARY, Category.KASU, 'sm_Hana-02-04.jpg'),
    # March
    Card(Month.MARCH, Category.HIKARI, 'sm_Hana-03-01.jpg'),
    Card(Month.MARCH, Category.TANZAKU, 'sm_Hana-03-02.jpg'),
    Card(Month.MARCH, Category.KASU, 'sm_Hana-03-03.jpg'),
    Card(Month.MARCH, Category.KASU, 'sm_Hana-03-04.jpg'),
    # April
    Card(Month.APRIL, Category.TANE, 'sm_Hana-04-01.jpg'),
    Card(Month.APRIL, Category.TANZAKU, 'sm_Hana-04-02.jpg'),
    Card(Month.APRIL, Category.KASU, 'sm_Hana-04-03.jpg'),
    Card(Month.APRIL, Category.KASU, 'sm_Hana-04-04.jpg'),
    # May
    Card(Month.MAY, Category.TANE, 'sm_Hana-05-01.jpg'),
    Card(Month.MAY, Category.TANZAKU, 'sm_Hana-05-02.jpg'),
    Card(Month.MAY, Category.KASU, 'sm_Hana-05-03.jpg'),
    Card(Month.MAY, Category.KASU, 'sm_Hana-05-04.jpg'),
    # June
    Card(Month.JUNE, Category.TANE, 'sm_Hana-06-01.jpg'),
    Card(Month.JUNE, Category.TANZAKU, 'sm_Hana-06-02.jpg'),
    Card(Month.JUNE, Category.KASU, 'sm_Hana-06-03.jpg'),
    Card(Month.JUNE, Category.KASU, 'sm_Hana-06-04.jpg'),
    # July
    Card(Month.JULY, Category.TANE, 'sm_Hana-07-01.jpg'),
    Card(Month.JULY, Category.TANZAKU, 'sm_Hana-07-02.jpg'),
    Card(Month.JULY, Category.KASU, 'sm_Hana-07-03.jpg'),
    Card(Month.JULY, Category.KASU, 'sm_Hana-07-04.jpg'),
    # August
    Card(Month.AUGUST, Category.HIKARI, 'sm_Hana-08-01.jpg'),
    Card(Month.AUGUST, Category.TANE, 'sm_Hana-08-02.jpg'),
    Card(Month.AUGUST, Category.KASU, 'sm_Hana-08-03.jpg'),
    Card(Month.AUGUST, Category.KASU, 'sm_Hana-08-04.jpg'),
    # September
    Card(Month.SEPTEMBER, Category.SAKAZUKI, 'sm_Hana-09-01.jpg'),
    Card(Month.SEPTEMBER, Category.TANZAKU, 'sm_Hana-09-02.jpg'),
    Card(Month.SEPTEMBER, Category.KASU, 'sm_Hana-09-03.jpg'),
    Card(Month.SEPTEMBER, Category.KASU, 'sm_Hana-09-04.jpg'),
    # October
    Card(Month.OCTOBER, Category.TANE, 'sm_Hana-10-01.jpg'),
    Card(Month.OCTOBER, Category.TANZAKU, 'sm_Hana-10-02.jpg'),
    Card(Month.OCTOBER, Category.KASU, 'sm_Hana-10-03.jpg'),
    Card(Month.OCTOBER, Category.KASU, 'sm_Hana-10-04.jpg'),
    # November
    Card(Month.NOVEMBER, Category.HIKARI, 'sm_Hana-11-01.jpg'),
    Card(Month.NOVEMBER, Category.TANE, 'sm_Hana-11-02.jpg'),
    Card(Month.NOVEMBER, Category.TANZAKU, 'sm_Hana-11-03.jpg'),
    Card(Month.NOVEMBER, Category.KASU, 'sm_Hana-11-04.jpg'),
    # December
    Card(Month.DECEMBER, Category.HIKARI, 'sm_Hana-12-01.jpg'),
    Card(Month.DECEMBER, Category.KASU, 'sm_Hana-12-02.jpg'),
    Card(Month.DECEMBER, Category.KASU, 'sm_Hana-12-03.jpg'),
    Card(Month.DECEMBER, Category.KASU, 'sm_Hana-12-04.jpg'),
    
]

