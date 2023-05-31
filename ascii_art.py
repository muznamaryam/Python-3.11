# Name: Muzna Maryam
# GUI for an ASCII art editor - creates a GUI window for image conversion to ASCII text
# Rules:
# Select the image path of the desired image you want to convert
# Set the Character Image Width to your choice
# Select the GrayScale Method of your choice
# Click on Generate for the ASCII text
# Click on Save to save the generated ASCII text file

import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from PIL import Image

# Define the constants
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# Define the functions
def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image, method="Channel 1"):
    if method == "Channel 1":
        grayscale_image = image.convert("L")
    elif method == "Channel 2":
        grayscale_image = image.convert("RGBA").convert("L")
    elif method == "Channel 3":
        grayscale_image = image.convert("RGB").convert("L")
    else:
        grayscale_image = image.convert("L")
    return grayscale_image

def pixels_to_ascii(image, characters):
    pixels = image.getdata()
    characters = "".join([characters[pixel // 25] for pixel in pixels])
    return characters

def generate():
    image_path = image_path_entry.get()
    character_image_width = character_image_width_entry.get()
    character_set = character_set_entry.get()
    grayscale_method = grayscale_method_var.get()

    try:
        image = Image.open(image_path)
    except:
        print(image_path, "is not a valid pathname to an image.")
        return

    new_width = int(character_image_width)
    new_image_data = pixels_to_ascii(grayify(resize_image(image, new_width), grayscale_method), character_set)

    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[index:(index + new_width)] for index in range(0, pixel_count, new_width)])

    ascii_text_display.delete("1.0", tk.END)
    ascii_text_display.insert(tk.END, ascii_image)

def save_text():
    ascii_text = ascii_text_display.get("1.0", tk.END)
    filename = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt")])
    with open(filename, "w") as f:
        f.write(ascii_text)

def main():
    root = tk.Tk()
    root.title("ASCII Art Editor")

    # Create the image path entry
    image_path_label = tk.Label(root, text="Image Path:")
    image_path_label.pack()

    global image_path_entry
    image_path_entry = tk.Entry(root)
    image_path_entry.pack()

    def select_image_path():
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(tk.END, path)

    select_image_button = tk.Button(root, text="Select Image", command=select_image_path)
    select_image_button.pack()

    # Create the character image width entry
    character_image_width_label = tk.Label(root, text="Character Image Width:")
    character_image_width_label.pack()

    global character_image_width_entry
    character_image_width_entry = tk.Entry(root)
    character_image_width_entry.insert(tk.END, "100")
    character_image_width_entry.pack()

    # Create the character set entry
    character_set_label = tk.Label(root, text="Character Set:")
    character_set_label.pack()

    global character_set_entry
    character_set_entry = tk.Entry(root)
    character_set_entry.insert(tk.END, "".join(ASCII_CHARS))
    character_set_entry.pack()

    # Create the grayscale method selection
    grayscale_method_label = tk.Label(root, text="Grayscale Method:")
    grayscale_method_label.pack()

    global grayscale_method_var
    grayscale_method_var = tk.StringVar(root, "Channel 1")

    grayscale_method_1_radio = tk.Radiobutton(root, text="Channel 1", variable=grayscale_method_var, value="Channel 1")
    grayscale_method_1_radio.pack()

    grayscale_method_2_radio = tk.Radiobutton(root, text="Channel 2", variable=grayscale_method_var, value="Channel 2")
    grayscale_method_2_radio.pack()

    grayscale_method_3_radio = tk.Radiobutton(root, text="Channel 3", variable=grayscale_method_var, value="Channel 3")
    grayscale_method_3_radio.pack()

    # Create the Generate button
    generate_button = tk.Button(root, text="Generate", command=generate)
    generate_button.pack()

    # Create the Save button
    save_button = tk.Button(root, text="Save", command=save_text)
    save_button.pack()

    # Create the ASCII text display
    global ascii_text_display
    ascii_text_display = scrolledtext.ScrolledText(root, width=80, height=30)
    ascii_text_display.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
