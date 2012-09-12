import os
import sys
from os import path
from Tkinter import *
from PIL import Image, ImageTk, ImageDraw

x_center = -1.0
y_center = 0.0
zoom = 4.0
out_dir = path.join(path.curdir, 'out')

x_center = -1.30996188862
y_center = -0.0658154120439
zoom = 1.19209289551e-07

x_center = -1.30996188862
y_center = -0.0658154120392
zoom = 1.7763568394e-15


def draw_text(im, text, pos):
    draw = ImageDraw.Draw(im)
    text_size = draw.textsize(text)
    draw.rectangle((0, text_size[1] * pos, text_size[0], text_size[1] * pos + text_size[1]), fill='black')
    draw.text((0, text_size[1] * pos), text, fill='white')


def run(mod, size=600, itermax=600):
    mandel = __import__(mod)

    root = Tk()
    w = Canvas(root, width=size, height=size)

    def redraw():
        w.delete(ALL)
        bitmap = mandel.mandel(size, itermax, x_center, y_center, zoom)
        im = Image.fromstring('L', (size, size), bitmap)
        draw_text(im, 'x_c: %.69f' % x_center, 0)
        draw_text(im, 'y_c: %.69f' % y_center, 1)
        draw_text(im, 'zoom: %.69f' % zoom, 2)
        w.pil_im = im
        w.photo = ImageTk.PhotoImage(im)
        w.create_image(0, 0, anchor='nw', image=w.photo)
        print x_center, y_center, zoom

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

    def handle_print(ev):
        fname = 'mandel_%05d.png' % len([i for i in os.listdir(out_dir) if i.startswith('mandel_')])
        fpath = path.join(out_dir, fname)
        w.pil_im.save(fpath, optimize=True)
        print 'saved image: %s' % fpath

    w.bind('<Button-1>', handle_click)
    root.bind('<Key-Up>', handle_plus)
    root.bind('<Key-Down>', handle_minus)
    root.bind('<Key-p>', handle_print)
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
