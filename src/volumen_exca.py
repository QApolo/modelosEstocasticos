
class VolumenExcavacion:
    def __init__(self, lado: float, ed: float, tn: list, sr: list):

        self.lado = lado
        self.ed = ed    
        self.tn = tn
        self.sr = sr

        self.calcular()

    def calcular(self):
        self.getCT()
        self.getHx()
        self.getH_prom()
        
    def getArea(self):
        return self.lado ** 2

    def getCT(self):
        #if self.ct == None:
        self.ct = [tni-self.ed for tni in self.tn]
        return self.ct
    
    def getHx(self):
        #if self.hx == None:        
        self.hx = [sri - cti for (sri, cti) in zip(self.sr, self.ct)]
        return self.hx

    def getH_prom(self):
        #if self.positivo_hx == None:
        self.positivo_hx = [abs(hi) for hi in self.hx]
        return sum(self.positivo_hx) / 4.0

    def getVolumen(self):
        return self.getH_prom() * self.getArea()

    