import tkinter as tk
from picamera import PiCamera
from PIL import Image, ImageTk
import cv2
import threading

class PiCameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)

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
            self.thread = threading.Thread(target=self.video_stream)
            self.thread.start()

    def stop_camera(self):
        self.running = False
        self.thread.join()

    def video_stream(self):
        while self.running:
            image = self.camera.capture_continuous()
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.window.update()

    def on_closing(self):
        self.running = False
        self.window.quit()
        self.window.destroy()

root = tk.Tk()
app = PiCameraApp(root, "Raspberry Pi Camera")
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
