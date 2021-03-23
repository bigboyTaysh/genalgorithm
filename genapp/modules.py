from decimal import Decimal
import random
import math
import logging
from genapp.models import Individual 
from operator import attrgetter

logger = logging.getLogger(__name__)

def random_real(range_a, range_b, precision):
    prec = pow(10,Decimal(precision))
    return round(Decimal(random.randrange(range_a * prec, (range_b) * prec + 1))/prec, precision)

def power_of_2(range_a, range_b, precision):
    return math.ceil(math.log(((range_b - range_a) * (1/pow(10,Decimal(-precision))) + 1), 2))

def real_to_int(real, range_a, range_b, power):
    return round((1/(range_b-range_a)) * (real - range_a) * ((pow(2, power)-1)))

def bin_to_int(binary):
    return int(str(binary),2)

def int_to_bin(integer, power):
    return format(integer, '0' + str(power) + 'b')

def int_to_real(integer, range_a, range_b, precision, power):
    return round(range_a + ((range_b - range_a) * integer)/(pow(2, power)-1), precision)

def func(real, precision):
    #format_str = '%.' + str(precision) + 'f'
    fraction = math.modf(real)[0]
    #return format(format_str % fx)
    return round(fraction, precision) * (math.cos(20 * Decimal(math.pi) * real) - math.sin(real))

def get_individual(range_a, range_b, precision, power):
    real = random_real(range_a, range_b, precision)
    int_from_real = real_to_int(real, range_a, range_b, power)
    binary = int_to_bin(int_from_real, power)
    int_from_bin =  bin_to_int(binary)
    real_from_int = int_to_real(int_from_bin, range_a, range_b, precision, power)

    return Individual(
        real=real,
        int_from_real=int_from_real,
        binary=binary,
        int_from_bin=int_from_bin,
        real_from_int=real_from_int,
        fx=func(real, precision))

def get_individuals_array(range_a, range_b, precision, population):
    individuals = []
    power = power_of_2(range_a, range_b, precision)
    
    for x in range(population):
        individuals.append(get_individual(range_a, range_b, precision, power))

    return individuals

def selection_of_individuals(individuals, precision):
    fx_min = min(individuals, key=attrgetter('fx')).fx

    for individual in individuals:
        individual.gx = individual.fx - fx_min + pow(10,-precision)
    
    sum_gx = sum(individual.gx for individual in individuals)
    
    for individual in individuals:
        individual.px = individual.gx / sum_gx

    individuals[0].qx = individuals[0].px
    for i in range(1, len(individuals)):
        individuals[i].qx = individuals[i].px + individuals[i-1].qx

    for individual in individuals:
        individual.px = individual.gx / sum_gx

    randoms = []
    for i in range(0, len(individuals)):
        randoms.append(random.random())

    selected_individuals = []
    for i in range(0, len(randoms)):
        for j in range(0, len(individuals)):
            if(randoms[i] <= individuals[j].qx):
                selected_individuals.append(individuals[j])
                break

    return randoms, selected_individuals

def crossover_of_individuals(individuals, crossover_probability):
    for i in range(0, len(individuals)):
        if (random.random() < crossover_probability):
            individuals[i].is_parent = True
        else:
            individuals[i].is_parent = False