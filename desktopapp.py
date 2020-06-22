import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os, sys
import IPTU, pandas as pd

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.getIPTU = tk.Button(self)
        self.getIPTU["text"] = "Carregar dados"
        self.getIPTU["command"] = self.preencher_lista
        self.getIPTU.pack(side="top")
        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.listaIC = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listaIC.pack()
        self.extrair_btn = tk.Button(self, text="Extrair IPTU", fg="red",
                              command=self.extrairIC, state=tk.DISABLED)
        self.extrair_btn.pack(side="bottom")


    def preencher_lista(self):
        self.listaIC.delete(0,'end')
        self.filename =  filedialog.askopenfilename()
        path_data = self.filename #caminho para meu arquivo csv com os ID's
        self.data = pd.read_csv(path_data, delimiter = ';') # abre o arquivo
        print(self.data)
        for row in range(len(self.data['Indice Cadastral'])):
            self.listaIC.insert('end', str(self.data['Indice Cadastral'][row]))
        self.extrair_btn["state"] = tk.NORMAL

    def extrairIC(self):
        self.extrair_btn["state"] = tk.NORMAL
        IPTU.execute(self.data)
        messagebox.showinfo("Status", "Fim")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
