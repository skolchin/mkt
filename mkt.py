#-------------------------------------------------------------------------------
# Name:        Transparent image
# Purpose:     Small script to make transparent images
#              Origin https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
#
# Author:      kol
#
# Created:     18.11.2019
# Copyright:   (c) kol 2019
# Licence:     MIT
#-------------------------------------------------------------------------------
import os
import cv2
import tkinter as tk
from PIL import Image

from tkinter import filedialog
from tkinter import messagebox

click_x, click_y = None, None
transp_image = None

def show_help():
    messagebox.showinfo('Transparent color maker',
                        'Click on the image to select transparent color.\n' + \
                        'Press SPACE to make selected color transparent.\n' + \
                        'Press S to save image.\n' + \
                        'Press Q to quit.')


def onMouse(event, x, y, flags, param):
    global click_x, click_y

    if event == cv2.EVENT_LBUTTONDOWN:
        img = param[0]
        click_x, click_y = x, y
        messagebox.showinfo('Transparent color maker',
            'Color {} selected as transparent. Press SPACE to convert, S to save'.format(img[y, x]))

def display(filename):
    global click_x, click_y, transp_image

    img = cv2.imread(filename)
    if img is None:
        raise Exception('File not found', filename)
    cv2.namedWindow('Image')
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', onMouse, [img])

    while True:
        key = cv2.waitKey()
        if key & 0xFF == ord('q') or key & 0xFF == ord('Q'):
            break

        if click_x is None:
            show_help()
        elif key & 0xFF == ord(' '):
            clr = img[click_y, click_x]
            clr = tuple([c for c in reversed(clr)])
            transparent(filename, clr)

        elif key & 0xFF == ord('s') or key & 0xFF == ord('S'):
            if transp_image is None:
                show_help()
            else:
                os.rename(filename, filename + '.bak')
                transp_image.save(filename)
                messagebox.showinfo('Transparent color maker',
                                    'Converted image saved as ' + filename + '. Press Q to quit')

def transparent(src_file, transp_color = (255, 255, 255)):
    global transp_image

    transp_image = Image.open(src_file)
    transp_image = transp_image.convert("RGBA")

    check_color = transp_color + (255, )
    replace_color = transp_color + (0, )

    pixdata = transp_image.load()

    width, height = transp_image.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == check_color:
                pixdata[x, y] = replace_color

    messagebox.showinfo('Transparent color maker',
                        'Color {} converted to transparent. Press S to save image'.format(transp_color))

def main():
    root = tk.Tk()
    root.withdraw()

    # Convert
    file_path = filedialog.askopenfilename(
        filetypes=(('PNG files (*.png)', '*.png'), ('JPEG files (*.jpeg)', '*.jpeg')),
        title='Select image file',
        defaultextension='.png')

    # Convert image
    if file_path != '':
        display(file_path)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
