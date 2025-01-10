import cv2
import time
import os
import serial

# Create a folder to save images if it doesn't exist
save_dir = "captured_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Start the video capture from the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

try:
    arduino = serial.Serial("/dev/tty.usbserial-14110", baudrate=9600, timeout=5)
except:
    arduino = None
    print("Please check the port")

# Function to display the most recent captured image and close window immediately after
def display_recent_image():
    images = [f for f in os.listdir(save_dir) if f.endswith('.jpg')]
    if images:
        # Sort the images to get the most recent one
        images.sort(reverse=True)
        most_recent_image = images[0]
        img_path = os.path.join(save_dir, most_recent_image)
        image = cv2.imread(img_path)
        cv2.imshow(f"Captured Image: {most_recent_image}", image)
        cv2.waitKey(1)  # Display briefly
        cv2.destroyAllWindows()  # Close the window after display

# Start the loop to capture images every 10 seconds if Arduino input is 1
try:
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to grab frame.")
            break

        try:
            person = int(arduino.readline().decode('utf-8').strip())
        except:
            person = 1
        # Only capture if Arduino input == 1
        if person == 1:
            # Get the current timestamp to use in the filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_dir, f"image_{timestamp}.jpg")

            # Save the captured frame as an image file
            cv2.imwrite(filename, frame)
            print(f"Captured and saved {filename}")

            # Display the most recent image and close the window immediately after
            display_recent_image()

        # Wait for 1 second before capturing the next image
        time.sleep(1)

except KeyboardInterrupt:
    print("\nCapture stopped by user.")

finally:
    # Release the video capture object and close any open windows
    cap.release()
    cv2.destroyAllWindows()