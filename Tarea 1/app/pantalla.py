import re
import os
import pandas as pd
import numpy as np
import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter import messagebox
from ttkbootstrap.constants import *
import functions as func
import modelo as model

class Pantalla(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill = BOTH, expand = YES)
        self.parameters_keys = func.get_Keys()
        self.csv_path = None
        self.best_k = 0

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
        read_db_text           = 'Complete los campos leer la BD y entrenar el modelo'
        read_db_lf             = ttk.Labelframe(main_container, text = read_db_text, padding=(15,10,10,10))
        read_db_lf.configure(style="info.TLabelframe")
        read_db_lf.grid(row = 0, column = 0, sticky = "nsew")
        self.frames["READ"]    = read_db_lf
        self.read_db_entries   = {}
        self.read_db_file_btn  = None
        self.read_db_csv_label = None
        self.read_db_btn       = None
        self.Create_Read_DB_Fields()

        # Test new entry frame __init__
        test_text = 'Complete los campos para predecir si se va a jugar o no'
        test_lf = ttk.Labelframe(main_container, text = test_text, padding=(15,10,10,10))
        test_lf.configure(style="info.TLabelframe")
        test_lf.grid(row = 0, column = 0, sticky = "nsew")
        self.frames["TEST"] = test_lf
        self.test_entries = {}
        self.test_control_btns = {}
        self.test_img_btn = None
        self.test_play_label = None
        self.Create_Test_Fields()

        # Show register frame
        self.Show_Lf("READ")
        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())
    # end __init__

    def Create_Sidebar_Btns(self):
        register_btn = ttk.Button(
            master=self.sidebar_f,
            text='Registrar producto',
            bootstyle = PRIMARY,
            command=lambda: self.Show_Lf("READ")
        )
        self.sidebar_btns["READ"] = register_btn
        register_btn.pack(fill = X,  pady = (15,0), padx = (5,0)) 

        modify_btn = ttk.Button(
            master=self.sidebar_f,
            text='Modificar producto',
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
            text="Read DB", 
            command=lambda: self.Read_DB()
        )
        read_db_btn.configure(style="success.TButton")
        read_db_btn.grid(row=1, column=1, padx=5)
        self.read_db_btn = read_db_btn

        label = ttk.Label(read_db_frame)
        label.grid(row=0, column=0, sticky="w", padx=5)
        self.read_db_csv_label = label
        btn = ttk.Button(read_db_frame,
            text="Seleccionar CSV",
            command=lambda label = label: self.Read_CSV(label)
        )
        btn.grid(row=1, column=0, padx=5)
        btn.configure(style="info.TButton")
        self.read_db_file_btn = btn
    # end create_register_fields

    def Create_Test_Fields(self):
        test_frame = ttk.Frame(self.frames["TEST"])
        test_frame.pack(fill = X, expand = YES, anchor="nw")

        cancel_btn = ttk.Button(test_frame,
            text="Cancelar",
            command=lambda: self.Cancel_Modify()
        )
        cancel_btn.configure(bootstyle = DANGER)
        cancel_btn.grid(row=3, column=4, padx=5)
        self.test_control_btns["CANCEL"] = cancel_btn        
        
        predict_btn = ttk.Button(test_frame,
            text="Predecir",
            command=lambda: self.Predict()
        )
        predict_btn.configure(bootstyle = SUCCESS)
        predict_btn.grid(row=3, column=3, padx=5)
        self.test_control_btns["CANCEL"] = cancel_btn
        
        label_text = ''

        for index, P in enumerate(self.parameters_keys):
            entry = None
            label_text = func.get_Parameter_Des(P)
            label = ttk.Label(test_frame, text = label_text)
            
            entry = ttk.Entry(test_frame,
                font       = ("DM Sans", 10),
                foreground = "#ababab",
                width      = func.get_Parameter_Width(P)
            )
            entry.insert(0, func.get_Parameter_DV(P))
            entry.bind("<FocusIn>",
                lambda event, entry = entry, default_text = func.get_Parameter_DV(P):
                self.Entry_Focus(event, entry, default_text)
            )
            entry.bind("<FocusOut>",
                lambda event, entry = entry, default_text = func.get_Parameter_DV(P):
                self.Entry_Focus(event, entry, default_text)
            )
            if P == "PLAY":
                label.grid(row=0, column=index, sticky="w", padx=5)
            else:
                minus = 1 if index % 2 == 1 else 0
                label.grid(row=index - minus, column=index % 2, sticky="w", padx=5)
                entry.configure(bootstyle= INFO)
                entry.grid(row= index + 1 - minus , column=index % 2, padx=5)
                self.test_entries[P] = entry

        label = ttk.Label(test_frame, text="Resultado")
        label.grid(row=1, column=index, sticky="w", padx=5)
        self.test_play_label = label

    # end create_modify_fields

    def Show_Lf(self, lf_name):
        frame = self.frames[lf_name]
        frame.tkraise()
        self.sidebar_btns[lf_name].configure(bootstyle = PRIMARY)
        for key in self.sidebar_btns.keys():
            if key != lf_name:
                self.sidebar_btns[key].configure(bootstyle = OUTLINE)
    # end show_lf

    def Entry_Focus(self, event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, END)
            entry.configure(foreground = "#232323")
        elif entry.get() == '':
            entry.insert(0, default_text)
            entry.configure(foreground = "#ababab")
    # end entry_focus

    def Read_CSV(self, label):
        home_dir = os.path.expanduser("~")
        doc_dir = os.path.join(home_dir, "Documents")
        csv_path = filedialog.askopenfilename(
            initialdir = doc_dir,
            title = "Seleccionar archivo CSV",
            filetypes = (("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
        )
        if os.path.isfile(csv_path):
            self.csv_path = csv_path
            label.configure(text = csv_path.split("/")[-1])
        else:
            label.configure(text = '')
    # end get_img

    def Read_DB(self):
        path = self.read_db_csv_label.cget("text")
        is_valid = func.isValid_CSV(path)
        if not is_valid:
            self.Invalid_Data(self.read_db_entries, ['CSV'], "READ")
        else:
            self.read_db_btn.configure(text="Done")
            self.best_k = model.train(self.csv_path)
        return
        
    # end register_product

    def Cancel_Modify(self):
        self.Clear_Entries(self.test_entries, "TEST")
    # end cancel_modify

    def Invalid_Data(self, entries : dict, keys : list, from_f : str):
        for key in keys:
            if key == "CSV" and from_f == "READ":
                self.read_db_file_btn.configure(bootstyle = DANGER)
                continue
            entries[key].configure(bootstyle = DANGER)
        parameters = self.parameters_keys
        if from_f == "READ":
            parameters = 'CSV'
        valid_keys = [value for value in parameters + ["CSV"] if value not in keys]
        self.Valid_Data(entries, valid_keys, from_f)
    # end invalid_data

    def Valid_Data(self, entries : dict, keys : list, from_f : str):
        for key in keys:
            if key == "CSV" and from_f == "READ":
                self.read_db_file_btn.configure(bootstyle = INFO)
                continue
            entries[key].configure(bootstyle = INFO)
    # end valid_data

    def Clear_Entries(self, entries : dict, from_f : str):
        if from_f == "TEST":
            self.test_play_label.configure(text = 'Resultado')

            for key in entries.keys():
                entries[key].delete(0, END)
                entries[key].insert(0, func.get_Parameter_DV(key))
                entries[key].configure(foreground = "#ababab")


        if from_f == "REGISTER":
            for key in entries.keys():
                entries[key].delete(0, END)
                entries[key].insert(0, func.get_Parameter_DV(key))
                entries[key].configure(foreground = "#ababab")
                entries[key].configure(bootstyle = INFO)
            self.read_db_csv_label.configure(text = '')
    # end clear_entries
    
    def Predict(self):
        a, b = func.Verify_Data(self.test_entries)
        p = np.array([self.test_entries[key].get() for key in self.parameters_keys[:-1]])
        outlook = p[0]
        p = [np.int64(x) for x in p[1:]]
        if outlook == 'sunny':
            p = np.concatenate(([1, 0, 0], p))
        elif outlook == 'rainy':
            p = np.concatenate(([0, 1, 0], p))
        elif outlook == 'overcast':
            p = np.concatenate(([0, 0, 1], p))
        
        prediction = model.predict(p, self.best_k, self.csv_path)
        self.test_play_label.configure(text = prediction)
    # end predict