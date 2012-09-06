import sys
from Tkinter import *


def run(mod, size=600, itermax=100):
    mandel = __import__(mod).mandel
    x_center = -1.0
    y_center = 0.0
    zoom = 4.0

    bitmap = mandel(size, itermax, x_center, y_center, zoom)

    root = Tk()
    w = Canvas(root, width=size, height=size)
    w.pack()

    for y, row in enumerate(bitmap):
        for x, color in enumerate(row):
            w.create_line(x, size - y, x + 1, size + 1 - y, fill=color == 0 and 'black' or 'white')
            w.pack()
    print 'done'
    root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    elif len(sys.argv) == 4:
        run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        sys.exit('invalid arguments')
