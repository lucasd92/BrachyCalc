import datetime as date
from datetime import datetime
import numpy as np
from tkinter import filedialog as fd
from tkinter import messagebox
from parse_reports import parse_dwell_times
from parse_reports import parse_control_points
from tg_43_calcule import dose_calculation
from Patient import Paciente
from ReportHeader import ReportHeader
from print_report import print_report

def _openAndParseReports(self):
    error_flag = 0
    try:
        treatment_date = date.datetime.strptime(self.ent_date.get(), '%d/%m/%y')
    except:
        messagebox.showerror(title="Wrong Date", message="Please use dd/mm/yy format")
        error_flag = 1

    try:
        table_dtr,name_dtr,id_dtr,is_right_report_dtr = parse_dwell_times(self.ent_dtr.get())
    except:
        messagebox.showerror(title="Wrong file", message="There is an issue with the dwell times report file or path")
        error_flag = 1

    try:
        table_cpr,name_cpr,id_cpr,is_right_report_cpr = parse_control_points(self.ent_cpr.get())
    except:
        messagebox.showerror(title="Wrong file", message="There is an issue with the control points report file or path")
        error_flag = 1

    if not(is_right_report_dtr) or not(is_right_report_cpr):
        messagebox.showerror(title="Parse", message="Reports can not be parsed")
        error_flag = 1
    if name_cpr != name_dtr:
        messagebox.showerror(title="Wrong report", message="Patient name does not match")
        error_flag = 1
    if id_cpr != id_dtr:
        messagebox.showerror(title="Wrong report", message="Patient ID does not match")
        error_flag = 1
    if error_flag == 1:
        return
    table_dt = np.stack((table_dtr[...,0],table_dtr[...,3],table_dtr[...,4],table_dtr[...,5],table_dtr[...,-1]),axis=-1)
    return name_cpr, id_cpr, treatment_date, table_dt, table_cpr

def btn_dtr_onClick(self):
    filename = fd.askopenfilename(
    title='Open Dwell Time Report',
    initialdir='./',
    filetypes=(('Comma Separated Values','*.csv'),
    ('All files','*.*')))
    self.ent_dtr.delete(0,"end")
    self.ent_dtr.insert(0,filename)


def btn_cpr_onClick(self):
    filename = fd.askopenfilename(
    title='Open Control Points Report',
    initialdir='./',
    filetypes=(('Comma Separated Values','*.csv'),
    ('All files','*.*')))
    self.ent_cpr.delete(0,"end")
    self.ent_cpr.insert(0,filename)

def btn_report_onClick(self):
    try:
        name, id, date, dwell_times_table, control_points_table = _openAndParseReports(self)
    except:
        return

    table_list = []
    for index,point in enumerate(control_points_table):
        dose = np.round(dose_calculation(point[0:3]/10,dwell_times_table,date)/100,2)
        diff = np.round(np.abs((point[-1]-dose)/point[-1])*100,2)
        table_list.append([str(point[0:3]/10), str(dose), str(point[-1]), str(diff)])
    
    paciente = Paciente(name, id, datetime.now().strftime('-%d-%m-%Y'))

    rh = ReportHeader(  document_title = 'CI Braquiterapia',
                        main_title = 'Centro de Medicina Nuclear y Radioterapia',
                        sub_title = 'Pte. Dr. N??stor Kirchner',
                        aditional_data = (paciente.nombre_paciente + ' - ID: ' + paciente.id_paciente + ' ' + paciente.dia_reporte),
                        table_header = [[ 'Punto N??', 'Coordenadas', 'Resultado del \nC??lculo [Gy]', 'Resultado del \nTPS [Gy]', 
                        'Diferencia %', 'Observaciones'],],
                        table_title = 'Resultado del c??lculo independiente de dosis en los puntos de control',
                        logo_path = 'logo.jpg'
    )
    
    try:
        print_report(rh, table_list, './export/' + paciente.id_paciente + paciente.dia_reporte + '.pdf')
        messagebox.showinfo(title='report generated ', message= 'Report: ' + paciente.id_paciente + paciente.dia_reporte + '.pdf' +
        ' was generated')
    except:
        messagebox.showerror(title="Error", message="Could not generate report")
        return



def btn_calc_onClick(self):
    try:
        name, id, date, dwell_times_table, control_points_table = _openAndParseReports(self)
    except:
        return
    
    result = ''
    for index,point in enumerate(control_points_table):
        dose = np.round(dose_calculation(point[0:3]/10,dwell_times_table,date)/100,2)
        result = result + ('El punto ' + str(point[0:3]/10) + ' da ' + str(dose) + ' cGy y deber??a dar: ' + str(point[-1]) + ' cGy\n')

    messagebox.showinfo(title='Calculation for patient ' + name + ', ID: ' + id, message=result)

if __name__ == "__main__":


    treatment_date = date.datetime.strptime('10/10/22', '%d/%m/%y')
    table_dtr,name_dtr,id_dtr,is_right_report_dtr = parse_dwell_times('./SagiPlanReports/fx3dwellp.csv')
    table_cpr,name_cpr,id_cpr,is_right_report_cpr = parse_control_points('./SagiPlanReports/fx3cp.csv')


    table_dt = np.stack((table_dtr[...,0],table_dtr[...,3],table_dtr[...,4],table_dtr[...,5],table_dtr[...,-1]),axis=-1)
    
    name = name_cpr
    id = id_cpr
    date2 = treatment_date
    dwell_times_table = table_dt
    control_points_table = table_cpr

      

    table_list = []
    for index,point in enumerate(control_points_table):
        dose = np.round(dose_calculation(point[0:3]/10,dwell_times_table,date2)/100,2)
        diff = np.round(np.abs((point[-1]-dose)/point[-1])*100,2)
        table_list.append([str(point[0:3]/10), str(dose), str(point[-1]), str(diff)])
    
    paciente = Paciente(name, id, datetime.now().strftime('-%d-%m-%Y'))

    rh = ReportHeader(  document_title = 'CI Braquiterapia',
                        main_title = 'Centro de Medicina Nuclear y Radioterapia',
                        sub_title = 'Pte. Dr. N??stor Kirchner',
                        aditional_data = (paciente.nombre_paciente + ' - ID: ' + paciente.id_paciente + ' ' + paciente.dia_reporte),
                        table_header = [[ 'Punto N??', 'Coordenadas', 'Resultado del \nC??lculo [Gy]', 'Resultado del \nTPS [Gy]', 
                        'Diferencia %', 'Observaciones'],],
                        table_title = 'Resultado del c??lculo independiente de dosis en los puntos de control',
                        logo_path = 'logo.jpg'
    )
    

    print_report(rh, table_list, './export/' + paciente.id_paciente + paciente.dia_reporte + '.pdf')

         