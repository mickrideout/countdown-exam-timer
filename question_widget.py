# The question widget
import tkinter
import time
from tkinter import messagebox
from tkinter import W, E
from tkinter import ttk

from countdown_exam_timer import CountdownExamTimer
from countdown_exam_timer import seconds_to_display_string

class QuestionWidget:
    def __init__(self, countdown_exam_timer : CountdownExamTimer, points : int, row: int):
        self.countdown_exam_timer = countdown_exam_timer
        self.points = points
        self.row = row
        self.elapsed_time = 0
        self.is_timer_running = False

    def update(self):
        if self.is_timer_running:
            self.elapsed_time += 1
            self.elapsed_time_label.config(text=f"Elapsed Time: {seconds_to_display_string(self.elapsed_time)}")
            self.progress_bar.config(value=(self.elapsed_time / self.allowed_time) * 100)


    def start_timer(self):
        self.countdown_exam_timer.stop_all_question_timers()
        self.is_timer_running = True
        if self.countdown_exam_timer.is_timer_running == False:
            self.countdown_exam_timer.is_timer_running = True
            self.countdown_exam_timer.master.after(1000, self.countdown_exam_timer.update)

    def stop_timer(self):
        self.is_timer_running = False

    def generate_widget(self):
        right_frame = self.countdown_exam_timer.right_frame

        self.frame = tkinter.Frame(right_frame, bg="lightgrey")
        self.frame.grid(row=self.row, column=0, columnspan=6, padx=2, pady=2, sticky="nsew")
        self.question_label = tkinter.Label(self.frame, text=f"Q: {self.row}")
        self.question_label.grid(row=self.row, column=0, padx=2, pady=2, sticky="nsew")
        self.points_entry = tkinter.Entry(self.frame, width=3)
        self.points_entry.insert(0, self.points)
        self.points_entry.grid(row=self.row, column=1, padx=2, pady=2, sticky="nsew")
        self.points_entry.bind('<Key>', lambda e: self.update_on_key(e))
        self.points_label = tkinter.Label(self.frame, text=" Points")
        self.points_label.grid(row=self.row, column=2, padx=2, pady=2, sticky="nsew")
        self.start_button = tkinter.Button(self.frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=self.row, column=3, padx=2, pady=2, sticky="nsew")
        self.done_button = tkinter.Button(self.frame, text="Done", command=self.stop_timer)
        self.done_button.grid(row=self.row, column=4, padx=2, pady=2, sticky="nsew")
        self.progress_bar = ttk.Progressbar(self.frame, orient='horizontal', maximum=100, length=200, mode='determinate')
        self.progress_bar.grid(row=self.row, column=5, padx=2, pady=2, sticky="nsew")# Convert minutes to seconds
        self.elapsed_time_label = tkinter.Label(self.frame, text=f"Elapsed Time: {seconds_to_display_string(self.elapsed_time)}")
        self.elapsed_time_label.grid(row=self.row, column=6, padx=2, pady=2, sticky="nsew")
        self.allowed_time = self.points / self.countdown_exam_timer.total_points * self.countdown_exam_timer.exam_duration
        self.allowed_time_label = tkinter.Label(self.frame, text=f"Allowed Time: {seconds_to_display_string(self.allowed_time)}")
        self.allowed_time_label.grid(row=self.row, column=7, padx=2, pady=2, sticky="nsew")



    def update_allowed_time(self):
        self.allowed_time = self.points / self.countdown_exam_timer.total_points * self.countdown_exam_timer.exam_duration
        self.allowed_time_label.config(text=f"Allowed Time: {seconds_to_display_string(self.allowed_time)}")


    def update_total_points(self, event):
        try:
            new_points = int(self.points_entry.get())
            old_points = self.points
            self.points = new_points
            self.countdown_exam_timer.total_points += (new_points - old_points)
            self.countdown_exam_timer.total_points_label.config(text=f"Total Points: {self.countdown_exam_timer.total_points}")
            # update time per point
            self.countdown_exam_timer.time_per_point = self.countdown_exam_timer.exam_duration / self.countdown_exam_timer.total_points # self.time_per_point)
            self.countdown_exam_timer.time_per_point_label.config(text=f"Time per Point: {seconds_to_display_string(self.countdown_exam_timer.time_per_point)}")
            self.countdown_exam_timer.update_all_question_allowed_time()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for points.")

    def update_on_key(self, event):
        if event.keysym == 'BackSpace':
            # ignore this
            return  
        if event.char.isdigit():
            # Schedule the update after a short delay to allow the Entry widget to update its content
            self.frame.after(10, self.update_total_points, event)

       
    