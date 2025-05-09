import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageDraw, ImageTk, ImageFont
import cv2
import io

class CameraAlignmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Alignment Interface")
        self.root.geometry("1024x600")

        self.cameras = [cv2.VideoCapture(i) for i in [0, 2, 4, 6]]  # Initialize cameras
        for cam in self.cameras:
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        self.frames = []

        self.preview_frame = tk.Frame(self.root)
        self.preview_frame.pack(side="top", fill="both", expand=True)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="bottom", fill="x")

        self.alignment_button = Button(self.button_frame, text="Align Cameras", command=self.align_cameras)
        self.alignment_button.pack()

        self.create_camera_frames()
        self.root.after(3000, self.update_camera_views)

    def create_camera_frames(self):
        for i in range(2):
            for j in range(2):
                frame = Label(self.preview_frame, width=512, height=270)
                frame.grid(row=i, column=j, padx=5, pady=5)
                self.frames.append(frame)

    def align_cameras(self):
        self.update_camera_views()

    def update_camera_views(self):
        images = [self.capture_image(i) for i in range(len(self.cameras))]
        self.update_camera_frames(images)
        self.root.after(1000, self.update_camera_views)
    
    def flush_camera_buffer(self, camera, num_flush_frames=5):
        for _ in range(num_flush_frames):
            ret, frame = camera.read()
            if not ret:
                print_output("Failed to read frame while flushing buffer")
    
    def capture_image(self, cam_index):
        self.flush_camera_buffer(self.cameras[cam_index])
        ret, frame = self.cameras[cam_index].read()
        if not ret:
            return self.create_error_image("Camera not available")

        # Convert frame to PIL Image to use with Tkinter
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = image.resize((512, 270), Image.ANTIALIAS)
        return image

    def create_error_image(self, message):
        image = Image.new('RGB', (512, 270), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        text_width, text_height = draw.textsize(message, font=font)
        position = ((512 - text_width) // 2, (270 - text_height) // 2)
        draw.text(position, message, (255, 255, 255), font=font)
        return image

    def update_camera_frames(self, images):
        for i, img in enumerate(images):
            self.draw_alignment_box(img)
            img = ImageTk.PhotoImage(img)
            self.frames[i].config(image=img)
            self.frames[i].image = img

    def draw_alignment_box(self, img):
        draw = ImageDraw.Draw(img)
        box_size = 40
        box_color = 'yellow'
        start_point = (img.width // 2 - box_size // 2, img.height // 2 - box_size // 2)
        end_point = (img.width // 2 + box_size // 2, img.height // 2 + box_size // 2)
        draw.rectangle([start_point, end_point], outline=box_color, width=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraAlignmentApp(root)
    root.mainloop()
