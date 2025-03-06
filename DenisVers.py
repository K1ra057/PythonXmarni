import string
import tkinter as tk
from tkinter import filedialog, messagebox


def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift

    result = ""
    for char in text:
        if char.isalpha():
            alphabet = string.ascii_lowercase if char.islower() else string.ascii_uppercase
            new_char = alphabet[(alphabet.index(char) + shift) % 26]
            result += new_char
        else:
            result += char
    return result


def encrypt_file():
    file_path = filedialog.askopenfilename(title="Виберіть файл для шифрування")
    if not file_path:
        return

    shift = int(shift_entry.get())
    with open(file_path, 'r', encoding='utf-8') as infile:
        text = infile.read()

    encrypted_text = caesar_cipher(text, shift)
    output_filename = filedialog.asksaveasfilename(defaultextension=".txt", title="Збережіть зашифрований файл")
    if output_filename:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(encrypted_text)
        messagebox.showinfo("Успіх", "Файл успішно зашифровано!")


def decrypt_file():
    file_path = filedialog.askopenfilename(title="Виберіть файл для розшифрування")
    if not file_path:
        return

    shift = int(shift_entry.get())
    with open(file_path, 'r', encoding='utf-8') as infile:
        encrypted_text = infile.read()

    decrypted_text = caesar_cipher(encrypted_text, shift, decrypt=True)
    messagebox.showinfo("Розшифрований текст", decrypted_text)


# Інтерфейс
root = tk.Tk()
root.title("Шифр Цезаря")
root.geometry("300x200")

tk.Label(root, text="Введіть зміщення:").pack()
shift_entry = tk.Entry(root)
shift_entry.pack()

encrypt_button = tk.Button(root, text="Шифрувати файл", command=encrypt_file)
encrypt_button.pack(pady=5)

decrypt_button = tk.Button(root, text="Розшифрувати файл", command=decrypt_file)
decrypt_button.pack(pady=5)

root.mainloop()