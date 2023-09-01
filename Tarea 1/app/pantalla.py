import re
import os
import pandas as pd
import numpy as np
import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter import messagebox
from ttkbootstrap.constants import *
import modelo as model

class Pantalla(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill = BOTH, expand = YES)
        self.train_csv_path = None
        self.test_csv_path = None
        self.best_k = None

        # Sidebar frame __init__
        self.sidebar_f = ttk.Frame(self, width = 200)
        self.sidebar_f.pack(side = LEFT, fill = Y, expand = YES, anchor="nw")
        self.sidebar_btns = {}
        self.Create_Sidebar_Btns()
        
        # Main container frame __init__
        main_container = ttk.Frame(self)
        main_container.pack(side = LEFT, expand = YES, anchor="nw", padx=10, pady=5)
        main_container.grid_rowconfigure(0, weight = 1)
        main_container.grid_columnconfigure(0, weight = 1)

        # Main container frame content __init__
        self.frames = {}

        # Read DB frame __init__
        read_db_text           = 'Seleccione la BD para entrenar el modelo'
        read_db_lf             = ttk.Labelframe(main_container, text = read_db_text, padding=(15,10,10,10))
        read_db_lf.configure(style="info.TLabelframe")
        read_db_lf.grid(row = 0, column = 0, sticky = "nsew")
        self.frames["READ"]    = read_db_lf
        self.select_db_btn     = None
        self.read_db_csv_label = None
        self.read_db_btn       = None
        self.read_best_k_label = None
        self.Create_Read_DB_Fields()

        # Test new entry frame __init__
        test_text              = 'Seleccione la DB a clasificar'
        test_lf                = ttk.Labelframe(main_container, text = test_text, padding=(15,10,10,10))
        test_lf.configure(style="info.TLabelframe")
        test_lf.grid(row = 0, column = 0, sticky = "nsew")
        self.frames["TEST"]    = test_lf
        self.select_db_test    = None
        self.test_db_csv_label = None
        self.test_db_btn       = None
        self.Create_Test_Fields()

        # Show register frame
        self.Show_Lf("READ")
        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())
    # end __init__

    def Create_Sidebar_Btns(self):
        register_btn = ttk.Button(
            master=self.sidebar_f,
            text='DB de Entrenamiento',
            bootstyle = PRIMARY,
            command=lambda: self.Show_Lf("READ")
        )
        self.sidebar_btns["READ"] = register_btn
        register_btn.pack(fill = X,  pady = (15,0), padx = (5,0)) 

        modify_btn = ttk.Button(
            master=self.sidebar_f,
            text='DB de Clasificación',
            bootstyle = PRIMARY,
            command=lambda: self.Show_Lf("TEST")
        )
        self.sidebar_btns["TEST"] = modify_btn
        modify_btn.pack(fill = X, pady = (10,0), padx = (5,0))
    # end create_sidebar_btns

    def Create_Read_DB_Fields(self):
        read_db_frame = ttk.Frame(self.frames["READ"])
        read_db_frame.pack(fill = X, expand = YES, anchor="nw")
        read_db_btn = ttk.Button(read_db_frame, 
            text="Entrener", 
            command=lambda: self.Train_DB()
        )
        read_db_btn.configure(style="success.TButton")
        read_db_btn.grid(row=1, column=1, padx=5)
        self.read_db_btn = read_db_btn

        label = ttk.Label(read_db_frame)
        label.grid(row=0, column=0, sticky="w", padx=5)
        self.read_db_csv_label = label
        btn = ttk.Button(read_db_frame,
            text="Seleccionar CSV",
            command=lambda label = label: self.Select_Train_CSV(label)
        )
        btn.grid(row=1, column=0, padx=5)
        btn.configure(style="info.TButton")
        self.select_db_btn = btn
        label = ttk.Label(read_db_frame, text="Mejor K:     ")
        label.grid(row=1, column=3, sticky="w", padx=5)
        self.read_best_k_label = label
    # end Create_Read_DB_Fields

    def Create_Test_Fields(self):
        test_frame = ttk.Frame(self.frames["TEST"])
        test_frame.pack(fill = X, expand = YES, anchor="nw")

        test_db_btn = ttk.Button(test_frame, 
            text="Clasificar Entradas", 
            command=lambda: self.Test_DB()
        )
        test_db_btn.configure(style="success.TButton")
        test_db_btn.grid(row=1, column=1, padx=5)
        self.test_db_btn = test_db_btn

        label = ttk.Label(test_frame)
        label.grid(row=0, column=0, sticky="w", padx=5)
        self.test_db_csv_label = label
        btn = ttk.Button(test_frame,
            text="Seleccionar CSV",
            command=lambda label = label: self.Select_Test_CSV(label)
        )
        btn.grid(row=1, column=0, padx=5)
        btn.configure(style="info.TButton")
        self.select_db_test = btn
    # end Create_Test_Fields

    def Show_Lf(self, lf_name):
        frame = self.frames[lf_name]
        frame.tkraise()
        self.sidebar_btns[lf_name].configure(bootstyle = PRIMARY)
        for key in self.sidebar_btns.keys():
            if key != lf_name:
                self.sidebar_btns[key].configure(bootstyle = OUTLINE)
    # end show_lf

    def Select_Train_CSV(self, label):
        home_dir = os.path.expanduser("~")
        doc_dir = os.path.join(home_dir, "Documents")
        csv_path = filedialog.askopenfilename(
            initialdir = doc_dir,
            title = "Seleccionar archivo CSV",
            filetypes = (("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
        )
        if os.path.isfile(csv_path):
            self.train_csv_path = csv_path
            label.configure(text = csv_path.split("/")[-1])
        else:
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            label.configure(text = '')
    # end Read_Train_CSV

    def Select_Test_CSV(self, label):
        home_dir = os.path.expanduser("~")
        doc_dir = os.path.join(home_dir, "Documents")
        csv_path = filedialog.askopenfilename(
            initialdir = doc_dir,
            title = "Seleccionar archivo CSV",
            filetypes = (("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
        )
        if os.path.isfile(csv_path):
            self.test_csv_path = csv_path
            label.configure(text = csv_path.split("/")[-1])
        else:
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            label.configure(text = '')
    # end Read_Test_CSV

    def Train_DB(self):
        path = self.train_csv_path
        if path == None or not path.endswith(".csv") :
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            return
        self.best_k = model.train(path)
        self.read_db_btn.configure(text="Done")
        self.read_best_k_label.configure(text="Mejor K:    " + str(self.best_k[1]))
        return
    # end read_db

    def Test_DB(self):
        path = self.test_csv_path
        if path == None or not path.endswith(".csv") :
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            return
        model.predict(self.test_csv_path, self.train_csv_path, self.best_k[1])
        self.read_db_btn.configure(text="Done")
        return
    # end read_db