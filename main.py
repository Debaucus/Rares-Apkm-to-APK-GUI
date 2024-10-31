import os
import shutil
import zipfile
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, BooleanVar, Checkbutton, scrolledtext

class APKMInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rare's APKM to APK GUI Tool")
        self.root.geometry("1920x1080")  # Set to 1080p resolution
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(True, True)  # Allow resizing

        # Hardcoded output folder
        self.output_folder = "output"

        # Dark theme styles
        self.dark_bg = "#2E2E2E"
        self.dark_fg = "#FFFFFF"
        self.accent_color = "#4E9CAF"
        self.root.tk_setPalette(background=self.dark_bg, foreground=self.dark_fg, activeBackground=self.accent_color)

        # Title Label
        title_label = tk.Label(root, text="Rare's APKM to APK GUI Tool", font=("Helvetica", 18, "bold"), 
                               bg=self.dark_bg, fg=self.accent_color)
        title_label.pack(pady=10)

        # Dynamically get connected devices
        self.device_list = self.get_connected_devices()
        self.selected_devices = []
        self.device_vars = {}

        # Device selection area
        tk.Label(root, text="Select Device(s):", bg=self.dark_bg, fg=self.accent_color).pack(pady=5)
        
        # "Select All" checkbox
        self.select_all_var = BooleanVar(value=False)
        self.select_all_checkbox = Checkbutton(root, text="Select All", variable=self.select_all_var, 
                                               command=self.toggle_select_all, bg=self.dark_bg, fg=self.dark_fg,
                                               activeforeground=self.accent_color, selectcolor=self.accent_color)
        self.select_all_checkbox.pack()

        # Device checkboxes
        for device_id in self.device_list:
            var = BooleanVar(value=False)
            checkbox = Checkbutton(root, text=device_id, variable=var, 
                                   command=lambda d=device_id, v=var: self.toggle_device_selection(d, v),
                                   bg=self.dark_bg, fg=self.dark_fg, activeforeground=self.accent_color, 
                                   selectcolor=self.accent_color)
            checkbox.pack()
            self.device_vars[device_id] = var

        # Checkbox for saving APK to output folder
        self.save_apk_var = BooleanVar(value=False)
        self.save_apk_checkbox = Checkbutton(root, text="Save APK to Output Folder", variable=self.save_apk_var,
                                             bg=self.dark_bg, fg=self.dark_fg, activeforeground=self.accent_color, 
                                             selectcolor=self.accent_color)
        self.save_apk_checkbox.pack(pady=5)

        # Button to load multiple .apkm or .apk files
        self.load_button = tk.Button(root, text="Load APKM or APK Files", command=self.load_apkm_or_apk,
                                     bg=self.accent_color, fg=self.dark_fg, activebackground=self.dark_bg)
        self.load_button.pack(pady=10)

        # Label to display chosen files
        self.file_label = tk.Label(root, text="No files selected", bg=self.dark_bg, fg=self.dark_fg)
        self.file_label.pack(pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
        self.progress.pack(pady=10)

        # Scrolled text for verbose log output with dark theme, resizable
        self.log_output = scrolledtext.ScrolledText(root, width=100, height=25, state='disabled', bg="#1E1E1E", fg="#FFFFFF")
        self.log_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Make the log area resizable
        self.log_output.pack_propagate(False)  # Prevent resizing based on content

        # Button to install APKs
        self.install_button = tk.Button(root, text="Install APKs", command=self.run_install_thread, state=tk.DISABLED,
                                        bg=self.accent_color, fg=self.dark_fg, activebackground=self.dark_bg)
        self.install_button.pack(pady=10)

        # Store list of selected files and extracted folder path
        self.apkm_or_apk_files = []
        self.apk_folder = None

    def get_connected_devices(self):
        """Retrieve the list of currently connected ADB devices."""
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        device_list = []
        for line in result.stdout.splitlines():
            if "\tdevice" in line:
                device_id = line.split("\t")[0]
                device_list.append(device_id)
        return device_list

    def toggle_device_selection(self, device_id, var):
        if var.get():
            self.selected_devices.append(device_id)
        else:
            self.selected_devices.remove(device_id)
        
        # Update "Select All" checkbox state based on individual selections
        all_selected = all(v.get() for v in self.device_vars.values())
        self.select_all_var.set(all_selected)

    def toggle_select_all(self):
        """Select or deselect all devices based on the Select All checkbox."""
        select_all = self.select_all_var.get()
        for device_id, var in self.device_vars.items():
            var.set(select_all)
            if select_all:
                if device_id not in self.selected_devices:
                    self.selected_devices.append(device_id)
            else:
                if device_id in self.selected_devices:
                    self.selected_devices.remove(device_id)

    def load_apkm_or_apk(self):
        # Select multiple .apkm or .apk files
        file_paths = filedialog.askopenfilenames(filetypes=[("APKM/APK files", "*.apkm *.apk")])
        if file_paths:
            self.apkm_or_apk_files = file_paths
            filenames = ", ".join(os.path.basename(f) for f in file_paths)
            self.file_label.config(text=f"Loaded: {filenames}")
            # Enable Install button
            self.install_button.config(state=tk.NORMAL)

    def extract_apkm(self, file_path):
        """Extract a single .apkm file to the hard-coded output folder and return list of APK paths."""
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_folder = os.path.join(self.output_folder, base_name)
        os.makedirs(output_folder, exist_ok=True)

        zip_path = file_path.replace('.apkm', '.zip')
        shutil.move(file_path, zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)

        shutil.move(zip_path, file_path)

        apk_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.apk')]
        if not apk_files:
            self.log(f"Error: Failed to extract APK files from {os.path.basename(file_path)}")
            return None
        else:
            self.log(f"Extraction complete for {os.path.basename(file_path)}")
            return apk_files  # Return list of extracted APK files

    def log(self, message):
        """Log message to the scrolled text output."""
        self.log_output.config(state='normal')
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.see(tk.END)
        self.log_output.config(state='disabled')

    def run_install_thread(self):
        """Run the installation in a separate thread to avoid freezing the GUI."""
        threading.Thread(target=self.install_apks).start()

    def install_apks(self):
        # Update progress for the number of files
        self.progress["value"] = 0
        self.progress["maximum"] = len(self.apkm_or_apk_files) * len(self.selected_devices)

        for file_path in self.apkm_or_apk_files:
            # Determine if the current file is an APKM or single APK
            if file_path.endswith(".apk"):
                apk_files = [file_path]
                self.log(f"Preparing to install single APK: {os.path.basename(file_path)}")
            else:
                apk_files = self.extract_apkm(file_path)
                if not apk_files:
                    continue

            # Save only if the option is selected
            if not self.selected_devices and self.save_apk_var.get():
                self.log(f"Saved APK(s) for {os.path.basename(file_path)} to output folder, skipping installation.")
                continue

            # Try normal installation, and if it fails, retry with -r for replacement
            for device in self.selected_devices:
                adb_command = ["adb", "-s", device, "install-multiple"] + apk_files
                self.log(f"Starting installation of {os.path.basename(file_path)} on {device}.")
                result = subprocess.run(adb_command, capture_output=True, text=True)
                
                if result.returncode != 0:
                    # Log the error, then retry with replacement
                    self.log(f"Normal install failed on {device} for {os.path.basename(file_path)}. Retrying with replacement...")
                    adb_command = ["adb", "-s", device, "install-multiple", "-r"] + apk_files
                    result = subprocess.run(adb_command, capture_output=True, text=True)
                    
                if result.returncode == 0:
                    self.log(f"Success: {os.path.basename(file_path)} installed on {device}.")
                else:
                    self.log(f"Failed: Could not install {os.path.basename(file_path)} on {device}. Error: {result.stderr}")

                # Update progress bar for each device
                self.progress["value"] += 1
                self.root.update_idletasks()

            # Clean up extracted APKs if Save APK is not selected
            if not self.save_apk_var.get() and self.apk_folder:
                shutil.rmtree(self.apk_folder)
                self.log(f"Cleaned up extracted APK files for {os.path.basename(file_path)}")

        messagebox.showinfo("Installation Complete", "All installations are finished.")

# Main execution
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = APKMInstallerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
