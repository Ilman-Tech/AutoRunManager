import subprocess
import json
import time
from plyer import notification
import psutil
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import os

# Load saved program configurations from a JSON file
def load_programs():
    try:
        with open('program_config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save program configurations to a JSON file
def save_programs(program_list):
    with open('program_config.json', 'w') as file:
        json.dump(program_list, file)

# Main menu to handle user input and actions
def main_menu():
    root = tk.Tk()
    root.withdraw()

    choice = simpledialog.askinteger("Input", "(1) Open program, (2) Add program, (3) Show programs,\n(4) Remove program, (5) Quit.")

    if choice == 1:
        open_programs(program_list)
    elif choice == 2:
        add_program()
    elif choice == 3:
        show_programs()
    elif choice == 4:
        remove_program()
    else:
        exit()

# Check if a program is already running
def is_program_running(program_name):
    for process in psutil.process_iter():
        process_info = process.as_dict(attrs=['pid', 'name'])
        if program_name.lower() in process_info['name'].lower():
            return True
    return False

# Open saved programs with a delay
def open_programs(program_list):
    for program_path, delay in program_list:
        program_name = program_path.split("\\")[-1]
        if not is_program_running(program_name):
            time.sleep(delay)
            subprocess.Popen(program_path)
            notification.notify(
                title="Opening Program",
                message=f"Opening {program_name}",
                timeout=5
            )
        else:
            tk.messagebox.showinfo("Program Running", f"{program_name} is already open")

# Add a new program to the list
def add_program():
    program_path = simpledialog.askstring("Input", "Enter the program's file path:")
    if os.path.isfile(program_path):
        delay = simpledialog.askinteger("Input", "Enter the delay time in seconds:")
        if delay is not None:
            program_list.append([program_path, delay])
            save_programs(program_list)
            tk.messagebox.showinfo("Success",
                                   f"Program {program_path.split('\\')[-1]} added with a delay of {delay} seconds!")
            ask_to_add_another()
    else:
        tk.messagebox.showinfo("Error", "Program not found. Please try again.")
        add_program()

# Prompt user to add another program
def ask_to_add_another():
    choice = simpledialog.askstring("Input", "Do you want to add another program? (yes/no)")

    if choice and choice.lower() == 'yes':
        add_program()
    else:
        main_menu()

# Remove a program from the list
def remove_program():
    if not program_list:
        tk.messagebox.showinfo("Info", "Your program list is empty.")
        return

    program_names = [program_path.split("\\")[-1] for program_path, delay in program_list]

    selected_program = simpledialog.askstring("Available Programs", f"Programs:\n{' '.join(program_names)}\n\n"
                                                               f"Enter the program name to delete:")

    if selected_program:
        for program_path, delay in program_list:
            if selected_program.lower() == program_path.split("\\")[-1].lower():
                program_list.remove([program_path, delay])
                save_programs(program_list)
                tk.messagebox.showinfo("Success", f"{selected_program} was successfully removed.")
                return
        tk.messagebox.showinfo("Error", "Program not found in the list.")
    else:
        tk.messagebox.showinfo("Error", "No program selected!")

# Show the list of saved programs
def show_programs():
    if not program_list:
        tk.messagebox.showinfo("Info", "Your program list is empty!")
        return

    program_names = [program_path.split("\\")[-1] for program_path, delay in program_list]

    next_action = simpledialog.askstring("Info", f"Programs list:\n{', '.join(program_names)}\n\n"
                                           f"(Type 'back' to return to the main menu):")

    if next_action and next_action.lower() == 'back':
        main_menu()
    else:
        exit()

if __name__ == "__main__":
    program_list = load_programs()
    main_menu()
