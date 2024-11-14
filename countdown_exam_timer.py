# A countdown exam timer. Allocates time based on points per question
import tkinter
from tkinter import ttk
import time
from tkinter import messagebox
from tkinter import W, E

class CountdownExamTimer:
    def __init__(self, master):
        self.master = master
        self.total_points = 0
        self.number_of_questions = 0
        self.time_per_point = 0
        self.exam_duration = 0
        self.elapsed_time = 0
        self.question_widgets = []# Changed to DoubleVar for more precise values
        self.is_timer_running = False
        self.master.title("Countdown Exam Timer")
        self.master.geometry("900x500")


        # Top frame
        self.top_frame = tkinter.Frame(self.master, bg="lightblue")
        self.top_frame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")  # Increased pady and added 'ns' to sticky
        self.total_points_label = tkinter.Label(self.top_frame, text=f"Total Points: {self.total_points}")
        self.total_points_label.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.time_per_point_label = tkinter.Label(self.top_frame, text=f"Time per Point: {seconds_to_display_string(self.time_per_point)}")
        self.time_per_point_label.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.elapsed_time_label = tkinter.Label(self.top_frame, text=f"Elapsed Time: {seconds_to_display_string(self.elapsed_time)}")
        self.elapsed_time_label.grid(row=0, column=2, padx=2, pady=2, sticky="nsew")
        # Elapsed time progress bar
        self.progress_bar = ttk.Progressbar(self.top_frame, orient='horizontal', maximum=100, length=200, mode='determinate')
        self.progress_bar.grid(row=1, column=2, padx=2, pady=2, sticky="nsew")# Convert minutes to seconds

        # Left frame
        self.left_frame = tkinter.Frame(self.master, bg="lightgreen")
        self.left_frame.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        # Exam Duration
        self.exam_duration_label = tkinter.Label(self.left_frame, text="Exam Duration (mins):")
        self.exam_duration_label.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.exam_duration_entry = tkinter.Entry(self.left_frame, width=3)
        self.exam_duration_entry.insert(0, "0")
        self.exam_duration_entry.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        # Number of questions
        self.number_of_questions_label = tkinter.Label(self.left_frame, text="Number of Questions:")
        self.number_of_questions_label.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.number_of_questions_entry = tkinter.Entry(self.left_frame, width=3)
        self.number_of_questions_entry.insert(0, "0")
        self.number_of_questions_entry.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        # Default points per question
        self.points_per_question_label = tkinter.Label(self.left_frame, text="Default Points per Question:")
        self.points_per_question_label.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        self.points_per_question_entry = tkinter.Entry(self.left_frame, width=3)
        self.points_per_question_entry.insert(0, "1")
        self.points_per_question_entry.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")
        # Generate Questions Button
        self.generate_questions_button = tkinter.Button(self.left_frame, text="Generate Questions", command=self.generate_questions)
        self.generate_questions_button.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")


        # Right frame
        self.right_frame = tkinter.Frame(self.master, bg="lightpink")
        self.right_frame.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")


        # Configure grid weights to make frames expandable
        self.master.grid_rowconfigure(0, weight=1)  # Added weight to row 0 (top frame)
        self.master.grid_rowconfigure(1, weight=3)  # Increased weight for row 1 (left and right frames)
        self.master.grid_columnconfigure(0, weight=0)  # Left frame weight
        self.master.grid_columnconfigure(1, weight=2)  # Right frame weight (twice the left frame)

    def generate_questions(self):
        self.question_widgets = []
        # Remove all widgets from right frame
        for widget in self.right_frame.winfo_children():
            widget.grid_forget()

        # Get the values from the left frame
        self.exam_duration = int(self.exam_duration_entry.get()) * 60
        self.number_of_questions = int(self.number_of_questions_entry.get())
        self.default_points_per_question = int(self.points_per_question_entry.get())
        self.total_points = self.number_of_questions * self.default_points_per_question
        self.total_points_label.config(text=f"Total Points: {self.total_points}")

        # Generate the questions
        from question_widget import QuestionWidget
        for i in range(1,self.number_of_questions + 1):
            question = QuestionWidget(self, self.default_points_per_question, i)
            question.generate_widget()
            self.question_widgets.append(question)

        self.time_per_point = self.exam_duration / self.total_points
        self.time_per_point_label.config(text=f"Time per Point: {seconds_to_display_string(self.time_per_point)}")
        
        # Reset elapsed time and progress bar
        self.elapsed_time = 0
        self.elapsed_time_label.config(text=f"Elapsed Time: {seconds_to_display_string(self.elapsed_time)}")

    
    def update_all_question_allowed_time(self):
        for question_widget in self.question_widgets:
            question_widget.update_allowed_time()

    def update(self):
        if self.is_timer_running:
            self.elapsed_time += 1
            self.elapsed_time_label.config(text=f"Elapsed Time: {seconds_to_display_string(self.elapsed_time)}")
            
            # Update progress bar
            progress = (self.elapsed_time / self.exam_duration) * 100
            self.progress_bar.config(value=progress)
            
            # Update questions
            for question_widget in self.question_widgets:
                question_widget.update()
            
            # Check if exam time is up
            if self.elapsed_time >= self.exam_duration * 60:
                self.stop_all_question_timers()
                self.is_timer_running = False
                messagebox.showinfo("Exam Finished", "Time's up! The exam has ended.")
            else:
                self.master.after(1000, self.update)

    def stop_all_question_timers(self):
        for question_widget in self.question_widgets:
            question_widget.stop_timer()


def seconds_to_display_string(seconds, minute_precision=2):
    if seconds <= 0:
        return "00:00"
    minutes = int(seconds // 60)  # Convert to int
    seconds = int(seconds % 60)   # Convert to int
    return f"{minutes:{minute_precision}d}:{seconds:02d}"

if __name__ == "__main__":
    root = tkinter.Tk()
    timer = CountdownExamTimer(root)
    root.mainloop()
