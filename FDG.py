import os
from tkinter import *
from tkinter import ttk, messagebox
import xlsxwriter
from math import exp, log
from datetime import datetime, timedelta

class dFDG:
    def creatFDG(self):
        self.FDGbutton.destroy()
        self.PSMAbutton.destroy()
        self.chooseRAD.destroy()


        self.i += 1
        p = "FDG #" + str(self.i)
        t = self.i

        if self.pharmnote is None:
            self.pharmnote = ttk.Notebook(self.main_frame, style="AL.TNotebook")
            self.pharmnote.configure(width=1525, height=730)
            self.pharmnote.grid(row=0, sticky="w")
        self.Pharmframe = ttk.Frame(self.pharmnote)
        self.Pharmframe.pack(fill=BOTH, expand=1)
        self.pharmnote.add(self.Pharmframe, text=p)
        #======Room scrollbar=========
        self.pharmcanv= Canvas(self.Pharmframe)
        self.xscrollroom = ttk.Scrollbar(self.Pharmframe, orient=HORIZONTAL, command=self.pharmcanv.xview)
        self.xscrollroom.pack(side=BOTTOM, fill=X)
        self.pharmcanv.pack(side=LEFT, fill=BOTH, expand=1)
        self.yscrollroom = ttk.Scrollbar(self.Pharmframe, orient=VERTICAL, command=self.pharmcanv.yview)
        self.yscrollroom.pack(side=RIGHT, fill=Y)
        self.pharmcanv.configure(yscrollcommand=self.yscrollroom.set,xscrollcommand=self.xscrollroom.set, bg="#f6f8f8")
        # =========Room tab===========================
        self.d["frame_1 {0}".format(str(t))] = ttk.Frame(self.pharmcanv)
        self.d["frame_1 " + str(t)].bind('<Configure>', lambda e: self.pharmcanv.configure(scrollregion=self.pharmcanv.bbox("all")))
        self.pharmcanv.create_window((0,0), window=self.d["frame_1 " + str(t)], anchor="nw")

        # ==========αρχικοποίηση τιμών =================
        self.d["x {0}".format(str(t))] = 0
        self.d["patient {0}".format(t)] = 0


        # StringVars for Entry widgets
        self.r[f"initial_activ {t}"] = StringVar()
        self.r[f"initial_time {t}"] = StringVar()
        self.r[f"vial_volume {t}"] = StringVar()
        self.r[f"rad_volume {t}"] = StringVar()

        # Labels for inputs and calculated outputs
        self.lanumpat = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel", text="Number of Patients:")
        self.lanumpat.grid(row=0, column=1, pady=20, padx=5, sticky="w")

        self.d[f"vnumdose {t}"] = IntVar(value=6)
        self.d[f"numdose {t}"] = ttk.Spinbox(master=self.d[f"frame_1 {t}"], textvariable=self.d[f"vnumdose {t}"],
                                             from_=1, to=50, width=5, command=lambda: self.patients(t))
        self.d[f"numdose {t}"].grid(row=0, column=2, pady=10, padx=10, sticky="w")

        self.Inactl = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel", text="Initial activity (mCi):")
        self.Inactl.grid(row=0, column=3, pady=20, padx=5, sticky="e")
        self.r[f"initial_activ_entry {t}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                       textvariable=self.r[f"initial_activ {t}"], width=10)
        self.r[f"initial_activ_entry {t}"].grid(row=0, column=4, padx=5, pady=5, sticky="w")

        self.lanumpat = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel", text="Initial time (HH:MM):")
        self.lanumpat.grid(row=1, column=3, pady=20, padx=5, sticky="e")
        self.r[f"initial_time_entry {t}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                      textvariable=self.r[f"initial_time {t}"], width=10)
        self.r[f"initial_time_entry {t}"].grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.r[f"initial_time_entry {t}"].bind('<KeyRelease>', self.format_time)

        self.vial_volume_label = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel",
                                           text="Total Vial Volume (ml):")
        self.vial_volume_label.grid(row=0, column=5, pady=20, padx=5, sticky="e")
        self.r[f"vial_volume_entry {t}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                     textvariable=self.r[f"vial_volume {t}"], width=10)
        self.r[f"vial_volume_entry {t}"].grid(row=0, column=6, padx=5, pady=5, sticky="w")

        self.rad_volume_label = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel",
                                          text="Initial Radiopharmacy\nVolume (ml):")
        self.rad_volume_label.grid(row=1, column=5, pady=20, padx=5, sticky="e")
        self.r[f"rad_volume_entry {t}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                    textvariable=self.r[f"rad_volume {t}"], width=10)
        self.r[f"rad_volume_entry {t}"].grid(row=1, column=6, padx=5, pady=5, sticky="w")

        self.req_vial_volume_label = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel",
                                               text="Required Saline\nVolume (ml):")
        self.req_vial_volume_label.grid(row=1, column=7, pady=20, padx=5, sticky="w")
        self.req_vial_volume = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel", text="0.0")
        self.req_vial_volume.grid(row=1, column=8, padx=5, pady=5, sticky="w")

        self.used_vial_volume_label = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel",
                                                text="Remaining Radiopharmacy\nVolume (ml):")
        self.used_vial_volume_label.grid(row=0, column=7, pady=20, padx=5, sticky="w")

        self.remaining_activity_label = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel",
                                                  text="Remaining Activity\nin the Vial (mCi):")
        self.remaining_activity_label.grid(row=1, column=1, pady=20, padx=5, sticky="w")

        # Labels for headers
        headers = ["Patient Name", "Weight (kg)", "Measurement\nTime (HH:MM)", "Required\nActivity (mCi)",
                   "Required\nVolume (ml)", "Measured\nActivity (mCi)", "Measured Activity\nTime (HH:MM)",
                   "Remaining\nActivity (mCi)", "Measured Time\nRemaining (HH:MM)", "Error (%)\n-10<Limit<10",
                   "Injection\nTime (HH:MM)", "Time Left"]

        for col, header in enumerate(headers):
            ttk.Label(self.d[f"frame_1 {t}"], text=header, style="AL.TLabel").grid(row=2, column=col + 1, padx=5,
                                                                                   pady=5, sticky="w")

        # Bindings for Entry widgets
        self.r[f"vial_volume_entry {t}"].bind("<FocusOut>", lambda event: self.calculate_saline(t))
        self.r[f"rad_volume_entry {t}"].bind("<FocusOut>", lambda event: self.calculate_saline(t))

        # Button to save data
       # ttk.Button(self.d["frame_1 " + str(self.i)], text="Save Data", command=self.save_Data).grid(row=0, column=0, padx=2, pady=2)
        self.patients(t)
        return p
    def calculate_saline(self, t):
        try:
            total_vial_volume = float(self.r["vial_volume " + str(t)].get())
            rad_volume = float(self.r["rad_volume " + str(t)].get())
            saline_volume = total_vial_volume - rad_volume
            self.req_vial_volume.config(text=f"{saline_volume:.2f}")
        except Exception as e:
            print(f"Error in calculating saline volume: {e}")

    def patients(self, t):
        if self.d["x " + str(t)] < self.d["vnumdose " + str(t)].get():
            while self.d["x " + str(t)] < self.d["vnumdose " + str(t)].get():
                self.d["x " + str(t)] += 1
                e = self.d["x " + str(t)]
                a = self.i
                self.p[f"nampat {a}{e}_var"] = StringVar()
                self.p[f"weightpat {a}{e}_var"] = StringVar()
                self.p[f"meas_timepat {a}{e}_var"] = StringVar()
                self.p[f"required_activity_var {a}{e}"] = StringVar()
                self.p[f"reqvol {a}{e}_var"] = StringVar()
                self.p[f"meas_activ {a}{e}_var"] = StringVar()
                self.p[f"meas_timeact {a}{e}_var"] = StringVar()
                self.p[f"meas_remain {a}{e}_var"] = StringVar()
                self.p[f"meas_timeremain {a}{e}_var"] = StringVar()
                self.p[f"error {a}{e}_var"] = StringVar()
                self.p[f"admintime {a}{e}_var"] = StringVar()
                self.p[f"exam_end_time {a}{e}_var"] = StringVar()

                self.d[f"nump {a}{e}"] = ttk.Label(master=self.d[f"frame_1 {t}"], style="AL.TLabel", text=f"#{e}")
                self.d[f"nump {a}{e}"].grid(row=2 + e, column=0, padx=2, pady=2, sticky="w")

                # Entry for patient name
                self.p[f"nampat {a}{e}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                     textvariable=self.p[f"nampat {a}{e}_var"], width=20)
                self.p[f"nampat {a}{e}"].grid(row=2 + e, column=1, padx=5, pady=5)
                self.p[f"nampat {a}{e}"].bind("<FocusOut>",
                                              lambda event, t=t, i=a, e=e: self.calculate_activity(t, i, e))

                # Entry for patient weight
                self.p[f"weightpat {a}{e}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                        textvariable=self.p[f"weightpat {a}{e}_var"], width=5)
                self.p[f"weightpat {a}{e}"].grid(row=2 + e, column=2, padx=5, pady=5)
                self.p[f"weightpat {a}{e}"].bind("<FocusOut>",
                                                 lambda event, t=t, i=a, e=e: self.calculate_activity(t, i, e))

                # Entry for measurement time of patient
                self.p[f"meas_timepat {a}{e}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                           textvariable=self.p[f"meas_timepat {a}{e}_var"], width=9)
                self.p[f"meas_timepat {a}{e}"].grid(row=2 + e, column=3, padx=5, pady=5)
                self.p[f"meas_timepat {a}{e}"].bind('<KeyRelease>', self.format_time)
                self.p[f"meas_timepat {a}{e}"].bind("<FocusOut>",
                                                    lambda event, t=t, i=a, e=e: self.calculate_activity(t, i, e))

                # Label for required activity (you didn't specify an Entry here, assuming it's a Label)
                self.p[f"reqactiv {a}{e}"] = ttk.Label(master=self.d[f"frame_1 {t}"], style="C.TLabel", text=" ")
                self.p[f"reqactiv {a}{e}"].grid(row=2 + e, column=4, padx=2, pady=2)

                # Label for required volume (you didn't specify an Entry here, assuming it's a Label)
                self.p[f"reqvol {a}{e}"] = ttk.Label(master=self.d[f"frame_1 {t}"], style="C.TLabel", text=" ")
                self.p[f"reqvol {a}{e}"].grid(row=2 + e, column=5, padx=2, pady=2)

                # Entry for measured activity of patient
                self.p[f"meas_activ {a}{e}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                         textvariable=self.p[f"meas_activ {a}{e}_var"], width=10)
                self.p[f"meas_activ {a}{e}"].grid(row=2 + e, column=6, padx=5, pady=5)
                self.p[f"meas_activ {a}{e}"].bind("<FocusOut>",
                                                  lambda event, t=t, i=a, e=e: self.calculate_activity(t, i, e))

                # Entry for measured time of activity
                self.p[f"meas_timeact {a}{e}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                           textvariable=self.p[f"meas_timeact {a}{e}_var"], width=9)
                self.p[f"meas_timeact {a}{e}"].grid(row=2 + e, column=7, padx=5, pady=5)
                self.p[f"meas_timeact {a}{e}"].bind("<FocusOut>",
                                                    lambda event, t=t, i=a, e=e: self.calculate_activity(t, i, e))
                self.p[f"meas_timeact {a}{e}"].bind('<KeyRelease>', self.format_time)

                # Entry for measured remaining activity
                self.p[f"meas_remain {a}{e}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                          textvariable=self.p[f"meas_remain {a}{e}_var"], width=10)
                self.p[f"meas_remain {a}{e}"].grid(row=2 + e, column=8, padx=5, pady=5)
                self.p[f"meas_remain {a}{e}"].bind("<FocusOut>",
                                                   lambda event, t=t, i=a, e=e: self.calculate_activity(t, i, e))

                # Entry for measured time remaining
                self.p[f"meas_timeremain {a}{e}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                              textvariable=self.p[f"meas_timeremain {a}{e}_var"],
                                                              width=9)
                self.p[f"meas_timeremain {a}{e}"].grid(row=2 + e, column=9, padx=5, pady=5)
                self.p[f"meas_timeremain {a}{e}"].bind('<KeyRelease>', self.format_time)
                self.p[f"meas_timeremain {a}{e}"].bind("<FocusOut>",
                                                       lambda event, t=t, i=a, e=e: self.calculate_activity(t, i, e))

                self.p[f"admintime {a}{e}"] = ttk.Entry(master=self.d[f"frame_1 {t}"],
                                                        textvariable=self.p[f"admintime {a}{e}_var"], width=9)
                self.p[f"admintime {a}{e}"].grid(row=2 + e, column=11, padx=5, pady=5)
                self.p[f"admintime {a}{e}"].bind('<KeyRelease>', self.format_time)
                self.p[f"admintime {a}{e}"].bind("<FocusOut>",
                                                 lambda event, t=t, i=a, e=e: self.calculate_remaining_time(t, a, e))

                # Label for exam end time
                self.p[f"exam_end_time {a}{e}"] = ttk.Label(master=self.d[f"frame_1 {t}"],
                                                            textvariable=self.p[f"exam_end_time {a}{e}_var"])
                self.p[f"exam_end_time {a}{e}"].grid(row=2 + e, column=12, padx=5, pady=5)


        else:

            while self.d["x " + str(t)] > self.d["vnumdose " + str(t)].get():
                g = self.d["x " + str(t)]
                a = self.i
                self.d["x " + str(t)] -= 1
                # Destroying widgets
                if f"nump {a}{g}" in self.d:
                    self.d[f"nump {a}{g}"].destroy()
                    del self.d[f"nump {a}{g}"]

                if f"nampat {a}{g}" in self.p:
                    self.p[f"nampat {a}{g}"].destroy()
                    del self.p[f"nampat {a}{g}"]

                if f"weightpat {a}{g}" in self.p:
                    self.p[f"weightpat {a}{g}"].destroy()
                    del self.p[f"weightpat {a}{g}"]

                if f"meas_timepat {a}{g}" in self.p:
                    self.p[f"meas_timepat {a}{g}"].destroy()
                    del self.p[f"meas_timepat {a}{g}"]

                if f"reqactiv {a}{g}" in self.p:
                    # Destroy Labels
                    self.p[f"reqactiv {a}{g}"].destroy()
                    del self.p[f"reqactiv {a}{g}"]

                    if f"reqvol {a}{g}" in self.p:
                        self.p[f"reqvol {a}{g}"].destroy()
                        del self.p[f"reqvol {a}{g}"]
                    if f"error {a}{g}" in self.p:
                        self.p[f"error {a}{g}"].destroy()
                        del self.p[f"error {a}{g}"]
                    # Update used and remaining volumes
                    if f"meas_activ {a}{g}" in self.p and self.p[f"meas_activ {a}{g}"].get() != "":
                        activ = float(self.p[f"meas_activ {a}{g}"].get())
                        vvol = float(self.p[f"used_rad_volume {a}"].cget("text"))
                        new_vol = vvol + activ
                        self.p[f"used_rad_volume {a}"].config(text=f"{new_vol:.2f}")
                        vial_remaining = float(self.p[f"remain_activ {a}"].cget("text"))
                        new_remain = vial_remaining + activ
                        self.p[f"remain_activ {a}"].config(text=f"{new_remain:.2f}")

                if f"meas_activ {a}{g}" in self.p:
                    self.p[f"meas_activ {a}{g}"].destroy()
                    del self.p[f"meas_activ {a}{g}"]
                if f"meas_timeact {a}{g}" in self.p:
                    self.p[f"meas_timeact {a}{g}"].destroy()
                    del self.p[f"meas_timeact {a}{g}"]
                if f"meas_remain {a}{g}" in self.p:
                    self.p[f"meas_remain {a}{g}"].destroy()
                    del self.p[f"meas_remain {a}{g}"]
                if f"meas_timeremain {a}{g}" in self.p:
                    self.p[f"meas_timeremain {a}{g}"].destroy()
                    del self.p[f"meas_timeremain {a}{g}"]
                if f"admintime {a}{g}" in self.p:
                    self.p[f"admintime {a}{g}"].destroy()
                    del self.p[f"admintime {a}{g}"]

    def format_time(self, event):
        widget = event.widget
        value = widget.get().replace(':', '')  # Remove existing colons

        # Allow the user to type, but don't format until a valid time length is reached
        if len(value) == 4 and value.isdigit():
            if int(value[:2]) < 24 and int(value[2:]) < 60:
                formatted_time = f"{int(value[:2]):02}:{int(value[2:]):02}"
                widget.delete(0, END)
                widget.insert(0, formatted_time)

    def calculate_activity(self, t, i, e):
        try:
            if self.p["weightpat " + str(i) + str(e)].get() != '':
                weight = float(self.p["weightpat " + str(i) + str(e)].get())
            else:
                weight = 0

            if self.r["initial_activ " + str(i)].get() != "":
                initial_activity = float(self.r["initial_activ " + str(i)].get())
            else:
                initial_activity = 0

            if self.r["initial_time " + str(i)].get() != "":
                initial_time_str = self.r["initial_time " + str(i)].get()
            else:
                initial_time_str = "00:00"

            if self.p["meas_timepat " + str(i) + str(e)].get() != "":
                meas_time_str = self.p["meas_timepat " + str(i) + str(e)].get()
            elif self.p["meas_timepat " + str(i) + str(e)].get() == "" and self.p["meas_timepat " + str(i) + str(e-1)].get() != "":
                meas_time_str = self.p["meas_timepat " + str(i) + str(e-1)].get()
            elif initial_time_str is not None:
                meas_time_str = initial_time_str
            else:
                meas_time_str = "00:00"

            initial_time = self.validate_time_format(initial_time_str)
            meas_time = self.validate_time_format(meas_time_str)

            delta_t = (meas_time - initial_time).total_seconds() / 3600  # in hours
            decay_factor = exp(-log(2) * delta_t / 1.83)  # FDG half-life is 1.83 hours


            self.p[f"required_activity_var {i}{e}"] = weight * 0.1  # Assuming 0.1 mCi/kg is the standard dose

            self.p["remain_activ_var " + str(i)] = initial_activity * decay_factor

            if self.p["meas_activ " + str(i) + str(e)].get() != '' and self.p[f"meas_remain {i}{e}"].get() != "":
                error_percentage = (self.p[f"required_activity_var {i}{e}"] - (float(
                    self.p["meas_activ " + str(i) + str(e)].get()))-float(self.p[f"meas_remain {i}{e}"].get())) / self.p[f"required_activity_var {i}{e}"] * 100
            elif self.p["meas_activ " + str(i) + str(e)].get() != '' and self.p[f"meas_remain {i}{e}"].get() == "":
                error_percentage = (self.p[f"required_activity_var {i}{e}"] - (float(self.p["meas_activ " + str(i) + str(e)].get())))/ self.p[f"required_activity_var {i}{e}"] * 100
            else:
                error_percentage = 0

            # Calculate required volume based on entered vial volume
            if i == 1:
                if self.r["vial_volume " + str(i)].get() != "":
                    vial_volume = float(self.r["vial_volume " + str(i)].get())
                else:
                    vial_volume = 0
            else:
                vial_volume = float(self.p["used_rad_volume " + str(i)].cget("text"))

            if self.p["remain_activ_var " + str(i)] and vial_volume != 0:
                required_volume = self.p[f"required_activity_var {i}{e}"] / self.p["remain_activ_var " + str(i)] * vial_volume
            else:
                required_volume = 0

            # Display remaining activity
            if "remain_activ " + str(i) not in self.p :
                self.p["remain_activ " + str(i)] = ttk.Label(master=self.d["frame_1 " + str(i)],
                                                             text=f"{self.p['remain_activ_var ' + str(i)]:.2f}")
                self.p["remain_activ " + str(i)].grid(row=1, column=2, padx=5, pady=5)
            else:
                self.p["remain_activ " + str(i)].config(text=f"{self.p['remain_activ_var ' + str(i)]:.2f}")
            if "reqactiv " + str(i) + str(e) not in self.p:
                self.p["reqactiv " + str(i) + str(e)] = ttk.Label(master=self.d["frame_1 " + str(i)],
                                                                  text=f"{self.p[f'required_activity_var {i}{e}']:.2f}")
                self.p["reqactiv " + str(i) + str(e)].grid(row=2 + e, column=4, padx=5, pady=5)
            else:
                self.p["reqactiv " + str(i) + str(e)].config(text =f"{self.p[f'required_activity_var {i}{e}']:.2f}")
            if "reqvol " + str(i) + str(e) not in self.p:
                self.p["reqvol " + str(i) + str(e)] = ttk.Label(master=self.d["frame_1 " + str(i)],
                                                                text=f"{required_volume:.2f}")
                self.p["reqvol " + str(i) + str(e)].grid(row=2 + e, column=5, padx=5, pady=5)
            else:
                self.p["reqvol " + str(i) + str(e)].config(text=f"{required_volume:.2f}")
            if "error " + str(i) + str(e) not in self.p:
                self.p["error " + str(i) + str(e)] = ttk.Label(master=self.d["frame_1 " + str(i)],
                                                               text=f"{error_percentage:.2f}")
                self.p["error " + str(i) + str(e)].grid(row=2 + e, column=10, padx=5, pady=5)
            else:
                self.p["error " + str(i) + str(e)].config(text =f"{error_percentage:.2f}")

            # Calculate and display how much radiopharmacy has been used
            used_volume = vial_volume - required_volume
            if "used_rad_volume " + str(i) not in self.p:
                self.p["used_rad_volume " + str(i)] = ttk.Label(master=self.d["frame_1 " + str(i)],
                                                                text=f"{used_volume:.2f}")
                self.p["used_rad_volume " + str(i)].grid(row=0, column=8, padx=5, pady=5, sticky="w")
            else:
                self.p["used_rad_volume " + str(i)].config(text=f"{used_volume:.2f}")

            # Update remaining activity of the vial after measuring the activity of current patient
            if self.p[f"meas_activ {i}{e}"].get() != "":
                self.p['remain_activ_var ' + str(i)] -= float(self.p[f"meas_activ {i}{e}"].get())
                self.p["remain_activ " + str(i)].config(text=f"{self.p['remain_activ_var ' + str(i)]:.2f}")

                # Ensure remaining activity doesn't go negative
                if self.p['remain_activ_var ' + str(i)] < 0:
                    self.p['remain_activ_var ' + str(i)] = 0

        except Exception as ex:
            # Handle any exceptions gracefully
            print(f"Error in calculate_activity: {str(ex)}")

    def calculate_remaining_time(self, t, i, e):
        try:
            # Get the administration time from Entry widget's StringVar
            admin_time_str = self.p[f"admintime {i}{e}_var"].get()
            if not admin_time_str:
                self.p[f"exam_end_time {i}{e}_var"].set("Invalid admin time")
                return

            # Convert administration time to datetime
            admin_time = datetime.strptime(admin_time_str, "%H:%M")

            # Calculate the end time (assuming the exam takes 1 hour from the administration time)
            exam_duration = timedelta(hours=1)
            end_time = admin_time + exam_duration

            # Get the current time
            current_time = datetime.now()

            # Calculate the remaining time
            remaining_time_delta = end_time - current_time

            if remaining_time_delta.total_seconds() < 0:
                self.p[f"exam_end_time {i}{e}_var"].set("Exam finished")
            else:
                hours, remainder = divmod(remaining_time_delta.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.p[f"exam_end_time {i}{e}_var"].set(f"{hours:02}:{minutes:02}")
        except Exception as ex:
            self.p[f"exam_end_time {i}{e}_var"].set(f"Error: {str(ex)}")

    def validate_time_format(self, time_str):
        try:
            return datetime.strptime(time_str, "%H:%M")
        except ValueError:
            return None
