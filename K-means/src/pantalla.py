import re
import os
import pandas as pd
import numpy as np
import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter import messagebox
from ttkbootstrap.constants import *
import Kmeans as means

class Pantalla(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill = BOTH, expand = YES)
        self.train_csv_path = None
        self.test_csv_path = None
        self.best_k = None
        
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
        self.k_entry = None
        self.Create_Read_DB_Fields()

        # Show register frame
        self.Show_Lf("READ")
        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())
    # end __init__

    def Create_Read_DB_Fields(self):
        read_db_frame = ttk.Frame(self.frames["READ"])
        read_db_frame.pack(fill = X, expand = YES, anchor="nw")
        read_db_btn = ttk.Button(read_db_frame, 
            text="Agrupar", 
            command=lambda: self.Train_DB()
        )
        read_db_btn.configure(style="success.TButton")
        read_db_btn.grid(row=1, column=2, padx=5)
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
        entry = ttk.Entry(read_db_frame, width=4)
        entry.grid(row=1, column=1, sticky="w", padx=5)
        self.k_entry = entry
    # end Create_Read_DB_Fields

    def Show_Lf(self, lf_name):
        frame = self.frames[lf_name]
        frame.tkraise()

    def Select_Train_CSV(self, label):
        home_dir = os.path.expanduser("~")
        doc_dir = os.path.join(home_dir, "Documents")
        csv_path = filedialog.askopenfilename(
            initialdir = doc_dir,
            title = "Seleccionar database",
            filetypes = (("Archivos CSV y DATA", "*.csv, *.data"), ("Todos los archivos", "*.*"))
        )
        if os.path.isfile(csv_path):
            self.train_csv_path = csv_path
            label.configure(text = csv_path.split("/")[-1])
        else:
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            label.configure(text = '')
    # end Read_Train_CSV

    def Train_DB(self):
        path = self.train_csv_path
        if path == None or (not path.endswith(".csv") and not path.endswith(".data") ):
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            return
        k = self.k_entry.get()
        df = means.clust(path, int(k))
        home_dir = os.path.expanduser("~")
        doc_dir = os.path.join(home_dir, "Documents")
        df.to_csv(os.path.join(doc_dir, "clustered.csv"), index=False)
        messagebox.showinfo("Info", "Agrupamiento terminado\nArchivo guardado en Documents/clustered.csv")

        self.read_db_btn.configure(text="Done")
        return
    # end read_db