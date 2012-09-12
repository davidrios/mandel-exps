import sys
from Tkinter import *
from PIL import Image, ImageTk

x_center = -1.0
y_center = 0.0
zoom = 4.0


def run(mod, size=600, itermax=5000):
    mandel = __import__(mod)

    root = Tk()
    w = Canvas(root, width=size, height=size)

    def redraw():
        w.delete(ALL)
        bitmap = mandel.mandel(size, itermax, x_center, y_center, zoom)
        im = Image.fromstring('L', (size, size), bitmap)
        w.photo = ImageTk.PhotoImage(im)
        w.create_image(0, 0, anchor='nw', image=w.photo)

    def handle_click(ev):
        global x_center, y_center
        x_center = mandel.convert_x2r(ev.x, x_center, size, zoom)
        y_center = mandel.convert_y2i(ev.y, y_center, size, zoom)
        redraw()

    def handle_plus(ev):
        global zoom
        zoom /= 2
        redraw()

    def handle_minus(ev):
        global zoom
        zoom *= 2
        redraw()

    w.bind('<Button-1>', handle_click)
    root.bind('<Key-Up>', handle_plus)
    root.bind('<Key-Down>', handle_minus)
    w.pack()
    redraw()
    root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    elif len(sys.argv) == 4:
        run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        sys.exit('invalid arguments')
