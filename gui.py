import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from gui_actions import btn_cpr_onClick,btn_dtr_onClick,btn_calc_onClick,btn_report_onClick


class App:
    def __init__(self, root):
        #setting title
        root.title("TG-43 based independent calculation")
        #setting window size
        width=576
        height=300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        style = ttk.Style()
        style.theme_use('clam')
        
        lbl_dtr=ttk.Label(root)
        ft = tkFont.Font(family='Times',size=12)
        lbl_dtr["font"] = ft
        lbl_dtr["justify"] = "center"
        lbl_dtr["text"] = "Dwell time report"
        lbl_dtr.place(x=30,y=20,width=119,height=30)

        self.ent_dtr=ttk.Entry(root)
        ft = tkFont.Font(family='Times',size=10)
        self.ent_dtr["font"] = ft
        self.ent_dtr["justify"] = "center"
        self.ent_dtr.place(x=30,y=50,width=370,height=30)

        btn_dtr=ttk.Button(root)
        ft = tkFont.Font(family='Times',size=10)
        btn_dtr["text"] = "Browse"
        btn_dtr.place(x=420,y=50,width=100,height=30)
        btn_dtr["command"] = lambda: btn_dtr_onClick(self)

        lbl_cpr=ttk.Label(root)
        ft = tkFont.Font(family='Times',size=12)
        lbl_cpr["font"] = ft
        lbl_cpr["justify"] = "center"
        lbl_cpr["text"] = "Control points report"
        lbl_cpr.place(x=30,y=90,width=151,height=30)

        self.ent_cpr=ttk.Entry(root)
        ft = tkFont.Font(family='Times',size=10)
        self.ent_cpr["font"] = ft
        self.ent_cpr["justify"] = "center"
        self.ent_cpr.place(x=30,y=120,width=370,height=30)

        btn_cpr=ttk.Button(root)
        ft = tkFont.Font(family='Times',size=10)
        btn_cpr["text"] = "Browse"
        btn_cpr.place(x=420,y=120,width=100,height=30)
        btn_cpr["command"] = lambda: btn_cpr_onClick(self)

        btn_calc=ttk.Button(root)
        ft = tkFont.Font(family='Times',size=10)
        btn_calc["text"] = "Calculate"
        btn_calc.place(x=30,y=230,width=178,height=36)
        btn_calc["command"] =lambda: btn_calc_onClick(self)

        btn_report=ttk.Button(root)
        ft = tkFont.Font(family='Times',size=10)
        btn_report["text"] = "Report"
        btn_report.place(x=342,y=230,width=178,height=36)
        btn_report["command"] =lambda: btn_report_onClick(self)

        lbl_date=ttk.Label(root)
        ft = tkFont.Font(family='Times',size=12)
        lbl_date["font"] = ft
        lbl_date["justify"] = "center"
        lbl_date["text"] = "Date dd/mm/yy"
        lbl_date.place(x=30,y=170,width=120,height=30)

        self.ent_date=ttk.Entry(root)
        ft = tkFont.Font(family='Times',size=10)
        self.ent_date["font"] = ft
        self.ent_date["justify"] = "center"
        self.ent_date.place(x=160,y=170,width=161,height=30)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
