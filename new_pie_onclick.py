import matplotlib.pyplot as plt

class Pie:
    def __init__(self):
        self.index = 3
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('button_press_event',self.on_click)

    def draw_pie(self):
        s = str(self.index)
        labels=[s]*self.index
        sizes=[10]*self.index
        self.ax.pie(sizes, labels=labels,  autopct='%1.1f%%')

    def on_click(self,event):
        if event.inaxes == self.ax:
            self.ax.clear()
            self.index += 1
            self.draw_pie()
            plt.draw()

pie = Pie()
pie.draw_pie()
plt.show()

