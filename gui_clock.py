import tkinter as tk
from tkinter import filedialog, Label
import time
import threading


class ClockGUI:
    clock_label: tk.Label
    timer_label: tk.Label
    timer_file_label: tk.Label
    countdown_minutes_entry: tk.Entry
    countdown_seconds_entry: tk.Entry
    countdown_button: tk.Button
    timer_file_entry: tk.Entry
    timer_button: tk.Button

    def __init__(self, head):
        self.timer_end_time = None
        self.timer_duration = None
        self.timer_start_time = None
        self.head = head
        head.title("Clock")

        # Clock display
        self.clock_label = tk.Label(head, font=("Cambria", 50))
        self.clock_label.pack()

        # Timer display
        self.timer_label = tk.Label(head, text="Timer: 00:00:00", font=("Times New Roman", 20))
        self.timer_label.pack()

        # Countdown display
        self.countdown_minutes_label = tk.Label(head, text="Minutes:", font=("Times New Roman", 15))
        self.countdown_minutes_label.pack()
        self.countdown_minutes_entry = tk.Entry(head, font=("Times New Roman", 15))
        self.countdown_minutes_entry.pack()
        self.countdown_seconds_label = tk.Label(head, text="Seconds:", font=("Times New Roman", 15))
        self.countdown_seconds_label.pack()
        self.countdown_seconds_entry = tk.Entry(head, font=("Times New Roman", 15))
        self.countdown_seconds_entry.pack()
        self.countdown_button = tk.Button(head, text="Countdown", command=self.start_countdown)
        self.countdown_button.pack()

        # Timer file selection
        self.timer_file_label = tk.Label(head, text="Timer file:", font=("Times New Roman", 15))
        self.timer_file_label.pack()
        self.timer_file_entry = tk.Entry(head, font=("Times New Roman", 15))
        self.timer_file_entry.pack()
        self.timer_file_button = tk.Button(head, text="Select file", command=self.select_timer_file)
        self.timer_file_button.pack()

        # Set background color of root window
        head.config(bg="light grey")
        # Set background color of timer label
        self.timer_label.config(bg="#D8BFD8")  # light purple

        # Timer button
        self.timer_running = False
        self.timer_button = tk.Button(head, text="Start timer", bg="green", fg="white", command=self.toggle_timer)
        self.timer_button.pack()

        # Clock update
        self.update_clock()

    def update_clock(self):
        # Get current time and format it
        current_time = time.strftime("%A\n %d %B %Y\n %H:%M:%S")
        # Update clock display
        self.clock_label.config(text=current_time)
        # Schedule next update
        self.head.after(1000, self.update_clock)

    def toggle_timer(self):
        if not self.timer_running:
            # Start timer
            self.timer_start_time = time.time()
            self.timer_button.config(text="Stop timer", bg="red")
            self.timer_running = True
        else:
            # Stop timer
            self.timer_end_time = time.time()
            self.timer_duration = self.timer_end_time - self.timer_start_time
            self.timer_button.config(text="Start timer", bg="green")
            self.timer_running = False
            self.write_timer_data()

    def write_timer_data(self):
        # Get timer file path
        timer_file_path = self.timer_file_entry.get()
        if not timer_file_path:
            self.timer_label.config(text="Timer file path is not specified!")
            return
        # Write timer data to file
        with open(timer_file_path, "a") as f:
            f.write(
                "Start time: {}\n".format(time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(self.timer_start_time))))
            f.write("End time: {}\n".format(time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(self.timer_end_time))))
            f.write("Duration: {:.2f} seconds\n".format(self.timer_duration))

    def select_timer_file(self):
        # Open file selection dialog
        file_path = filedialog.askopenfilename()
        # Update timer file entry
        self.timer_file_entry.delete(0, tk.END)
        self.timer_file_entry.insert(0, file_path)

    def start_countdown(self):
        # Get the countdown time in seconds
        try:
            countdown_minutes = int(self.countdown_minutes_entry.get())
            countdown_seconds = int(self.countdown_seconds_entry.get())
            countdown_time = countdown_minutes * 60 + countdown_seconds
        except ValueError:
            self.timer_label.config(text="Invalid countdown time!")
            return

        # Start a new thread to run the countdown timer
        self.countdown_thread = threading.Thread(target=self.run_countdown, args=(countdown_time,))
        self.countdown_thread.start()

    def run_countdown(self, countdown_time):
        # Define countdown function
        def countdown(countdown_duration=None):
            for i in range(countdown_duration, 0, -1):
                minutes, seconds = divmod(i, 60)
                countdown_text = f"Countdown: {minutes:02d}:{seconds:02d}"
                self.timer_label.config(text=countdown_text)
                time.sleep(1)

            # Show the end message when the countdown is finished
            self.timer_label.config(text="Countdown ended!")

        # Get the countdown time in seconds
        try:
            countdown_minutes = int(self.countdown_minutes_entry.get())
            countdown_seconds = int(self.countdown_seconds_entry.get())
            countdown_time = countdown_minutes * 60 + countdown_seconds
        except ValueError:
            self.timer_label.config(text="Invalid countdown time!")
            return

        # Start the countdown timer
        countdown_thread = threading.Thread(target=countdown, args=(countdown_time,))
        countdown_thread.start()


root = tk.Tk()
clock_gui = ClockGUI(root)
root.mainloop()