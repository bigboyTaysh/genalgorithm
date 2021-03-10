from decimal import Decimal
import random
import math
import logging

logger = logging.getLogger(__name__)

def power_of_2(rangeA, rangeB, precision):
    return math.ceil(math.log(((rangeB - rangeA) * (1/pow(10,Decimal(-precision))) + 1), 2))
def random_rel(rangeA, rangeB, precision):
    return Decimal(random.randrange(rangeA, rangeB + 1))/pow(10,Decimal(precision))
def real_to_int(real, rangeA, rangeB, precision):
    return round((1/(rangeB-rangeA)) * (real - rangeA) * ((pow(2, power_of_2(rangeA, rangeB, precision))-1)))
def bin_to_int(binary):
    return int(str(binary),2)
