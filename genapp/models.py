from django.db import models


class Individual(models.Model):
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
