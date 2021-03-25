from decimal import Decimal
import random
import math
import logging
from genapp.models import Individual
from operator import attrgetter
from copy import deepcopy, copy
import bisect
import numpy as np
import time
import ujson
import _pickle as cPickle

logger = logging.getLogger(__name__)


def random_real(range_a, range_b, precision):
    prec = pow(10, Decimal(precision))
    return round(Decimal(random.randrange(range_a * prec, (range_b) * prec + 1))/prec, precision)


def power_of_2(range_a, range_b, precision):
    return math.ceil(math.log(((range_b - range_a) * (1/pow(10, Decimal(-precision))) + 1), 2))


def real_to_int(real, range_a, range_b, power):
    return round((1/(range_b-range_a)) * (real - range_a) * ((pow(2, power)-1)))


def bin_to_int(binary):
    return int(str(binary), 2)


def int_to_bin(integer, power):
    return format(integer, '0' + str(power) + 'b')


def int_to_real(integer, range_a, range_b, precision, power):
    return round(range_a + ((range_b - range_a) * integer)/(pow(2, power)-1), precision)


def func(real, precision):
    #format_str = '%.' + str(precision) + 'f'
    fraction = math.modf(real)[0]
    # return format(format_str % fx)
    return round(fraction, precision) * (math.cos(20 * Decimal(math.pi) * real) - math.sin(real))


def get_individual(range_a, range_b, precision, power):
    real = random_real(range_a, range_b, precision)
    int_from_real = real_to_int(real, range_a, range_b, power)
    binary = int_to_bin(int_from_real, power)
    int_from_bin = bin_to_int(binary)
    real_from_int = int_to_real(
        int_from_bin, range_a, range_b, precision, power)

    return Individual(
        real=real,
        int_from_real=int_from_real,
        binary=binary,
        int_from_bin=int_from_bin,
        real_from_int=real_from_int,
        fx=func(real, precision))


def get_individual_from_binary(binary, range_a, range_b, precision, power):
    int_from_bin = bin_to_int(binary)
    real_from_int = int_to_real(
        int_from_bin, range_a, range_b, precision, power)
    real = real_from_int
    int_from_real = real_to_int(real, range_a, range_b, power)

    return Individual(
        real=real,
        int_from_real=int_from_real,
        binary=binary,
        int_from_bin=int_from_bin,
        real_from_int=real_from_int,
        fx=func(real, precision))


def get_individuals_array(range_a, range_b, precision, population, power):
    individuals = []

    for i in range(population):
        individuals.append(get_individual(range_a, range_b, precision, power))

    return individuals


def selection_of_individuals(individuals, precision):
    len_individuals = len(individuals)
    fx_min = min(individuals, key=attrgetter('fx')).fx

    for individual in individuals:
        individual.gx = individual.fx - fx_min + pow(10, -precision)

    sum_gx = sum(individual.gx for individual in individuals)

    for individual in individuals:
        individual.px = individual.gx / sum_gx

    individuals[0].qx = individuals[0].px
    for i in range(1, len_individuals):
        individuals[i].qx = individuals[i].px + individuals[i-1].qx
        individuals[i].px = individuals[i].gx / sum_gx

    randoms = np.random.default_rng().uniform(0,1,len_individuals)

    selected_individuals = []
    for i in range(0, len_individuals):
        location = bisect.bisect_right(individuals, randoms[i])
        selected_individuals.append(copy(individuals[location]))

    return randoms.tolist(), selected_individuals


def crossover(individuals, crossover_probability, range_a, range_b, precision, power):
    parents = []

    for individual in individuals:
        if (random.random() < crossover_probability):
            individual.is_parent = True
            parents.append(individual)
        else:
            individual.is_parent = False
            individual.cross_population = individual.binary

    len_parents = len(parents)
    if len_parents > 1:
        if len_parents % 2 == 0:
            for i in range(0, len_parents, 2):
                crossover_of_individuals(parents[i], parents[i+1])
        else:
            for i in range(0, len_parents-1, 2):
                crossover_of_individuals(parents[i], parents[i+1])
            crossover_of_individuals(parents[random.randrange(
                0, len_parents-1)], parents[len_parents-1])
    else: 
        individuals[0].cross_population = individuals[0].binary


def crossover_of_individuals(individual_1, individual_2):
    crossover_point = random.randrange(1, len(individual_1.binary))
    if individual_1.crossover_points:
        individual_1.crossover_points += ", "
        individual_1.crossover_points += str(crossover_point)
    else:
        individual_1.crossover_points += str(crossover_point)
        individual_1.child_binary = individual_1.binary[:crossover_point] + \
            individual_2.binary[crossover_point:]
        individual_1.cross_population = individual_1.child_binary
    individual_2.crossover_points += str(crossover_point)
    individual_2.child_binary = individual_2.binary[:crossover_point] + \
        individual_1.binary[crossover_point:]
    individual_2.cross_population = individual_2.child_binary


def mutation_of_individuals(individuals, probability_of_mutation):
    for individual in individuals:
        individual.mutant_population = individual.cross_population
        for i in range(0, len(individual.mutant_population)):
            if(random.random() < probability_of_mutation):
                individual.mutant_population = individual.mutant_population[:i] + (
                    str(1 - int(individual.mutant_population[i]))) + individual.mutant_population[i+1:]
                if individual.mutation_points:
                    individual.mutation_points += ", "
                    individual.mutation_points += str(i+1)
                else:
                    individual.mutation_points += str(i+1)
