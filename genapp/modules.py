from decimal import Decimal
import random
import math
import logging

logger = logging.getLogger(__name__)

def power_of_2(rangeA, rangeB, precision):
    return math.ceil(math.log(((rangeB - rangeA) * (1/pow(10,Decimal(-precision))) + 1), 2))
def random_rel(rangeA, rangeB, precision):
    return Decimal(random.randrange(rangeA, rangeB + 1))/pow(10,Decimal(precision))
def rel_to_int(rel, rangeA, rangeB, precision):
    return (1/(rangeB-rangeA)) * (rel - rangeA) * (pow(2, precision))