# Simple Backup Tool

## Description

This is a simple multi-platform GUI backup tool written in Python. It uses `rsync` on Unix-based systems and `robocopy` on Windows to perform the backups. 

lease note, this tool simply **copies** files from the source directories to the destination directory, maintaining the original directory structure. It **does not** perform any alterations on the files such as compression or encryption, nor does it remove files from the source directories. It is strictly a tool for creating a duplicate copy of your files.

The application allows you to select multiple source directories and a single destination directory for the backup. It also lets you specify directories to exclude from the backup. 

## Prerequisites

* Python 3.8 or later.
* `tkinter` library for Python. Usually comes pre-installed with Python, but if not, it can be added via `apt-get install python3-tk` on Ubuntu or `sudo pacman -S tk` on Arch Linux.
* `rsync` installed and in your PATH if you're using a Unix-based system.
* `robocopy` available if you're using Windows (comes pre-installed on Windows Vista and later).

## Usage

1. Clone the repository: `git clone https://codeberg.org/betazetadev/simple-backup-tool.git`
2. Navigate to the cloned project: `cd simple-backup-tool`
3. Run the script: `python main.py`
4. Click on "Select Source Directories" to select one or more directories you want to backup.
5. Click on "Select Destination Directory" to select the directory where you want the backup to be stored.
6. Specify directories to exclude from the backup in the "Exclude Directories (comma separated)" field. The default directories are: ".git,.idea,node_modules,public,build,.dart_tool"
7. Click on "Start Backup" to begin the backup process. The progress will be displayed in the application.

## License

This project is licensed under the terms of the MIT license.