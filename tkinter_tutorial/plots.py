from tkinter import *
import numpy as np
import matplotlib.pyplot as plt


root = Tk()
root.geometry("400x200")

def graph():
    # normal distribution, avg, standard dev, and number of points
    house_prices = np.random.normal(200000, 25000, 5000)
    # to plot histogram, can specify how many bins/bars
    plt.hist(house_prices, 200)
    plt.show()

my_button = Button(root, text="Graph It!", command=graph)
my_button.pack()

root.mainloop()

#NOTES
# matplotlib charts