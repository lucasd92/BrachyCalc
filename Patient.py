class Paciente:
    """
    Información del Paciente: Nombre, ID, fecha del reporte
    """
    def __init__(self, nombre_paciente, id_paciente, dia_reporte):
        self.nombre_paciente = nombre_paciente
        self.id_paciente = id_paciente
        self.dia_reporte = dia_reporte