from decimal import Decimal
import random
from math import ceil, log, modf, cos, pi, sin
from genapp.models import Individual, Generation, Test
from operator import attrgetter
from copy import deepcopy, copy
import bisect
import numpy
import time
import csv

def random_real(range_a, range_b, precision):
    prec = pow(10, precision)
    return round(random.randrange(range_a * prec, (range_b) * prec + 1)/prec, precision)


def power_of_2(range_a, range_b, precision):
    return ceil(log(((range_b - range_a) * (1/pow(10, -precision)) + 1), 2))


def real_to_int(real, range_a, range_b, power):
    return round((1/(range_b-range_a)) * (real - range_a) * ((pow(2, power)-1)))


def bin_to_int(binary):
    return int(str(binary), 2)


def int_to_bin(integer, power):
    return format(integer, '0' + str(power) + 'b')


def int_to_real(integer, range_a, range_b, precision, power):
    return round(range_a + ((range_b - range_a) * integer)/(pow(2, power)-1), precision)


def func(real, precision):
    return round(modf(real)[0], precision) * (cos(20 * pi * real) - sin(real))


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

    return Individual(
        real=real_from_int,
        int_from_real=int_from_bin,
        binary=binary,
        int_from_bin=int_from_bin,
        real_from_int=real_from_int,
        fx=func(real_from_int, precision))


def get_individuals_array(range_a, range_b, precision, population_size, power):
    individuals = numpy.empty(population_size, dtype=object)

    for i in range(population_size):
        individuals[i] = get_individual(range_a, range_b, precision, power)

    return individuals


def selection_of_individuals(individuals, precision):
    len_individuals = len(individuals)
    fx_min = min(individual.fx for individual in individuals)

    precision_var = pow(10, -precision)

    for i in range(0, len_individuals):
        individuals[i].gx = individuals[i].fx - fx_min + precision_var

    sum_gx = numpy.sum(individual.gx for individual in individuals)
    selected_individuals = numpy.empty(len_individuals, dtype=Individual)

    individuals[0].px = individuals[0].gx / sum_gx
    individuals[0].qx = individuals[0].px

    for i in range(1, len_individuals):
        individuals[i].qx = individuals[i].gx / sum_gx + individuals[i-1].qx
        individuals[i].px = individuals[i].gx / sum_gx

    for i in range(0, len_individuals):
        individuals[i].random = random.random()
        selected_individuals[i] = copy(individuals[numpy.searchsorted(
            individuals, individuals[i].random, side='right')])

    return selected_individuals


def crossover(individuals, crossover_probability, power):
    parents = []

    for individual in individuals:
        if random.random() <= crossover_probability:
            individual.is_parent = True
            parents.append(individual)
        else:
            individual.cross_population = individual.binary

    len_parents = len(parents)

    if len_parents > 1:
        if len_parents % 2 == 0:
            for i in range(0, len_parents, 2):
                crossover_of_individuals(parents[i], parents[i+1], power)
        else:
            for i in range(0, len_parents-1, 2):
                crossover_of_individuals(parents[i], parents[i+1], power)
            crossover_of_individuals(parents[0], parents[len_parents-1], power)
    elif len_parents == 1:
        parents[0].is_parent = False
        parents[0].cross_population = parents[0].binary


def crossover_of_individuals(individual_1, individual_2, power):
    crossover_point = random.randrange(1, power)
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


def mutation(individuals, mutation_probability, power):
    for individual in individuals:
        individual.mutant_population = individual.cross_population
        for i in range(0, power):
            if random.random() <= mutation_probability:
                individual.mutant_population = individual.mutant_population[:i] + (
                    str(1 - int(individual.mutant_population[i]))) + individual.mutant_population[i+1:]
                if individual.mutation_points:
                    individual.mutation_points += ", "
                    individual.mutation_points += str(i+1)
                else:
                    individual.mutation_points += str(i+1)


def evolution(range_a, range_b, precision, population_size, generations_number, crossover_probability, mutation_probability, elite_number, save_file=True):
    generations = numpy.empty(generations_number, dtype=object)
    population = numpy.empty(population_size, dtype=object)

    power = power_of_2(range_a, range_b, precision)

    individuals = get_individuals_array(
        range_a, range_b, precision, population_size, power)

    if elite_number:
        elite = copy(max(individuals, key=attrgetter('fx')))

    selected_individuals = selection_of_individuals(
        individuals, precision)

    crossover(selected_individuals, crossover_probability, power)

    mutation(
        selected_individuals, mutation_probability, power)

    for i in range(0, population_size):
        population[i] = get_individual_from_binary(
            selected_individuals[i].mutant_population, range_a, range_b, precision, power)

    generation = Generation()

    if elite_number:
        if not any(individual.real == elite.real for individual in population):
            index = random.randrange(0, population_size)
            if population[index].fx < elite.fx:
                population[index] = elite

    generation.individuals = population
    generation.fmin = min(
        individual.fx for individual in generation.individuals)
    generation.fmax = max(
        individual.fx for individual in generation.individuals)
    generation.favg = sum(
        individual.fx for individual in generation.individuals) / population_size
    generations[0] = generation

    get_generations(generations, generations_number, range_a, range_b, precision,
                    population_size, power, crossover_probability, mutation_probability, elite_number)

    if save_file:
        with open('staticfiles/generations_history.csv', 'w', newline='', encoding='utf8') as history_csvfile, \
                open('staticfiles/generations_summary.csv', 'w', newline='', encoding='utf8') as summary_csvfile:
            history_writer = csv.writer(
                history_csvfile, delimiter=';', dialect=csv.excel)
            summary_writer = csv.writer(
                summary_csvfile, delimiter=';', dialect=csv.excel)

            history_writer.writerow(['Parametry'])
            history_writer.writerow(['Precyzja: 10^-%d' % precision])
            history_writer.writerow(['Populacja: %d' % population_size])
            history_writer.writerow(['Pokolenia: %d' % generations_number])
            history_writer.writerow(
                ['P. krzyzowania: %g%%' % (crossover_probability*100)])
            history_writer.writerow(['P. mutacji: %g%%' %
                                     (mutation_probability*100)])

            summary_writer.writerow(['Parametry'])
            summary_writer.writerow(['Precyzja: 10^-%d' % precision])
            summary_writer.writerow(['Populacja: %d' % population_size])
            summary_writer.writerow(['Pokolenia: %d' % generations_number])
            summary_writer.writerow(
                ['P. krzyzowania: %g%%' % (crossover_probability*100)])
            summary_writer.writerow(['P. mutacji: %g%%' %
                                     (mutation_probability*100)])
            summary_writer.writerow(['Pokolenie', 'fmin', 'favg', 'fmax'])

            for gen_num, generation in enumerate(generations, start=1):
                summary_writer.writerow(
                    [gen_num, generation.fmin, generation.favg, generation.fmax])

                history_writer.writerow(['Pokolenie %d' % gen_num])
                history_writer.writerow(['', 'Xreal', 'Xbin', 'f(x)'])

                for pop_num, individual in enumerate(generation.individuals, start=1):
                    history_writer.writerow(
                        [pop_num, individual.real,  "'%s'" % individual.binary, individual.fx])

                history_writer.writerow([])

    return generations


def get_generations(generations, generations_number, range_a, range_b, precision, population_size, power, crossover_probability, mutation_probability, elite_number):
    for gereration_number in range(1, generations_number):
        if elite_number:
            elite = copy(
                max(generations[gereration_number - 1].individuals, key=attrgetter('fx')))

        selected_individuals = selection_of_individuals(
            generations[gereration_number - 1].individuals, precision)

        crossover(selected_individuals, crossover_probability, power)

        mutation(
            selected_individuals, mutation_probability, power)

        generation = Generation(numpy.empty(population_size, dtype=Individual))

        for i in range(0, population_size):
            generation.individuals[i] = get_individual_from_binary(
                selected_individuals[i].mutant_population, range_a, range_b, precision, power)

        if elite_number:
            if not any(individual.real == elite.real for individual in generation.individuals):
                index = random.randrange(0, population_size)
                if generation.individuals[index].fx < elite.fx:
                    generation.individuals[index] = elite

        generation.fmin = min(
            individual.fx for individual in generation.individuals)
        generation.fmax = max(
            individual.fx for individual in generation.individuals)
        generation.favg = numpy.sum(
            individual.fx for individual in generation.individuals) / population_size

        generations[gereration_number] = generation


def test(tests_number, precision):
    tests = []

    for generations_number in range(50, 151, 10):
        print(generations_number)
        for population_size in range(30, 81, 5):
            for crossover_probability in numpy.around(numpy.arange(0.5, 0.91, 0.05), 2):
                    generations = []
                    
                    for test in range(0, tests_number):
                        mutation_probability = 0.0001
                        generations.append(evolution(-4.0, 12.0, precision, population_size, generations_number,
                                                 float(crossover_probability), float(mutation_probability), 1, False))
                    tests.append(Test(generations_number, population_size, crossover_probability, mutation_probability, sum(
                        generation[-1].favg for generation in generations)/tests_number, max(generation[-1].fmax for generation in generations)))
                    
                    for mutation_probability in numpy.around(numpy.arange(0.0005, 0.0101, 0.0005), 4):
                        generations = []
                        for test in range(0, tests_number):
                            generations.append(evolution(-4.0, 12.0, precision, population_size, generations_number,
                                                         float(crossover_probability), float(mutation_probability), 1, False))
                        tests.append(Test(generations_number, population_size, crossover_probability, mutation_probability, sum(
                            generation[-1].favg for generation in generations)/tests_number, max(generation[-1].fmax for generation in generations)))

    return tests