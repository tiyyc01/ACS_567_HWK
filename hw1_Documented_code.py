#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: chinmaietiyyagura
"""

import pandas as pd
from datetime import datetime
import statistics

class ExerciseData:
    """
    Class to encapsulate exercise data.

    Attributes:
        exercise (str): Name of the exercise.
        duration (int): Duration of the exercise in minutes.
        calories_burned (int): Calories burned during the exercise.
        date (datetime): Date when the exercise was performed.
    """

    def __init__(self, exercise, duration, calories_burned, date):
        """
        Initialize ExerciseData object.

        Args:
            exercise (str): Name of the exercise.
            duration (int): Duration of the exercise in minutes.
            calories_burned (int): Calories burned during the exercise.
            date (datetime): Date when the exercise was performed.
        """
        self.exercise = exercise
        self.duration = duration
        self.calories_burned = calories_burned
        self.date = date

class ExerciseManager:
    """
    Singleton class to manage exercise data.

    Attributes:
        _instance (ExerciseManager): Singleton instance of ExerciseManager.
        csv_file (str): Path to the CSV file storing exercise data.
        columns (list): List of column names for the exercise DataFrame.
    """

    _instance = None
    csv_file = "exercise_data.csv"
    columns = ["Exercise", "Duration", "Calories_Burned", "Date"]

    def __new__(cls):
        """
        Implement the singleton pattern.

        Returns:
            ExerciseManager: The singleton instance of ExerciseManager.
        """
        if not cls._instance:
            cls._instance = super(ExerciseManager, cls).__new__(cls)
            cls._instance.exercise_df = cls._instance.load_data()
        return cls._instance

    def load_data(self):
        """
        Load exercise data from the CSV file.

        Returns:
            pandas.DataFrame: Loaded exercise data.
        """
        try:
            exercise_df = pd.read_csv(self.csv_file, parse_dates=['Date'])
        except FileNotFoundError:
            # File doesn't exist, create an empty DataFrame
            exercise_df = pd.DataFrame(columns=self.columns)
        return exercise_df

    def save_data(self):
        """
        Save exercise data to the CSV file.
        """
        self.exercise_df.to_csv(self.csv_file, index=False)

    def get_all_data(self):
        """
        Retrieve all exercise data.

        Returns:
            pandas.DataFrame: All exercise data.
        """
        return self.exercise_df

    def add_data(self, exercise, duration, calories_burned, date):
        """
        Add new exercise data.

        Args:
            exercise (str): Name of the exercise.
            duration (int): Duration of the exercise in minutes.
            calories_burned (int): Calories burned during the exercise.
            date (datetime): Date when the exercise was performed.
        """
        new_row = pd.DataFrame([[exercise, duration, calories_burned, date]], columns=self.columns)
        self.exercise_df = pd.concat([self.exercise_df, new_row], ignore_index=True)
        self.save_data()

    def edit_data(self, index, exercise, duration, calories_burned, date):
        """
        Edit existing exercise data.

        Args:
            index (int): Index of the data to edit.
            exercise (str): New name of the exercise.
            duration (int): New duration of the exercise in minutes.
            calories_burned (int): New calories burned during the exercise.
            date (datetime): New date when the exercise was performed.
        """
        self.exercise_df.at[index, "Exercise"] = exercise
        self.exercise_df.at[index, "Duration"] = duration
        self.exercise_df.at[index, "Calories_Burned"] = calories_burned
        self.exercise_df.at[index, "Date"] = date
        self.save_data()

    def delete_data(self, index):
        """
        Delete existing exercise data.

        Args:
            index (int): Index of the data to delete.
        """
        self.exercise_df = self.exercise_df.drop(index)
        self.save_data()

class ExerciseApp:
    """
    Class to drive the exercise application.

    Attributes:
        exercise_manager (ExerciseManager): Instance of ExerciseManager.
    """

    def __init__(self):
        """
        Initialize ExerciseApp object.
        """
        self.exercise_manager = ExerciseManager()

    def display_menu(self):
        """
        Display the menu for the console application.
        """
        print("\n1. Read data")
        print("2. Add data")
        print("3. Edit data")
        print("4. Delete data")
        print("5. Analyze data (mean and median)")
        print("6. Filter data")
        print("7. Exit")

    def run(self):
        """
        Run the console application.
        """
        while True:
            self.display_menu()
            choice = int(input("Enter your choice: "))

            if choice == 1:
                # Read data
                print(self.exercise_manager.get_all_data())
            elif choice == 2:
                # Add data
                exercise = input("Enter exercise name: ")
                duration = int(input("Enter duration in minutes: "))
                calories_burned = int(input("Enter calories burned: "))
                date_str = input("Enter date (MM/DD/YY): ")
                date = datetime.strptime(date_str, "%m/%d/%y")
                self.exercise_manager.add_data(exercise, duration, calories_burned, date)
                print("Exercise added successfully.")
            elif choice == 3:
                # Edit data
                index = int(input("Enter index to edit: "))
                exercise = input("Enter new exercise name: ")
                duration = int(input("Enter new duration in minutes: "))
                calories_burned = int(input("Enter new calories burned: "))
                date_str = input("Enter new date (MM/DD/YY): ")
                date = datetime.strptime(date_str, "%m/%d/%y")
                self.exercise_manager.edit_data(index, exercise, duration, calories_burned, date)
                print("Exercise edited successfully.")
            elif choice == 4:
                # Delete data
                index = int(input("Enter index to delete: "))
                self.exercise_manager.delete_data(index)
                print("Exercise deleted successfully.")
            elif choice == 5:
                # Analyze data (mean and median)
                if not self.exercise_manager.get_all_data().empty:
                    mean_duration = statistics.mean(self.exercise_manager.get_all_data()["Duration"])
                    median_duration = statistics.median(self.exercise_manager.get_all_data()["Duration"])
                    print(f"Mean Duration: {mean_duration} mins")
                    print(f"Median Duration: {median_duration} mins")
                else:
                    print("No data available for analysis.")
            elif choice == 6:
                # Filter data
                filter_option = int(input("Filter by:\n1. Exercise\n2. Date\nEnter your choice: "))
                if filter_option == 1:
                    exercise_name = input("Enter exercise name to filter: ")
                    filtered_data = self.exercise_manager.get_all_data()[self.exercise_manager.get_all_data()["Exercise"] == exercise_name]
                elif filter_option == 2:
                    date_str = input("Enter date to filter (MM/DD/YY): ")
                    date = datetime.strptime(date_str, "%m/%d/%y")
                    filtered_data = self.exercise_manager.get_all_data()[self.exercise_manager.get_all_data()["Date"] == date]
                print(filtered_data)
            elif choice == 7:
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = ExerciseApp()
    app.run()
