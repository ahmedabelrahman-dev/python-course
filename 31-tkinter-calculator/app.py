import tkinter as tk


def calculate_sum():
    try:
        num1 = float(first_number.get())
        num2 = float(second_number.get())

        result = num1 + num2

        result_label.config(text=f"Result: {result}")
    except ValueError:
        result_label.config(text="Please enter valid numbers!")


# create the main window
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("300x250")

title_label = tk.Label(window, text="Simple Calculator", font=("Arial", 16))
title_label.pack(pady=10)

frame1 = tk.Frame(window)
frame1.pack(pady=5)

num1_label = tk.Label(frame1, text="First Number:")
num1_label.pack(side=tk.LEFT)

first_number = tk.Entry(frame1, width=10)
first_number.pack()


frame2 = tk.Frame(window)
frame2.pack(pady=5)

num2_label = tk.Label(frame2, text="Second Number:")
num2_label.pack(side=tk.LEFT)

second_number = tk.Entry(frame2, width=10)
second_number.pack()

calculate_button = tk.Button(window, text="Add Numbers", command=calculate_sum)
calculate_button.pack(pady=10)

result_label = tk.Label(window, text="Result: ", font=("Arial", 12))
result_label.pack(pady=10)


def clear_fields():
    first_number.delete(0, tk.END)
    second_number.delete(0, tk.END)
    result_label.config(text="Result: ")


clear_button = tk.Button(window, text="Clear", command=clear_fields)
clear_button.pack(pady=5)

window.mainloop()
