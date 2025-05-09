import cv2
import os
import time
from datetime import datetime
from threading import Thread
from tkinter import *
from PIL import Image, ImageTk

NUM_IMG = 60

# Initialize webcams
camera_paths = [0, 2, 4, 6]
cameras = [cv2.VideoCapture(port) for port in camera_paths]
for camera in cameras:
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    camera.set(cv2.CAP_PROP_FPS, 15)

# Path for cow ID file
cow_id_file_path = '/home/pi/Desktop/NTU20250509/cow_id.txt'

def load_cow_id():
    try:
        with open(cow_id_file_path, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def save_cow_id(cow_id):
    with open(cow_id_file_path, 'w') as file:
        file.write(str(cow_id))

def flush_camera_buffer(camera, num_flush_frames=5):
    for _ in range(num_flush_frames):
        ret, frame = camera.read()
        if not ret:
            print_output("Failed to read frame while flushing buffer")

cow_id = load_cow_id()

def print_output(message):
    text_box.insert(END, message + "\n")
    text_box.see(END)

def handle_button_a():
    global cow_id
    cow_id += 1
    save_cow_id(cow_id)
    directory_name = f'{cow_id}'
    os.makedirs(f'/home/pi/Desktop/NTU20250509/{directory_name}', exist_ok=True)
    print_output(f"Directory created: /home/pi/Desktop/NTU20250509/{directory_name}")
    show_initial_view()

def show_initial_view():
    flush_camera_buffer(cameras[3])
    ret, frame = cameras[3].read()
    if ret:
        # Resize frame to fit GUI
        frame = cv2.resize(frame, (480, 360))
        
        # Draw alignment box in the center of the frame
        height, width, _ = frame.shape
        box_size = 50
        start_point = (width // 2 - box_size // 2, height // 2 - box_size // 2)
        end_point = (width // 2 + box_size // 2, height // 2 + box_size // 2)
        box_color = (255, 0, 0)  # Red color for the alignment box
        cv2.rectangle(frame, start_point, end_point, box_color, 2)
        
        # Convert the OpenCV image (frame) to a PIL Image
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Assuming 'panel' is the Tkinter Label where the image is to be displayed
        panel.imgtk = imgtk  # Keep a reference, prevent garbage-collection
        panel.configure(image=imgtk)

def capture_single_camera(camera, directory, camera_index, num_images):
    for img_count in range(num_images):
        # camera.set(cv2.CAP_PROP_POS_FRAMES, 1)  # Attempt to clear the buffer
        flush_camera_buffer(camera)
        ret, frame = camera.read()
        if ret:
            # Include more precise datetime in filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f'{directory}/cam{camera_index}_{timestamp}.jpg'
            cv2.imwrite(filename, frame)
            print(f"Image saved: {filename}")
        else:
            print(f"Failed to capture image from camera {camera_index}")
        time.sleep(1 / 6)  # Interval in seconds (1 / FPS)
        
def capture_images():
    show_initial_view()
    num_images = NUM_IMG  # Total number of images to capture
    current_directory = f'/home/pi/Desktop/NTU20250509/{cow_id}'
    if not os.path.exists(current_directory):
        os.makedirs(current_directory)
        print_output(f"Directory created: {current_directory}")

    threads = []
    print_output(f"Start Capturing in {current_directory}")

    for i, camera in enumerate(cameras):
        thread = Thread(target=capture_single_camera, args=(camera, current_directory, i + 1, num_images))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        
    print_output(f"===Saved in {current_directory}, {NUM_IMG}/cam====")

def main():
    root = Tk()
    root.title("Cow Image Capture System")
    root.geometry("1024x600")  # Set the window to match your monitor resolution

    global panel
    panel = Label(root)  # Image panel
    panel.pack(side="top", fill="both", expand="yes")

    btn_view = Button(root, text="Show Initial View", command=show_initial_view)
    btn_view.pack(side="left", fill="both", expand="yes")
    
    btn_a = Button(root, text="Create Directory", command=handle_button_a)
    btn_a.pack(side="left", fill="both", expand="yes")

    btn_b = Button(root, text="Capture Images", command=capture_images)
    btn_b.pack(side="right", fill="both", expand="yes")

    global text_box
    text_box = Text(root, height=10)
    text_box.pack(side="bottom", fill="both", expand="yes")

    show_initial_view()  # Show initial view from the first camera
    root.mainloop()

if __name__ == '__main__':
    try:
        main()
    finally:
        print("Releasing cameras and cleaning up.")
        for camera in cameras:
            camera.release()

