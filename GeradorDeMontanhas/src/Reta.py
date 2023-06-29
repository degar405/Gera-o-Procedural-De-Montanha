from math import sqrt, pow

class Reta:
    def __init__(self, origem, p1):
        (x0, y0, z0) = origem
        (x1, y1, z1) = p1
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.a = x1 - self.x0
        self.b = y1 - self.y0
        self.c = z1 - self.z0
        distanciap1 = sqrt(pow(self.a, 2) + pow(self.b, 2))
        self.aProp = (z1 - z0)/distanciap1

    def calcularZ(self, x, y):
        t = 0
        if self.a != 0:
            t = (x - self.x0)/self.a
        elif self.b != 0:
            t = (y - self.y0)/self.b

        z = self.z0 + (t * self.c)
        return z
    
    def calcularZaPartirDaDistancia(self, x, y):
        distanciaPonto = sqrt(pow(x - self.x0, 2) + pow(y - self.y0, 2))
        z = (self.aProp * distanciaPonto) + self.z0

        return z

