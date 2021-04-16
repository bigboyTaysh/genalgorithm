class Individual:
    def __init__(self, real, int_from_real,
                 binary, int_from_bin, real_from_int, fx,
                 gx=None, px=None, qx=None, random=None, is_parent=False, crossover_points="",
                 child_binary=None, cross_population=None, mutation_points="",
                 mutant_population=None):
        self.real = real
        self.int_from_real = int_from_real
        self.binary = binary
        self.int_from_bin = int_from_bin
        self.real_from_int = real_from_int
        self.fx = fx
        self.gx = gx
        self.px = px
        self.qx = qx
        self.random = random
        self.is_parent = is_parent
        self.crossover_points = crossover_points
        self.child_binary = child_binary
        self.cross_population = cross_population
        self.mutation_points = mutation_points
        self.mutant_population = mutant_population

    def __lt__(self, other):
        return self.qx < other

    def __gt__(self, other):
        return self.qx > other


class Generation:
    def __init__(self, individuals=[], fmin=None, favg=None, fmax=None):
        self.individuals = individuals
        self.fmin = fmin
        self.favg = favg
        self.fmax = fmax

class Test:
    def __init__(self, generations_number, population_size, crossover_probability, mutation_probability, favg, fmax):
        self.generations_number = generations_number
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.favg = favg
        self.fmax = fmax
