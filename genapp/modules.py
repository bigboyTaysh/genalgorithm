import decimal
import random

class Modules():
    def power_of_2(self, rangeA, rangeB, precision):
        interval = (rangeB - rangeA) * pow(2, precision)
        return 1 if interval == 0 else 2**(interval - 1).bit_length()
    def random(self, rangeA, rangeB, precision):
        return decimal.Decimal(random.randrange(rangeA, rangeB + 1))/pow(10,decimal.Decimal(precision))
    def rel_to_int(self, rel, rangeA, rangeB, precision):
        return (1/(rangeB-rangeA)) * (rel - rangeA) * (pow(2, precision))