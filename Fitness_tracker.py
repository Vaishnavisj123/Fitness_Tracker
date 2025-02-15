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

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        for workout in self.workouts:
            print(workout)

    def save_data(self, filename):
        with open(filename, 'w') as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                date, exercise_type, duration, calories_burned = line.strip().split(',')
                workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                self.workouts.append(workout)

def add_workout(user):
    date = input("Enter the date (YYYY-MM-DD): ")
    exercise_type = input("Enter the exercise type: ")
    duration = int(input("Enter the duration (minutes): "))
    calories_burned = int(input("Enter the calories burned: "))
    workout = Workout(date, exercise_type, duration, calories_burned)
    user.add_workout(workout)
    print("Workout added successfully!")

def view_workouts(user):
    print(f"{user.name}'s Workouts:")
    user.view_workouts()

def save_data(user):
    filename = input("Enter the filename to save data: ")
    user.save_data(filename)
    print("Data saved successfully!")

def load_data(user):
    filename = input("Enter the filename to load data: ")
    user.load_data(filename)
    print("Data loaded successfully!")
def main():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight: "))
    user = User(name, age, weight)

    while True:
        print("\n1. Add Workout")
        print("2. View Workouts")
        print("3. Save Data")
        print("4. Load Data")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_workout(user)
        elif choice == '2':
            view_workouts(user)
        elif choice == '3':
            save_data(user)
        elif choice == '4':
            load_data(user)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()