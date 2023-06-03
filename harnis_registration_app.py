import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import threading
import subprocess

import netifaces
import os


def get_local_ip_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for address in addresses[netifaces.AF_INET]:
                ip_address = address["addr"]
                if ip_address != "127.0.0.1":
                    return ip_address

    return None  # Return None if unable to retrieve the IP address


flask_process = None  
attendance_list = None

def blast_qr_code():
    def browse_file():
        global attendance_list
        attendance_list = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        if attendance_list:
            messagebox.showinfo("File Selected", f"Selected File: {attendance_list}")

    def send_emails():
        subject = subject_entry.get()
        if not subject:
            messagebox.showwarning(
                "Missing Subject", "Please enter a subject for the emails."
            )
            return

        ip_address = get_local_ip_address()
        if ip_address is None:
            messagebox.showinfo(
                "IP Address Error",
                "Cannot Retreive IP Address",
            )
            return
        if os.getenv("APP_EMAIL") is None or os.getenv("APP_PASSWORD") is None:
            messagebox.showinfo(
                "Missing Email and Password",
                f"Please enter Email and Password in Environment Variable",
            )
            return
        # Call the send_email() function here with the required parameters
        if attendance_list:
            messagebox.showinfo(
                "Sending Emails",
                f"Sending emails with subject: {subject} and IP Address: {ip_address}",
            )
            subprocess.run([
                "python", "qr_generator.py", 
                "--ip", ip_address, 
                "--subject", subject,
                "--excel_path", attendance_list
            ])

            messagebox.showinfo(
                "Success",
                "Emails sent successfully",
            )
        else:
            messagebox.showinfo("Error", f"Input Attendance List first")
            return

            # Hide the main window
    root.withdraw()


   # Create the Blast QR Code page
    blast_qr_code_page = tk.Toplevel()
    blast_qr_code_page.title("Blast QR Code")
    blast_qr_code_page.geometry("400x200")

    browse_button = tk.Button(blast_qr_code_page, text="Browse Excel File", command=browse_file)
    browse_button.pack(pady=10)

    subject_label = tk.Label(blast_qr_code_page, text="Email Subject:")
    subject_label.pack()

    subject_entry = tk.Entry(blast_qr_code_page)
    subject_entry.pack(pady=5)
    subject_entry.focus()  # Set focus to the subject_entry widget

    send_button = tk.Button(blast_qr_code_page, text="Send Emails", command=send_emails)
    send_button.pack(pady=10)

    def close_blast_qr_code():
        # Show the main window and destroy the Blast QR Code page
        root.deiconify()
        blast_qr_code_page.destroy()

    blast_qr_code_page.protocol("WM_DELETE_WINDOW", close_blast_qr_code)


def run_scanner_app():
    def run_flask_app():
        global flask_process  # Declare the variable as global
        flask_process = subprocess.Popen(["flask", "run", "--host=0.0.0.0"])

    def stop_flask_app():
        flask_process.terminate()
        messagebox.showinfo("Stop Scanner", "Scanner app stopped.")

    messagebox.showinfo("Run Scanner App", "Running the Scanner app in the background.")
    run_button.config(text="Stop Scanner", command=stop_flask_app)

    # Start a new thread to run the Flask app
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()


if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("Harnis Attendance List App")
    root.geometry("400x200")

    blast_button = tk.Button(root, text="Blast QR Code", command=blast_qr_code)
    blast_button.pack(pady=10)

    run_button = tk.Button(root, text="Run Scanner", command=run_scanner_app)
    run_button.pack(pady=10)

    # Start the main event loop
    root.mainloop()
