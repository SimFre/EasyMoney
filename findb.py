
import tkinter as tk
#import tktable

class FinDB(tk.Frame):
   def __init__(self, master=None):
      tk.Frame.__init__(self, master)
      self.grid(sticky=tk.N+tk.S+tk.W+tk.E)
      self.createWidgets()

   def createWidgets(self):
      self.quitButton = tk.Button(self, text="Quit", command=self.quit)
      self.quitButton.grid()

      table = tktable.Table(parent, rows=5, cols=5)
      table.pack()

application = FinDB()
application.master.title("Finance Database")
