#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kol
#
# Created:     20.01.2020
# Copyright:   (c) kol 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cv2
import numpy as np
import os
import tkinter as tk

from tkinter import filedialog
#from PIL import ImageGrab as ig
from PIL import Image
from mss import mss
import win32gui

class GetVideoApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, "get_video")

        self.count = 5
        self.file_name = None
        self.bbox = None
        self.window_text = None
        self.sct = None
        self.out = None
        self.frame_count = None

        self.attributes("-toolwindow", True)
        self.attributes("-topmost", True)

        self.title("Video recorder")

        x = self.winfo_screenwidth() - 300
        y = self.winfo_screenheight() - 200
        self.geometry("%+d%+d" % (x, y))

        self.resizable(False, False)

        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.statusLabel = tk.Label(self.frame, text="Click Start to begin")
        self.statusLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady = 10, padx = 5)

        self.titleLabel = tk.Label(self.frame, text="")
        self.titleLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady = 10, padx = 5)

        button_frame = tk.Frame(self.frame)
        button_frame.pack(side=tk.BOTTOM)

        self.startBtn = tk.Button(button_frame, text = "Start",
            command = self.start_callback)
        self.startBtn.pack(side=tk.LEFT, padx = 10, pady = 5)

        self.cancelBtn = tk.Button(button_frame, text = "Stop",
            command = self.cancel_callback, state = tk.DISABLED)
        self.cancelBtn.pack(side=tk.LEFT, padx = 10, pady = 5)

        tk.Button(button_frame, text = "Close", command = self.close_callback).pack(
            side=tk.LEFT, padx = 10, pady = 5)

        self.bind('<Escape>', self.esc_callback)

    def start_callback(self):
        self.file_name = self.get_filename()
        if self.file_name is None or self.file_name == '':
            return

        self.cancelBtn.configure(state = tk.NORMAL)
        self.startBtn.configure(state = tk.DISABLED)

        self.count = 5
        self.statusLabel.configure(text = "Activate target window: {}".format(self.count))
        self.after(1000, self.count_down)

    def cancel_callback(self):
        self.count = -1
        self.statusLabel.configure(text="Click Start to begin")
        self.titleLabel.configure(text = 'Done')
        self.cancelBtn.configure(state = tk.DISABLED)
        self.startBtn.configure(state = tk.NORMAL)

    def esc_callback(self, event):
        self.cancel_callback()

    def close_callback(self):
        #self.grab_release()
        self.destroy()

    def count_down(self):
        if self.count < 0:
            return

        self.count -= 1
        if self.count > 0:
            self.statusLabel.configure(text = "Activate target window: {}".format(self.count))
            self.after(1000, self.count_down)
        else:
            self.statusLabel.configure(text = "Capturing video from:")

            self.bbox, self.window_text = self.get_window()
            self.titleLabel.configure(text = self.window_text)

            self.after(20, self.start_capture)

    def start_capture(self):
        w, h = self.bbox[2]-self.bbox[0], self.bbox[3]-self.bbox[1]

        self.frame_count = 0
        self.sct = mss()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.file_name, fourcc, 20.0, (w, h))

        self.after(20, self.capture_frame())

    def capture_frame(self):
        self.frame_count += 1
        print("Frame {}, count {}".format(self.frame_count, self.count))
        w, h = self.bbox[2]-self.bbox[0], self.bbox[3]-self.bbox[1]

        monitor = {'left': self.bbox[0], 'top': self.bbox[1],
                   'width': w, 'height': h}
        img_rgb = Image.frombytes('RGB', (w, h), self.sct.grab(monitor).rgb)
        img_bgr = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)
        self.out.write(img_bgr)

        if self.count >= 0:
            self.update()
            self.after(20, self.capture_frame())
        else:
            print("Done")
            self.out.release()

    def get_filename(self):
        return filedialog.asksaveasfilename(title = "Save video",
            defaultextension = '.avi',
            filetypes = (("AVI files","*.avi"),("All files","*.*")))

    def get_window(self):
        hwnd = win32gui.GetForegroundWindow()
        bbox = win32gui.GetWindowRect(hwnd)
        text = win32gui.GetWindowText(hwnd)
        return bbox, text


def main():
    app = GetVideoApp()
    app.mainloop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
