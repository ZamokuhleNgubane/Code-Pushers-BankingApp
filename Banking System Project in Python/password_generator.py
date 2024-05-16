import random
import random
import string
import tkinter as tk

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_and_display_password():
    password = generate_password()
    password_label.config(text="Random Password: " + password)

root = tk.Tk()
root.title("Tinka Generator")
root.configure(bg='#29c5f6')

password_label = tk.Label(root, text="")
password_label.pack(pady=10)

generate_button = tk.Button(root, text="Generate Password", command=generate_and_display_password)
generate_button.pack()

root.mainloop()
