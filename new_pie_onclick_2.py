import matplotlib.pyplot as plt

arr = []

c = [
'#ff0000',
'#ffaa00',
'#00aaaa',
'#00aa00',
'#aaaa00',
'#ff00ff',
'#00ffaa',
'#ff00aa'
]

l=['a','b','c']
s=[33,33,33]
arr.append([l,s,c])

l=['d','e','f','g']
s=[25,25,25,25]
arr.append([l,s,c])

l=['g','h','i','j','k']
s=[20,20,20,20,20]
arr.append([l,s,c])



class Pie:
    def __init__(self,arr:list):
        self.index = 0
        self.arr = arr
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('button_press_event',self.on_click)

    def draw_pie(self):
        labels = self.arr[self.index][0]
        sizes = self.arr[self.index][1]
        colors = self.arr[self.index][2]
        self.ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')

    def on_click(self,event):
        if event.inaxes == self.ax:
            self.ax.clear()
            self.index += 1
            if self.index>len(self.arr)-1:
                self.index = 0
            self.draw_pie()
            plt.draw()

pie = Pie(arr)
pie.draw_pie()
plt.show()

