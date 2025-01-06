import os
import shutil
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Step 1: Clear Temporary Files
def clear_temp_files():
    temp_dir = os.environ.get("TEMP")
    try:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except PermissionError:
                    pass
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    shutil.rmtree(dir_path)
                except PermissionError:
                    pass
        messagebox.showinfo("Success", "Temporary files cleared successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error clearing temp files: {e}")

# Step 2: Find a File in File Explorer
def find_file_in_explorer():
    filename = simpledialog.askstring("Find File", "Enter the file name to search:")
    if not filename:
        return
    user_dir = os.path.expanduser("~")
    found_files = []
    for root, dirs, files in os.walk(user_dir):
        if filename in files:
            found_files.append(os.path.join(root, filename))
    if found_files:
        messagebox.showinfo("File Found", f"File(s) found:\n{found_files[0]}")
        subprocess.run(["explorer", "/select,", found_files[0]])
    else:
        messagebox.showwarning("Not Found", "File not found.")

# Step 3: Clean Downloads Folder
def clean_downloads_folder():
    days = simpledialog.askinteger("Clean Downloads", "Enter the number of days to keep files:")
    if not days:
        return
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    cutoff_date = datetime.now().timestamp() - (days * 86400)
    try:
        for root, dirs, files in os.walk(downloads_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_creation_time = os.path.getctime(file_path)
                if file_creation_time < cutoff_date:
                    try:
                        os.remove(file_path)
                    except PermissionError:
                        pass
        messagebox.showinfo("Success", "Downloads folder cleaned successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error cleaning Downloads folder: {e}")

# Step 4: Show Disk Usage
def check_disk_usage():
    drive = simpledialog.askstring("Disk Usage", "Enter the drive letter (e.g., C:):")
    if not drive:
        return
    try:
        total, used, free = shutil.disk_usage(drive)
        messagebox.showinfo(
            "Disk Usage",
            f"Disk Usage for {drive}:\nTotal: {total // (1024 ** 3)} GB\nUsed: {used // (1024 ** 3)} GB\nFree: {free // (1024 ** 3)} GB"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Error checking disk usage: {e}")

# Create the GUI
def main():
    app = tk.Tk()
    app.title("Windows Task Automator")
    app.geometry("400x300")

    # Buttons for tasks
    tk.Button(app, text="Clear Temporary Files", command=clear_temp_files, width=30).pack(pady=10)
    tk.Button(app, text="Find a File in File Explorer", command=find_file_in_explorer, width=30).pack(pady=10)
    tk.Button(app, text="Clean Downloads Folder", command=clean_downloads_folder, width=30).pack(pady=10)
    tk.Button(app, text="Check Disk Usage", command=check_disk_usage, width=30).pack(pady=10)

    # Run the app
    app.mainloop()

if __name__ == "__main__":
    main()



