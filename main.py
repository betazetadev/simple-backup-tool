import os
import subprocess
import platform
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Simple Backup Tool')

        self.src_dirs = []
        self.dst_dir = tk.StringVar()
        self.exclude_dirs = tk.StringVar()
        self.exclude_dirs.set(".git,.idea,node_modules,public,build,.dart_tool")  # Set default value

        self.create_widgets()

    def create_widgets(self):
        src_button = tk.Button(self.root, text="Select Source Directories", command=self.select_src_dirs)
        src_button.pack()

        self.src_text = tk.Text(self.root)
        self.src_text.pack()

        dst_button = tk.Button(self.root, text="Select Destination Directory", command=self.select_dst_dir)
        dst_button.pack()

        self.dst_text = tk.Text(self.root, height=2)
        self.dst_text.pack()

        exclude_label = tk.Label(self.root, text="Exclude Directories (comma separated):")
        exclude_label.pack()
        exclude_entry = tk.Entry(self.root, textvariable=self.exclude_dirs, width=30)
        exclude_entry.pack()

        backup_button = tk.Button(self.root, text="Start Backup", command=self.start_backup_thread)
        backup_button.pack()

        self.progress_text = tk.Text(self.root)
        self.progress_text.pack()

    def select_src_dirs(self):
        while True:
            dir = filedialog.askdirectory()
            if not dir:
                break
            self.src_dirs.append(dir)
            self.src_text.insert(tk.END, dir + '\n')

    def select_dst_dir(self):
        dir = filedialog.askdirectory()
        if dir:
            self.dst_dir.set(dir)
            self.dst_text.insert(tk.END, dir + '\n')

    def start_backup_thread(self):
        threading.Thread(target=self.run_backup, daemon=True).start()

    def run_backup(self):
        dst_dir = self.dst_dir.get()

        is_windows = platform.system() == 'Windows'
        exclude_options = ''

        if is_windows:
            # Generate robocopy exclude options
            exclude_dirs = self.exclude_dirs.get().split(',')
            exclude_options = "/XD " + " ".join(exclude_dirs)
        else:
            # Generate rsync exclude options
            exclude_dirs = self.exclude_dirs.get().split(',')
            exclude_options = ' '.join(f'--exclude={dir.strip()}' for dir in exclude_dirs)

        if is_windows:
            backup_command = ' '.join([f'robocopy {src_dir} {dst_dir}/{os.path.basename(src_dir)} /E {exclude_options}' for src_dir in self.src_dirs])
        else:
            backup_command = ' '.join([f'rsync -avh --progress {exclude_options} {src_dir} {dst_dir}' for src_dir in self.src_dirs])

        try:
            process = subprocess.Popen(backup_command, stdout=subprocess.PIPE, shell=True)

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.progress_text.insert(tk.END, output.decode())
                    self.progress_text.see(tk.END)
                    self.root.update()

            if process.poll() > 0:
                raise subprocess.CalledProcessError(process.poll(), backup_command)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Backup failed with error:\n{str(e)}")

        messagebox.showinfo("Success", "Backup completed successfully!")

root = tk.Tk()
app = BackupApp(root)
root.mainloop()
