import sys
from Tkinter import *
from PIL import Image, ImageTk


def run(mod, size=600, itermax=100):
    mandel = __import__(mod).mandel
    x_center = -1.0
    y_center = 0.0
    zoom = 4.0

    bitmap = mandel(size, itermax, x_center, y_center, zoom)
    bitmapstr = ''.join(''.join(chr(j) for j in i) for i in bitmap)

    im = Image.fromstring('L', (size, size), bitmapstr)

    root = Tk()
    w = Canvas(root, width=size, height=size)
    w.pack()
    w.photo = ImageTk.PhotoImage(im)
    w.create_image(0, 0, anchor='nw', image=w.photo)
    root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    elif len(sys.argv) == 4:
        run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        sys.exit('invalid arguments')
