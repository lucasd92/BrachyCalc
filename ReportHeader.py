class ReportHeader:
    """
    Información del Paciente: Nombre, ID, fecha del reporte
    """
    def __init__(self, document_title = None, main_title = None, sub_title = None, aditional_data = None,
    table_title = None, table_header = [['','','','','',''],], logo_path = 'logo.png'):
        self.document_title = document_title
        self.main_title = main_title
        self.sub_title = sub_title
        self.aditional_data = aditional_data
        self.table_title = table_title
        self.table_header = table_header
        self.logo_path = logo_path