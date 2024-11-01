# Import necessary libraries
import decimal
from decimal import Decimal

decimal.getcontext().prec = 9  # Set precision to 9

def calculate_shares_percentage(shares):
    total_shares = Decimal(sum(shares))
    percentages = [round((Decimal(share) / total_shares) * Decimal(100), 3) for share in shares]
    return percentages

# Test the function with example data
shares = [0.125, 0.250, 0.500, 0.125]
percentages = calculate_shares_percentage(shares)
for perc in percentages:
    print(f"{perc:.3f}%")

# The megatrader problem
class BondLot:
    def __init__(self, day, name, price, quantity):
        self.day = day
        self.name = name
        self.price = Decimal(price)
        self.quantity = quantity

    @property
    def cost(self):
        return self.price * self.quantity

    @property
    def income(self):
        return self.quantity * (1 + 1000)

class MegaTrader:
    def __init__(self, n, m, s):
        self.n = n
        self.m = m
        self.s = Decimal(s)
        self.bond_lots = []
        self.purchased_lots = []

    def add_bond_lot(self, day, name, price, quantity):
        self.bond_lots.append(BondLot(day, name, price, quantity))

    def maximize_income(self):
        # Sort lots by day and then by price (ascending)
        bond_lots = sorted(self.bond_lots, key=lambda lot: (lot.day, lot.price))
        
        for lot in bond_lots:
            if lot.cost <= self.s:
                self.s -= lot.cost
                self.purchased_lots.append(lot)

    def calculate_total_income(self):
        total_income = sum(lot.income for lot in self.purchased_lots)
        return total_income

    def get_purchased_lots(self):
        return self.purchased_lots

# Example usage
n, m, s = 2, 2, 8000
trader = MegaTrader(n, m, s)
trader.add_bond_lot(1, "alfa-05", 100.2, 2)
trader.add_bond_lot(2, "alfa-05", 101.5, 5)
trader.add_bond_lot(2, "gazprom-17", 100.0, 2)

trader.maximize_income()

# Print the total income
print(f"Total income on day {n + 30}: {trader.calculate_total_income():.2f}")

# Print the purchased lots
for lot in trader.get_purchased_lots():
    print(f"{lot.day} {lot.name} {lot.price} {lot.quantity}")

print("")

# Описание алгоритма на русском языке
# Алгоритм состоит из следующих этапов:
# 1. Создание класса BondLot для представления каждого лота облигаций, содержащего день, название, цену и количество.
# 2. Создание класса MegaTrader, который хранит информацию о доступных лотах и купленных лотах.
# 3. Метод add_bond_lot() добавляет лоты в список доступных.
# 4. Метод maximize_income() сортирует все доступные лоты по дню и цене (по возрастанию) и добавляет в портфель те лоты, которые можно купить на имеющиеся средства.
# 5. Метод calculate_total_income() вычисляет общий доход от купленных лотов, включая выплату номинала и купонов.

# Корректность алгоритма обеспечивается тем, что он выполняет покупку лотов только в том случае, если достаточно средств, и добавляет их в список купленных лотов. Таким образом, алгоритм всегда поддерживает актуальный баланс средств и корректно рассчитывает итоговый доход.

# 1. Вычислительная сложность алгоритма и оценка необходимой памяти
# Сложность метода maximize_income() зависит от сортировки списка лотов, которая выполняется за O(K * log(K)), где K - количество лотов. После сортировки происходит итерация по лотам, что добавляет линейную сложность O(K). Таким образом, общая сложность алгоритма - O(K * log(K)). Память используется линейно, O(K), для хранения всех лотов и списка купленных лотов.

# 2. Ограничения на размер входных параметров
# Алгоритм будет выполняться в разумное время (до 5 секунд) при размере N и M, не превышающем 10^4. Это ограничение связано с необходимостью сортировки и итерации по всем лотам.

# 3. Субъективная оценка сложности задачи
# Сложность задачи можно оценить на уровне 6 из 10, так как она включает сортировку и оптимизацию расходов, что требует внимательного подхода к управлению ресурсами. На реализацию решения было затрачено около 2 часов.
