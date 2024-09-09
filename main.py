import xlsxwriter
import json
import os
from datetime import datetime
from ttkthemes import ThemedTk
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter import font
from FDG import dFDG

from PSMA import dPSMA

root = ThemedTk(theme="arc")
font.families()

class App(dFDG, dPSMA):

    def __init__(self, master):
        # ============Menu Bar==================
        main_menubar = Menu(root)
        root.configure(menu=main_menubar)
        #==========αρχικοποίηση παραθύρων=======
        self.pharmnote = None
        self.Pharmframe = None
        # ===========File=============
        self.file_menu = Menu(main_menubar, tearoff=0)
        self.newoptions = Menu(main_menubar, tearoff=0)
        main_menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_cascade(label="New...", menu=self.newoptions)
        self.file_menu.add_command(label="Open", command = self.load_data)
        self.file_menu.add_command(label="Save to Excel", command=self.save_to_excel)
        self.newoptions.add_command(label="FDG", command=self.creatFDG)
        self.newoptions.add_command(label="PSMA", command=self.creatPSMA)

        """self.file_menu.add_command(label="Open", )
        self.file_menu.add_command(label="Save as...", )"""
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        # ==========Edit=====================
        self.edit_menu = Menu(main_menubar, tearoff=0)
        """"main_menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Redo",)  # command = my_text.edit_redo)
        self.edit_menu.add_command(label="Undo", )  # command = my_text.edit_undo)
        self.edit_menu.add_command(label="Cut", )  # command = my_text.edit_redo)
        self.edit_menu.add_command(label="Copy", )  # command = my_text.edit_undo)
        self.edit_menu.add_command(label="Paste", )  # command = my_text.edit_redo)
        """
#========Settings===============
        self.setting_menu = Menu(main_menubar, tearoff=0)
        main_menubar.add_cascade(label="Settings", menu=self.setting_menu)
        self.setting_menu.add_command(label = "FDG Properties")
#==========help=====================
        self.help_menu = Menu(main_menubar, tearoff= 0)
        main_menubar.add_cascade(label="Help", menu=self.help_menu)
        self.i = 0
        self.d = {}
        self.p = {"patient_data": {}}
        self.r = {}
        '''self.thm = {}
        self.xlmat = {}
        self.barn = {}
        self.barr = {}
        self.wa = {}
        self.col = {}'''
        #=====Main window scrollbar=========
        self.master = master
        self.main_frame = ttk.Frame(self.master, style="ML.TFrame")
        self.main_frame.pack(fill=BOTH, expand=1)

        # ===========Buttons========
        self.chooseRAD = ttk.Label(master=self.main_frame,text="Select Radio-pharmacy", style="CL.TLabel" )
        self.FDGbutton = ttk.Button(master=self.main_frame, style="AL.TButton", text="FDG", command=self.creatFDG)
        self.PSMAbutton = ttk.Button(master=self.main_frame,style="AL.TButton", text="PSMA", command=self.creatPSMA)

        self.chooseRAD.pack(anchor="c", pady=10, padx=10)
        self.FDGbutton.pack(anchor="c", pady=10, padx=10)
        self.PSMAbutton.pack(anchor="c", pady=10, padx=10)

        # ====================Styles=============================================
        self.style = ttk.Style()
        self.style.configure("TButton", background="#f7faf9", foreground='#171a24', font="calibri 12")
        self.style.configure("AL.TButton", background="#2c3b47", foreground='#171a24', font="calibri 13")
        self.style.configure("TFrame", background="#f7faf9", foreground="#f7faf9")
        self.style.configure("ML.TFrame", background="#2c3b47", foreground="#171719")
        self.style.configure("AL.TNotebook", background="#2c3b47", foreground="#f7faf9")
        self.style.configure("BL.TNotebook", background="#f7faf9", foreground="#f7faf9")
        self.style.configure("BL.TLabel", background="#f7faf9", foreground='#171719', font='Helvetica 14',
                             weight='bold')
        self.style.configure("CL.TLabel", background="#2c3b47", foreground='#f6f8f8', font='Helvetica 14',
                             weight='bold')
        self.style.configure("AL.TLabel", background="#f7faf9", foreground='#171719', font='Helvetica 12')

        self.style.configure("TLabel", background="#f7faf9", foreground='#171719', font='Helvetica 12')
        self.style.configure("TRadiobutton", background="#f7faf9", foreground='#171719', font='Helvetica 11')
        self.style.configure("TCheckbutton", background="#f7faf9", foreground='#171719', font='Helvetica 11')
        self.style.configure("TSpinbox", background="#f7faf9", foreground='#000000', font='Helvetica 11')
        self.style.configure("TCombobox", background="#f7faf9", foreground='#000000', font='Helvetica 11')
        self.style.configure("TMenubutton", background="#ffffff", foreground='#000000', font='Helvetica 9')
        self.style.configure("TScrollbar", background="#f7faf9", foreground="#f7faf9")

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.save_data()
        root.destroy()

    def save_data(self):
        today = datetime.now()
        file_path = f"PET_{today.strftime('%d_%m_%Y')}.json"
        data = {"patients": [], "pharmacy": []}

        for t in range(1, self.i + 1):
            # Save patient data
            for i in range(1, self.d[f"vnumdose {t}"].get() + 1):
                patient_data = {"t": t, "i": i, "name": self.p[f"nampat {t}{i}_var"].get(),
                    "weight": self.p[f"weightpat {t}{i}_var"].get(),
                    "measurement_time": self.p[f"meas_timepat {t}{i}_var"].get(),
                    "required_activity": self.p[f'required_activity_var {t}{i}'],
                    "required_volume": self.p[f"reqvol {t}{i}_var"].get(),
                    "measured_activity": self.p[f"meas_activ {t}{i}_var"].get(),
                    "measured_time": self.p[f"meas_timeact {t}{i}_var"].get(),
                    "remaining_activity": self.p[f"meas_remain {t}{i}_var"].get(),
                    "measured_time_remaining": self.p[f"meas_timeremain {t}{i}_var"].get(),
                    "error": self.p[f"error {t}{i}_var"].get()}
                data["patients"].append(patient_data)

            # Save pharmacy data
            pharmacy_data = {"t": t, "initial_activ": self.r[f"initial_activ {t}"].get(),
                "initial_time": self.r[f"initial_time {t}"].get(),
                "vial_volume": self.r[f"vial_volume {t}"].get(), "rad_volume": self.r[f"rad_volume {t}"].get()}
            data["pharmacy"].append(pharmacy_data)

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        messagebox.showinfo("Save Data", f"Data saved to {file_path}")

    def load_data(self):
        root = Tk()
        root.withdraw()  # Hide the root window

        file_path = filedialog.askopenfilename(title="Open Data File",
                                               filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])

        if not file_path:
            return

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Load patient data
        for patient_data in data["patients"]:
            t = patient_data["t"]
            i = patient_data["i"]

            self.p[f"nampat {t}{i}_var"].set(patient_data["name"])
            self.p[f"weightpat {t}{i}_var"].set(patient_data["weight"])
            self.p[f"meas_timepat {t}{i}_var"].set(patient_data["measurement_time"])
            self.p[f'required_activity_var {t}{i}'].set(patient_data["required_activity"])
            self.p[f"reqvol {t}{i}_var"].set(patient_data["required_volume"])
            self.p[f"meas_activ {t}{i}_var"].set(patient_data["measured_activity"])
            self.p[f"meas_timeact {t}{i}_var"].set(patient_data["measured_time"])
            self.p[f"meas_remain {t}{i}_var"].set(patient_data["remaining_activity"])
            self.p[f"meas_timeremain {t}{i}_var"].set(patient_data["measured_time_remaining"])
            self.p[f"error {t}{i}_var"].set(patient_data["error"])

        # Load pharmacy data
        for pharmacy_data in data["pharmacy"]:
            t = pharmacy_data["t"]
            self.r[f"initial_activ {t}"].set(pharmacy_data["initial_activ"])
            self.r[f"initial_time {t}"].set(pharmacy_data["initial_time"])
            self.r[f"vial_volume {t}"].set(pharmacy_data["vial_volume"])
            self.r[f"rad_volume {t}"].set(pharmacy_data["rad_volume"])

        messagebox.showinfo("Load Data", "Data loaded successfully")

    def save_to_excel(self):
        today = datetime.now()
        file_path = f"PET_{today.strftime('%d_%m_%Y')}.xlsx"

        try:
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()

            headers = ["Patient Name", "Weight (kg)", "Measurement Time (HH:MM)", "Required Activity (mCi)",
                       "Required Volume (ml)", "Measured Activity (mCi)", "Measured Time (HH:MM)",
                       "Remaining Activity (mCi)", "Measured Time Remaining (HH:MM)", "Error (%)"]
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)
            row = 1
            for t in range(1, self.i + 1):
                dose_count = self.d.get(f"vnumdose {t}")
                if dose_count is None:
                    continue
                for i in range(1, dose_count.get() + 1):
                    data = [self.p.get(f"nampat {t}{i}", StringVar()).get(),
                        self.p.get(f"weightpat {t}{i}", StringVar()).get(),
                        self.p.get(f"meas_timepat {t}{i}", StringVar()).get(),
                        self.p.get(f"reqactiv {t}{i}", StringVar()).get(),
                        self.p.get(f"reqvol {t}{i}", StringVar()).get(),
                        self.p.get(f"meas_activ {t}{i}", StringVar()).get(),
                        self.p.get(f"meas_timeact {t}{i}", StringVar()).get(),
                        self.p.get(f"meas_remain {t}{i}", StringVar()).get(),
                        self.p.get(f"meas_timeremain {t}{i}", StringVar()).get(),
                        self.p.get(f"error {t}{i}", StringVar()).get()]

                    for col, value in enumerate(data):
                        worksheet.write(row, col, value)

                    row += 1
            workbook.close()
            messagebox.showinfo("Save to Excel", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Save to Excel", f"Failed to save data: {e}")

    def opencpr(self):
        self.path= "5_NCRP_147_2004.pdf"
        os.system(self.path)

# =============
app = App(root)
root.mainloop()

