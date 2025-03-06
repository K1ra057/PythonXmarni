import string
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from collections import Counter


# Функція для знаходження ймовірного ключа шифру Цезаря
# Використовує припущення, що найчастіша літера в англійській мові — 'e'
def find_caesar_shift(frequencies):
    most_common_char = max(frequencies, key=frequencies.get)  # Знаходимо найчастішу букву у тексті
    assumed_most_common = 'e'  # Припускаємо, що вона відповідає 'e'

    if most_common_char in string.ascii_lowercase:
        shift = (ord(most_common_char) - ord(assumed_most_common)) % 26
    elif most_common_char in string.ascii_uppercase:
        shift = (ord(most_common_char) - ord(assumed_most_common.upper())) % 26
    else:
        shift = None  # Якщо неможливо визначити зміщення

    return shift


# Функція для розшифрування тексту шифром Цезаря
# Використовує знайдене зміщення shift для відновлення вихідного тексту
def decrypt_caesar_cipher(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            alphabet = string.ascii_lowercase if char.islower() else string.ascii_uppercase
            new_char = alphabet[(alphabet.index(char) - shift) % 26]  # Зсуваємо букву назад на shift позицій
            decrypted_text += new_char
        else:
            decrypted_text += char  # Неалфавітні символи залишаємо без змін
    return decrypted_text


# Основна функція для аналізу частоти символів у файлі
def frequency_analysis(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        messagebox.showerror("Помилка", "Файл не знайдено!")
        return

    # Видаляємо всі неалфавітні символи
    text_filtered = ''.join(filter(str.isalpha, text))
    total_chars = len(text_filtered)
    char_counts = Counter(text_filtered)  # Підраховуємо частоту появи кожного символу

    # Обчислюємо відносну частоту кожної букви
    frequencies = {char: count / total_chars for char, count in char_counts.items()}

    # Визначаємо можливий ключ шифрування
    shift = find_caesar_shift(frequencies)

    # Формуємо текст для виводу результатів
    result_text = "Частотний аналіз символів у файлі:\n"
    for char, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
        result_text += f"Символ: '{char}' | Частота: {freq:.4f}\n"

    if shift is not None:
        decrypted_text = decrypt_caesar_cipher(text, shift)  # Розшифровуємо текст за знайденим ключем
        result_text += f"\nЙмовірний ключ шифрування (зміщення): {shift}\n"
        result_text += f"\nРозшифрований текст:\n{decrypted_text}"
    else:
        result_text += "\nНе вдалося визначити ключ шифрування."

    # Створюємо нове вікно для виводу результатів
    result_window = tk.Toplevel(root)
    result_window.title("Результати аналізу")
    result_window.geometry("600x400")

    # Додаємо текстове поле з прокруткою для перегляду результатів
    text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=70, height=20)
    text_area.insert(tk.INSERT, result_text)
    text_area.config(state=tk.DISABLED)  # Робимо поле тільки для читання
    text_area.pack(padx=10, pady=10)


# Функція для відкриття файлу і запуску аналізу
def analyze_file():
    file_path = filedialog.askopenfilename(title="Виберіть файл для аналізу")
    if file_path:
        frequency_analysis(file_path)


# Головне вікно програми
root = tk.Tk()
root.title("Частотний аналіз")
root.geometry("400x200")

# Додаємо кнопку для запуску аналізу
tk.Label(root, text="Виберіть файл для аналізу:").pack()
analyze_button = tk.Button(root, text="Аналізувати файл", command=analyze_file)
analyze_button.pack(pady=10)

root.mainloop()
