import tkinter as tk
from PIL import Image, ImageTk
import cv2

class USB_Camera_App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.camera = cv2.VideoCapture(video_source)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start_camera)
        self.btn_start.pack(padx=20, pady=10, side=tk.LEFT)

        self.btn_stop = tk.Button(window, text="Stop", width=10, command=self.stop_camera)
        self.btn_stop.pack(padx=20, pady=10, side=tk.RIGHT)

        self.running = False

    def start_camera(self):
        if not self.running:
            self.running = True
            self.update_frame()

    def stop_camera(self):
        self.running = False

    def update_frame(self):
        if self.running:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                self.imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgtk)
                self.window.after(10, self.update_frame)
            else:
                print("Failed to capture frame")

    def on_closing(self):
        if self.running:
            self.running = False
        self.window.quit()
        self.window.destroy()
        self.camera.release()

root = tk.Tk()
app = USB_Camera_App(root, "USB Camera with Raspberry Pi")
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
