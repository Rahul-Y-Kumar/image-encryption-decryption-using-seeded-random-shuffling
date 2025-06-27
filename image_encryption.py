import os
import random
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox
from PIL import Image

# Get seeded random generator
def get_seeded_random(seed):
    return random.Random(seed)

# Encrypt the image
def encrypt_image(input_image_path, output_image_path, seed):
    try:
        image = Image.open(input_image_path).convert("RGB")
        width, height = image.size
        pixels = list(image.getdata())

        random_gen = get_seeded_random(seed)
        indices = list(range(len(pixels)))
        random_gen.shuffle(indices)

        encrypted_pixels = [pixels[i] for i in indices]
        encrypted_image = Image.new("RGB", (width, height))
        encrypted_image.putdata(encrypted_pixels)
        encrypted_image.save(output_image_path)
        return True
    except Exception as e:
        messagebox.showerror("Encryption Error", f"An error occurred: {str(e)}")
        return False

# Decrypt the image
def decrypt_image(input_image_path, output_image_path, seed):
    try:
        image = Image.open(input_image_path).convert("RGB")
        width, height = image.size
        encrypted_pixels = list(image.getdata())

        random_gen = get_seeded_random(seed)
        indices = list(range(len(encrypted_pixels)))
        random_gen.shuffle(indices)

        decrypted_pixels = [None] * len(encrypted_pixels)
        for original_index, shuffled_index in enumerate(indices):
            decrypted_pixels[shuffled_index] = encrypted_pixels[original_index]

        decrypted_image = Image.new("RGB", (width, height))
        decrypted_image.putdata(decrypted_pixels)
        decrypted_image.save(output_image_path)
        return True
    except Exception as e:
        messagebox.showerror("Decryption Error", f"An error occurred: {str(e)}")
        return False

# Select input image
def select_input_image():
    input_image_path = filedialog.askopenfilename(title="Select Image")
    if input_image_path:
        input_image_label.config(text=input_image_path)

# Select output image path
def select_output_image():
    output_image_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")],
        title="Save Encrypted/Decrypted Image"
    )
    if output_image_path:
        output_image_label.config(text=output_image_path)

# Encrypt button handler
def encrypt():
    input_image_path = input_image_label.cget("text")
    output_image_path = output_image_label.cget("text")
    seed = seed_entry.get()

    if not input_image_path or not output_image_path or not seed:
        messagebox.showerror("Error", "Please select input/output and enter a seed.")
        return

    try:
        seed_int = int(seed)
    except ValueError:
        messagebox.showerror("Error", "Seed must be an integer.")
        return

    if encrypt_image(input_image_path, output_image_path, seed_int):
        messagebox.showinfo("Success", "Image encrypted successfully!")

# Decrypt button handler
def decrypt():
    input_image_path = input_image_label.cget("text")
    output_image_path = output_image_label.cget("text")
    seed = seed_entry.get()

    if not input_image_path or not output_image_path or not seed:
        messagebox.showerror("Error", "Please select input/output and enter a seed.")
        return

    try:
        seed_int = int(seed)
    except ValueError:
        messagebox.showerror("Error", "Seed must be an integer.")
        return

    if decrypt_image(input_image_path, output_image_path, seed_int):
        messagebox.showinfo("Success", "Image decrypted successfully!")

# GUI Setup
root = Tk()
root.title("Image Encryption & Decryption Tool")

Label(root, text="Select Image to Encrypt/Decrypt:").pack(pady=5)
input_image_label = Label(root, text="No image selected", wraplength=400)
input_image_label.pack(pady=5)
Button(root, text="Browse", command=select_input_image).pack(pady=5)

Label(root, text="Output Image Path:").pack(pady=5)
output_image_label = Label(root, text="No output path selected", wraplength=400)
output_image_label.pack(pady=5)
Button(root, text="Save As", command=select_output_image).pack(pady=5)

Label(root, text="Enter Seed Key (integer):").pack(pady=5)
seed_entry = Entry(root)
seed_entry.pack(pady=5)

Button(root, text="Encrypt Image", command=encrypt).pack(pady=10)
Button(root, text="Decrypt Image", command=decrypt).pack(pady=5)

root.mainloop()
