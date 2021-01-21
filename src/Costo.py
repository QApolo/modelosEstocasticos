class CostoFijo:
    def __init__(self, depreciacion, inversion, seguro, mantenimiento):
        self.depreciacion = depreciacion
        self.inversion = inversion
        self.seguro = seguro
        self.mantenimiento = mantenimiento
    def getHoraActiva(self):
        return self.depreciacion + self.inversion + self.seguro + self.mantenimiento
    def getHoraInactiva(self):
        return self.depreciacion + self.inversion + self.seguro + self.mantenimiento * 0.75
    def getHoraReserva(self):
        return self.depreciacion + self.inversion + self.seguro + self.mantenimiento * 0.15

class CostoConsumo:
    def __init__(self, combustible, lubricante, llantas, especiales):
        self.combustible = combustible
        self.lubricante = lubricante
        self.llantas = llantas
        self.especiales = especiales
    def getHoraActiva(self):
        return self.combustible + self.lubricante + self.llantas + self.especiales
    def getHoraInactiva(self):
        return self.lubricante + self.llantas
    def getHoraReserva(self):
        return self.lubricante + self.llantas

class CostoOperacion:
    def __init__(self, salario_real):
        self.salario_real = salario_real

    def getHoraActiva(self):
        return self.salario_real
    def getHoraInactiva(self):
        return self.salario_real
    def getHoraReserva(self):
        return 0
    
class CostosDirectos:
    def __init__(self, costos_fijos: CostoFijo, costos_consumo: CostoConsumo, costos_operacion: CostoOperacion):
        self.horas_activas = costos_fijos.getHoraActiva() + costos_consumo.getHoraActiva() + costos_operacion.getHoraActiva()
        self.horas_inactivas = costos_fijos.getHoraInactiva() + costos_consumo.getHoraInactiva() + costos_operacion.getHoraInactiva()
        self.horas_reserva = costos_fijos.getHoraReserva() + costos_consumo.getHoraReserva() + costos_operacion.getHoraReserva()
    def getHoraActiva(self):
        return self.horas_activas
    def getHoraInactiva(self):
        return self.horas_inactivas
    def getHoraReserva(self):
        return self.horas_reserva
    def sumAllHora(self):
        return self.getHoraActiva() + self.getHoraInactiva() + self.getHoraReserva()