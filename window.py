from tkinter import *
from tkinter import Tk, Label, Canvas, Entry, Button
import tkinter.font as tkFont
import tkinter as tk
from tkinter import Canvas


# Create the main window
root = Tk()
root.title("Welcome to Your Personal Task Manager")
root.configure(bg='light blue')

# Set the window size
root.geometry("600x500")  # Increased width for more horizontal space

# Create a custom font
custom_font = tkFont.Font(family="Helvetica", size=20, weight="bold")

# Create a label with the main message
label = Label(root, text="Welcome to Your Personal Task Manager", font=custom_font, bg='light blue', fg='purple')
label.pack(pady=20)

# Create a label with the secondary message
secondary_label = Label(root, text="Click anywhere to start", font=("Helvetica", 16), bg='light blue', fg='black')
secondary_label.pack(pady=10)

# Center the labels
label.place(relx=0.5, rely=0.4, anchor=CENTER)
secondary_label.place(relx=0.5, rely=0.6, anchor=CENTER)


def create_calendar(event):
    for widget in root.winfo_children():
        widget.destroy()


    global canvas
    canvas = tk.Canvas(root, width=600, height=400, bg='white')
    canvas.pack(pady=20)

    # Draw a larger rectangle (weekly calendar)
    canvas.create_rectangle(20, 20, 580, 380, outline='black', width=4)

    # Draw vertical lines to create 7 columns and add day labels
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for i in range(7):
        x = 20 + i * (560 // 7)
        canvas.create_line(x, 20, x, 380, fill='black')
        canvas.create_text(x + (560 // 14), 10, text=days[i], font=("Helvetica", 12))

        # Bind click event to each column
        canvas.tag_bind(canvas.create_rectangle(x, 20, x + (560 // 7), 380, outline=''), '<Button-1>',
                         lambda e, day=days[i]: create_day_screen(day, canvas, x))

    # Add squares under each column
    rectangles = add_squares(canvas)

    # Display saved times on top of the squares
    for day, rect in rectangles.items():
        if day in times:
            x = 20 + days.index(day) * (560 // 7)
            text_id = canvas.create_text(x + (560 // 14), 360, text=times[day], font=("Helvetica", 12), anchor=tk.N)  # Adjusted y coordinate to 360
            canvas.tag_raise(text_id)  # Ensure text is on top of the

# Function to add squares under each column
def add_squares(canvas):
    days_of_week = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    rectangles = {}
    for i in range(7):
        x = 20 + i * (560 // 7)
        rect = canvas.create_rectangle(x, 360, x + (560 // 7), 380, fill='white')
        rectangles[days_of_week[i]] = rect
        canvas.tag_lower(rect)  # Ensure the rectangle is below the text
    return rectangles

# Function to create a new screen for each day
# Define global variables to store the numbers
num1, num2 = 0, 0

def create_day_screen(day, canvas, x):
    global num1, num2

    for widget in root.winfo_children():
        widget.destroy()

    day_label = Label(root, text=f"Tasks for {day}", font=("Helvetica", 20, "bold"), bg='light blue', fg='purple')
    day_label.pack(pady=20)

    # Entry for wake up time and sleep time
    time_label = Label(root, text="Number1 = wake up time\nNumber2 = sleep time", font=("Helvetica", 14), bg='light blue', fg='black')
    time_label.pack(pady=5)
    time_entry = Entry(root, font=("Helvetica", 14), width=35)
    time_entry.pack(pady=5)

    # Add placeholder text for time entry
    time_entry.insert(0, "0 0")
    time_entry.config(fg='grey')

    def on_click_time(event):
        if time_entry.get() == "0 0":
            time_entry.delete(0, "end")
            time_entry.config(fg='black')

    def on_focusout_time(event):
        if time_entry.get() == "":
            time_entry.insert(0, "0 0")
            time_entry.config(fg='grey')

    time_entry.bind("<FocusIn>", on_click_time)
    time_entry.bind("<FocusOut>", on_focusout_time)

    def store_numbers():
        global num1, num2
        input_text = time_entry.get()
        numbers = input_text.split()
        num1, num2 = int(numbers[0]), int(numbers[1])
        print(f"Stored Number 1: {num1}, Stored Number 2: {num2}")


    # Entry for tasks
    tasks_label = Label(root, text="Enter your task and time", font=("Helvetica", 14), bg='light blue', fg='black')
    tasks_label.pack(pady=5)
    tasks_entry = Entry(root, font=("Helvetica", 14), width=50)
    tasks_entry.pack(pady=5)

    # Add placeholder text for tasks entry
    tasks_entry.insert(0, "task 0AM-0PM")
    tasks_entry.config(fg='grey')

    def on_click_task(event):
        if tasks_entry.get() == "task 0AM-0PM":
            tasks_entry.delete(0, "end")
            tasks_entry.config(fg='black')

    def on_focusout_task(event):
        if tasks_entry.get() == "":
            tasks_entry.insert(0, "task 0AM-0PM")
            tasks_entry.config(fg='grey')

    tasks_entry.bind("<FocusIn>", on_click_task)
    tasks_entry.bind("<FocusOut>", on_focusout_task)

    # Dictionary to store the entered times
    global times
    if 'times' not in globals():
        times = {}

    # Dictionary to store the rectangles for each hour
    global hour_rectangles
    if 'hour_rectangles' not in globals():
        hour_rectangles = {}


    def save_times():
        wake_sleep_times = time_entry.get()
        if ' ' in wake_sleep_times:
            wake_time, sleep_time = map(int, wake_sleep_times.split(' '))
            formatted_time = f"{wake_time}AM-{sleep_time}PM"
            times[day] = formatted_time
            canvas.create_text(x + (560 // 14), 420, text=formatted_time, font=("Helvetica", 12),
                               anchor=NW)  # Adjusted y coordinate to 420 and anchor to NW
            print(wake_time + sleep_time)


    def combined_action():
        # Execute both commands
        save_times()


    # Create a single button with the combined action
    combined_button = Button(root, text="Save", command=combined_action)
    combined_button.pack(pady=15)  # Adjust padding as needed

    back_button = Button(root, text="Back", command=lambda: create_calendar(None))
    back_button.pack(pady=10)


# Bind the click event to the function
root.bind("u", create_calendar)

root.mainloop()


