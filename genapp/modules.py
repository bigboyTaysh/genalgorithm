from decimal import Decimal
import random
import math
import logging
from genapp.models import Individual 

logger = logging.getLogger(__name__)

def random_real(rangeA, rangeB, precision):
    precision = pow(10,Decimal(precision))
    return Decimal(random.randrange(rangeA * precision, (rangeB) * precision + 1))/precision

def power_of_2(rangeA, rangeB, precision):
    return math.ceil(math.log(((rangeB - rangeA) * (1/pow(10,Decimal(-precision))) + 1), 2))

def real_to_int(real, rangeA, rangeB, power):
    return round((1/(rangeB-rangeA)) * (real - rangeA) * ((pow(2, power)-1)))

def bin_to_int(binary):
    return int(str(binary),2)

def int_to_bin(integer, power):
    return format(integer, '0' + str(power) + 'b')

def int_to_real(integer, rangeA, rangeB, precision, power):
    return round(rangeA + ((rangeB - rangeA) * integer)/(pow(2, power)-1), precision)

def func(real, precision):
    #format_str = '%.' + str(precision) + 'f'
    fraction, integer = math.modf(real)
    #return format(format_str % fx)
    return round(fraction, precision) * (math.cos(20 * Decimal(math.pi) * real) - math.sin(real))

def get_individual(rangeA, rangeB, precision, power):
    real = random_real(rangeA, rangeB, precision)
    int_from_real = real_to_int(real, rangeA, rangeB, power)
    binary = int_to_bin(int_from_real, power)
    int_from_bin =  bin_to_int(binary)
    real_from_int = int_to_real(int_from_bin, rangeA, rangeB, precision, power)

    return Individual(
        real=real,
        int_from_real=int_from_real,
        binary=binary,
        int_from_bin=int_from_bin,
        real_from_int=real_from_int,
        fx=func(real, precision))

def get_individual_array(rangeA, rangeB, precision, power, population):
    array = []
    for x in range(population):
        array.append(get_individual(rangeA, rangeB, precision, power))

    return array