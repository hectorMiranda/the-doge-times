import tkinter as tk
from PIL import Image, ImageTk
import threading
import cv2
from flask import Flask, render_template, Response

class DogeMonitor:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.app = Flask(__name__)
        self.setup_routes()

        self.camera = cv2.VideoCapture(video_source)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        self.btn_capture = tk.Button(window, text="Capture", width=10, command=self.capture_image)
        self.btn_capture.pack(padx=20, pady=10, side=tk.LEFT)


        # Camera button
        self.btn_camera = tk.Button(window, text="Start Camera", width=15, command=self.toggle_camera)
        self.btn_camera.pack(padx=20, pady=10, side=tk.LEFT)

        # Web server button
        self.btn_web_server = tk.Button(window, text="Start Web Server", width=15, command=self.toggle_web_server)
        self.btn_web_server.pack(padx=20, pady=10, side=tk.LEFT)

        self.camera_running = False
        self.server_running = False
        self.server_thread = None

        self.running = False
    
    def setup_routes(self):
        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


    def toggle_camera(self):
        if self.camera_running:
            self.stop_camera()
            self.btn_camera.config(text="Start Camera")
        else:
            self.start_camera()
            self.btn_camera.config(text="Stop Camera")
        self.camera_running = not self.camera_running

    def toggle_web_server(self):
        if self.server_running:
            self.stop_web_server()
            self.btn_web_server.config(text="Start Web Server")
        else:
            self.start_web_server()
            self.btn_web_server.config(text="Stop Web Server")
        self.server_running = not self.server_running

    def start_web_server(self):
        if not self.server_thread:
            self.server_thread = threading.Thread(target=self.run_flask)
            self.server_thread.daemon = True
            self.server_thread.start()

    def run_flask(self):
        self.app.run(host='0.0.0.0', port=5000, use_reloader=False)

    def stop_web_server(self):
        # Stopping Flask server running in a separate thread is tricky
        # One approach is to use a global variable to signal the server to stop
        # Alternatively, simply leave the server running until the main application is closed
        pass
    

    def generate_frames():
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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
    
    def capture_image(self):
        if self.running:
            # Capture frame directly in BGR format
            ret, bgr_frame = self.camera.read()
            if ret:
                cv2.imwrite('captured_frame.jpg', bgr_frame)
                print("Image captured and saved as 'captured_frame.jpg'")
            else:
                print("Failed to capture frame for image")



    def on_closing(self):
        if self.running:
            self.running = False
        self.window.quit()
        self.window.destroy()
        self.camera.release()

root = tk.Tk()
app = DogeMonitor(root, "USB Camera with Raspberry Pi")
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
