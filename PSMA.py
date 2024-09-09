import os
import tkinter
from tkinter import *
from tkinter import ttk
import xlsxwriter

class dPSMA():
    # ============creating def for Deparment notebook===================================
    def creatPSMA(self):
        self.FDGbutton.destroy()
        self.PSMAbutton.destroy()
        self.chooseRAD.destroy()

        self.FDGbutton.destroy()
        self.PSMAbutton.destroy()
        self.chooseRAD.destroy()

        self.i += 1
        p = "FDG #" + str(self.i)
        t = 0
        if self.pharmnote is None:
            self.pharmnote = ttk.Notebook(self.new_main_Frame, style="AL.TNotebook")
            self.pharmnote.configure(width=1550, height=728)
            self.pharmnote.grid(row=0, sticky="w")
        self.Pharmframe = ttk.Frame(self.pharmnote)
        self.Pharmframe.pack(fill=BOTH, expand=1)
        self.pharmnote.add(self.Pharmframe, text=p)
        # ======Room scrollbar=========
        self.pharmcanv = Canvas(self.Pharmframe)

        self.xscrollroom = ttk.Scrollbar(self.Pharmframe, orient=HORIZONTAL, command=self.pharmcanv.xview)
        self.xscrollroom.pack(side=BOTTOM, fill=X)
        self.pharmcanv.pack(side=LEFT, fill=BOTH, expand=1)
        self.yscrollroom = ttk.Scrollbar(self.Pharmframe, orient=VERTICAL, command=self.pharmcanv.yview)
        self.yscrollroom.pack(side=RIGHT, fill=Y)
        self.pharmcanv.configure(yscrollcommand=self.yscrollroom.set, xscrollcommand=self.xscrollroom.set, bg="#f6f8f8")
        # =========Room tab===========================
        self.d["frame_1 {0}".format(str(t))] = ttk.Frame(self.pharmcanv)
        self.d["frame_1 " + str(t)].bind('<Configure>',
                                         lambda e: self.pharmcanv.configure(scrollregion=self.pharmcanv.bbox("all")))
        self.pharmcanv.create_window((0, 0), window=self.d["frame_1 " + str(t)], anchor="nw")

        # ==========αρχικοποίηση τιμών =================
        self.ep = 1
        self.d["x {0}".format(str(t))] = 0

        # ==============Number of Barriers in the Room==========
        self.lanumwall = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel", text="Number of Patients:")
        self.lanumwall.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.d["vnumdose {0}".format(str(t))] = IntVar(value=6)
        self.d["numdose {0}".format(str(t))] = ttk.Spinbox(master=self.d["frame_1 " + str(t)],
                                                           textvariable=self.d["vnumdose " + str(t)], from_=1, to=50,
                                                           width=5, command=lambda: self.patients(t))
        self.d["numdose " + str(t)].grid(row=0, column=1, pady=10, padx=10, sticky="w")
        # ======================Labels=================
        self.NameLabel = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel", text="Patient's Names")
        self.NameLabel.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.weightLabel = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel", text="Patient's weight (kg)")
        self.weightLabel.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.timeLabel = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel", text="Measurement time (HH:MM)")
        self.timeLabel.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        self.reqactivLabel = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel",
                                       text="Required activity (mCi)")
        self.reqactivLabel.grid(row=1, column=4, padx=10, pady=10, sticky="w")
        self.reqvolLabel = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel", text="Required volume (ml)")
        self.reqvolLabel.grid(row=1, column=5, padx=10, pady=10, sticky="w")
        self.mesactivLabel = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel",
                                       text="Measured activity (mCi)")
        self.mesactivLabel.grid(row=1, column=6, padx=10, pady=10, sticky="w")
        self.remactivLabel = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel",
                                       text="Remaining activity (mCi)")
        self.remactivLabel.grid(row=1, column=7, padx=10, pady=10, sticky="w")
        self.errorLabel = ttk.Label(master=self.d["frame_1 " + str(t)], style="AL.TLabel", text="Error (%)")
        self.errorLabel.grid(row=1, column=8, padx=10, pady=10, sticky="w")

    def patients(self, t):
        if self.d["x " + str(t)] < self.d["vnumdose " + str(t)].get():
            while self.d["x " + str(t)] < self.d["vnumdose " + str(t)].get():
                a = 1