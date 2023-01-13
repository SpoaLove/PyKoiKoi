from typing import List, Callable, Tuple
from hanafuda_card import Card, Month, Category, deck

class Yaku:
    def __init__(self, check_combo:Callable[[List[Card]], int]):
        self.name = check_combo.__name__[6:]
        self.check_combo = check_combo

# hikaris
crane_and_sun = Card(Month.JANUARY, Category.HIKARI, 'sm_Hana-01-01.jpg')
curtain = Card(Month.MARCH, Category.HIKARI, 'sm_Hana-03-01.jpg')
full_moon = Card(Month.AUGUST, Category.HIKARI, 'sm_Hana-08-01.jpg')
ono_no_michikaze = Card(Month.NOVEMBER, Category.HIKARI, 'sm_Hana-11-01.jpg')
chinese_phenoix = Card(Month.DECEMBER, Category.HIKARI, 'sm_Hana-12-01.jpg')

goko = [    
    crane_and_sun,
    curtain,
    full_moon,
    ono_no_michikaze,
    chinese_phenoix
]

shiko = [    
    crane_and_sun,
    curtain,
    full_moon,
    chinese_phenoix
]

# sake cup
sake_cup = Card(Month.SEPTEMBER, Category.SAKAZUKI, 'sm_Hana-09-01.jpg')

# inoshikacho
butterfiles = Card(Month.JUNE, Category.TANE, 'sm_Hana-06-01.jpg')
boar = Card(Month.JULY, Category.TANE, 'sm_Hana-07-01.jpg')
deer = Card(Month.OCTOBER, Category.TANE, 'sm_Hana-10-01.jpg')

inoshikacho = [butterfiles, boar, deer]

# tanzakus
poetry_tanzaku = [
    Card(Month.JANUARY, Category.TANZAKU, 'sm_Hana-01-02.jpg'),
    Card(Month.FEBRUARY, Category.TANZAKU, 'sm_Hana-02-02.jpg'),
    Card(Month.MARCH, Category.TANZAKU, 'sm_Hana-03-02.jpg'),
]
blue_tanzaku = [
    Card(Month.JUNE, Category.TANZAKU, 'sm_Hana-06-02.jpg'),
    Card(Month.SEPTEMBER, Category.TANZAKU, 'sm_Hana-09-02.jpg'),
    Card(Month.OCTOBER, Category.TANZAKU, 'sm_Hana-10-02.jpg'),
]

def count_intersection(point_file:List[Card], combo:List[Card]) -> int:
    intersection = [card for card in point_file if card in combo]
    return len(intersection)

def check_goko(point_pile:List[Card]) -> int: 
    return 15 if all(card in point_pile for card in goko) else 0

def check_shiko(point_pile:List[Card]) -> int:
    return 8 if (ono_no_michikaze not in point_pile) and count_intersection(point_pile, shiko) == 4 else 0

def check_ameshiko(point_pile:List[Card]) -> int:
    return 7 if (ono_no_michikaze in point_pile) and count_intersection(point_pile, shiko) == 3 else 0

def check_sanko(point_pile:List[Card]) -> int:
    return 6 if (ono_no_michikaze not in point_pile) and count_intersection(point_pile, shiko) == 3 else 0

def check_tsukimizake(point_pile:List[Card]) -> int:
    return 5 if (sake_cup in point_pile) and (full_moon in point_pile) else 0

def check_hanamizake(point_pile:List[Card]) -> int:
    return 5 if (sake_cup in point_pile) and (curtain in point_pile) else 0

def check_inoshikacho(point_pile:List[Card]) -> int:
    return 5 if all(card in point_pile for card in inoshikacho) else 0

def check_tane(point_pile:List[Card]) -> int:
    tane_count = len([card for card in point_pile if card.category == Category.TANE or card.category == Category.SAKAZUKI])
    return tane_count - 4 if tane_count >= 5 else 0

def check_akatan(point_pile:List[Card]) -> int:
    return 5 if all(card in point_pile for card in poetry_tanzaku) else 0

def check_aotan(point_pile:List[Card]) -> int:
    return 5 if all(card in point_pile for card in blue_tanzaku) else 0

def check_tanzaku(point_pile:List[Card]) -> int:
    tanzaku_count = len([card for card in point_pile if card.category == Category.TANZAKU])
    return tanzaku_count - 4 if tanzaku_count >= 5 else 0

def check_tsukifuda(point_pile:List[Card]) -> int:
    tsukifuda_count = len([month for month in Month if len([card for card in point_pile if card.month == month]) == 4]) 
    return tsukifuda_count * 4

def check_kasu(point_pile:List[Card]) -> int:
    kasu_count = len([card for card in point_pile if card.category == Category.KASU or card.category == Category.SAKAZUKI])
    return kasu_count - 9 if kasu_count >= 10 else 0

check_combo_functions = [
    check_goko,
    check_shiko,
    check_ameshiko,
    check_sanko,
    check_tsukimizake,
    check_hanamizake,
    check_inoshikacho,
    check_tane,
    check_akatan,
    check_aotan,
    check_tanzaku,
    check_tsukifuda,
    check_kasu
]

yakus = [
    Yaku(check_combo_function)
    for check_combo_function in check_combo_functions
]

def check_all_yakus(point_pile:List[Card]) -> Tuple[int, List[str]]:
    obtained_yakus = []
    sum_point = 0
    for yaku in yakus:
        yaku_point = yaku.check_combo(point_pile)
        if yaku_point:
            sum_point += yaku_point
            obtained_yakus.append(yaku.name)
    return sum_point, obtained_yakus


# print(check_all_yakus(deck))
# print(check_all_yakus(deck[:10]))





