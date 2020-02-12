from tkinter import *
from tkintertable import TableCanvas, TableModel

root = Tk()
root.geometry("1000x700")
c = Label(root, text="Test")
c.grid(row=0, column=3)
tframe = Frame(root)
tframe.grid(row=1, column=0)
table = TableCanvas(tframe, width=700)
table.cols=8
table.thefont = ('Arial',8)
filename = 'manual_data.csv'
table.importCSV(filename)
#table.show()

root.mainloop()
