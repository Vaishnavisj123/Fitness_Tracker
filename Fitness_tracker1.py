import tkinter as tk
from tkinter import messagebox
import os
import json

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []
        self.load_data()

    def add_workout(self, workout):
        self.workouts.append(workout)
        self.save_data()

    def get_workouts(self):
        return [str(workout) for workout in self.workouts]

    def save_data(self, filename="workouts.json"):
        with open(filename, 'w') as file:
            json.dump([vars(workout) for workout in self.workouts], file)

    def load_data(self, filename="workouts.json"):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                self.workouts = [Workout(**item) for item in data]

class WorkoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Tracker")
        self.root.geometry("800x500")  # Enlarged window
        self.root.configure(bg="#DFF6FF")
        self.user = None
        
        tk.Label(root, text="Enter Name:", bg="#DFF6FF").grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Enter Age:", bg="#DFF6FF").grid(row=1, column=0)
        self.age_entry = tk.Entry(root)
        self.age_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Enter Weight (kg):", bg="#DFF6FF").grid(row=2, column=0)
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=2, column=1)
        
        self.create_user_btn = tk.Button(root, text="Create Profile", command=self.create_user, bg="#A0C4FF")
        self.create_user_btn.grid(row=3, column=0, columnspan=2)
        
        self.workout_listbox = tk.Listbox(root, width=60, height=10, bg="#FFD6A5")
        self.workout_listbox.grid(row=4, column=0, columnspan=2)
        self.workout_listbox.bind("<Double-Button-1>", self.edit_workout)
        
        self.add_workout_btn = tk.Button(root, text="Add Workout", command=self.add_workout, state=tk.DISABLED, bg="#FFADAD")
        self.add_workout_btn.grid(row=5, column=0)
        
        self.save_btn = tk.Button(root, text="Save Workouts", command=self.save_workouts, state=tk.DISABLED, bg="#FFC6FF")
        self.save_btn.grid(row=5, column=1)
    
    def create_user(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        weight = self.weight_entry.get()
        if name and age.isdigit() and weight.replace('.', '', 1).isdigit():
            self.user = User(name, int(age), float(weight))
            self.add_workout_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)
            self.load_workouts()
            messagebox.showinfo("Success", "User profile created!")
        else:
            messagebox.showerror("Error", "Invalid input. Please enter valid details.")
    
    def add_workout(self, workout=None, index=None):
        if not self.user:
            return
        
        workout_window = tk.Toplevel(self.root)
        workout_window.title("Add/Edit Workout")
        
        tk.Label(workout_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        date_entry = tk.Entry(workout_window)
        date_entry.grid(row=0, column=1)
        
        tk.Label(workout_window, text="Exercise Type:").grid(row=1, column=0)
        exercise_entry = tk.Entry(workout_window)
        exercise_entry.grid(row=1, column=1)
        
        tk.Label(workout_window, text="Duration (minutes):").grid(row=2, column=0)
        duration_entry = tk.Entry(workout_window)
        duration_entry.grid(row=2, column=1)
        
        tk.Label(workout_window, text="Calories Burned:").grid(row=3, column=0)
        calories_entry = tk.Entry(workout_window)
        calories_entry.grid(row=3, column=1)

        # Pre-fill data if editing an existing workout
        if workout:
            date_entry.insert(0, workout.date)
            exercise_entry.insert(0, workout.exercise_type)
            duration_entry.insert(0, str(workout.duration))
            calories_entry.insert(0, str(workout.calories_burned))
        
        def save_workout():
            date = date_entry.get()
            exercise_type = exercise_entry.get()
            duration = duration_entry.get()
            calories_burned = calories_entry.get()
            
            if date and exercise_type and duration.isdigit() and calories_burned.isdigit():
                if workout:  
                    # Editing an existing workout
                    workout.date = date
                    workout.exercise_type = exercise_type
                    workout.duration = int(duration)
                    workout.calories_burned = int(calories_burned)
                    self.user.save_data()  
                    self.load_workouts()
                else:
                    # Adding a new workout
                    new_workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                    self.user.add_workout(new_workout)
                    self.workout_listbox.insert(tk.END, str(new_workout))
                
                workout_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid input. Please enter valid details.")
        
        tk.Button(workout_window, text="Save Workout", command=save_workout).grid(row=4, column=0, columnspan=2)
    
    def load_workouts(self):
        if not self.user:
            return
        self.workout_listbox.delete(0, tk.END)
        for workout in self.user.get_workouts():
            self.workout_listbox.insert(tk.END, workout)

    def edit_workout(self, event):
        selected_index = self.workout_listbox.curselection()
        if not selected_index:
            return
        
        index = selected_index[0]
        workout = self.user.workouts[index]
        self.add_workout(workout, index)

    def save_workouts(self):
        if not self.user:
            messagebox.showerror("Error", "No user profile found. Create a profile first.")
            return
        
        try:
            self.user.save_data()
            messagebox.showinfo("Success", "Workouts saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save workouts: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutApp(root)
    root.mainloop()
