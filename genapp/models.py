class Individual:
    '''
    real = models.DecimalField(max_digits=30, decimal_places=20)
    int_from_real = models.IntegerField()
    binary = models.CharField(max_length=30)
    int_from_bin = models.IntegerField()
    real_from_int = models.DecimalField(max_digits=30, decimal_places=20)
    fx = models.DecimalField(max_digits=30, decimal_places=20)
    gx = models.DecimalField(max_digits=30, decimal_places=20)
    px = models.DecimalField(max_digits=30, decimal_places=20)
    qx = models.DecimalField(max_digits=30, decimal_places=20)
    is_parent = models.BooleanField()
    crossover_points = models.CharField(max_length=200)
    child_binary = models.CharField(max_length=30)
    cross_population = models.CharField(max_length=30)
    mutation_points = models.CharField(max_length=30)
    mutant_population = models.CharField(max_length=30)

    def __lt__(self, other):
        return self.qx < other

    def __gt__(self, other):
        return self.qx > other


    real = 0
    int_from_real = 0
    binary = ""
    int_from_bin = 0
    real_from_int = 0
    fx = 0
    gx = 0
    px = 0
    qx = 0
    is_parent = False
    crossover_points = ""
    child_binary = ""
    cross_population = ""
    mutation_points = ""
'''  
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
