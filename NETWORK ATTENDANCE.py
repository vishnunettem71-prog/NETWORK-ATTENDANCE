import tkinter as tk
from tkinter import ttk, messagebox
import socket
import uuid
import subprocess
import re
import csv
import os
from datetime import datetime


class NetworkAttendanceSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Network-Based Attendance System")
        self.root.geometry("1100x700")
        self.root.configure(bg="#101820")

        self.attendance = []

        self.create_ui()

    # ==================================================
    # USER INTERFACE
    # ==================================================

    def create_ui(self):

        # Title
        title = tk.Label(
            self.root,
            text="NETWORK-BASED ATTENDANCE SYSTEM",
            font=("Arial", 25, "bold"),
            fg="#00e5ff",
            bg="#101820"
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            self.root,
            text="Student attendance using local network detection",
            font=("Arial", 12),
            fg="white",
            bg="#101820"
        )
        subtitle.pack()

        # Network information
        info_frame = tk.Frame(
            self.root,
            bg="#18232c"
        )
        info_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        self.hostname_label = tk.Label(
            info_frame,
            text="Computer: Detecting...",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#18232c"
        )
        self.hostname_label.grid(
            row=0,
            column=0,
            padx=30,
            pady=15
        )

        self.ip_label = tk.Label(
            info_frame,
            text="IP Address: Detecting...",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#18232c"
        )
        self.ip_label.grid(
            row=0,
            column=1,
            padx=30,
            pady=15
        )

        self.mac_label = tk.Label(
            info_frame,
            text="MAC Address: Detecting...",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#18232c"
        )
        self.mac_label.grid(
            row=0,
            column=2,
            padx=30,
            pady=15
        )

        self.get_network_info()

        # Student input
        input_frame = tk.LabelFrame(
            self.root,
            text=" Student Attendance ",
            font=("Arial", 14, "bold"),
            fg="#00e5ff",
            bg="#18232c",
            padx=20,
            pady=15
        )
        input_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        tk.Label(
            input_frame,
            text="Student Name:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#18232c"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.name_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=25
        )
        self.name_entry.grid(
            row=0,
            column=1,
            padx=10
        )

        tk.Label(
            input_frame,
            text="Register Number:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#18232c"
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        self.reg_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=20
        )
        self.reg_entry.grid(
            row=0,
            column=3,
            padx=10
        )

        # Buttons
        button_frame = tk.Frame(
            self.root,
            bg="#101820"
        )
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="MARK ATTENDANCE",
            font=("Arial", 12, "bold"),
            bg="#00e5ff",
            fg="black",
            padx=20,
            pady=10,
            command=self.mark_attendance
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        tk.Button(
            button_frame,
            text="SCAN NETWORK",
            font=("Arial", 12, "bold"),
            bg="#00ff88",
            fg="black",
            padx=20,
            pady=10,
            command=self.scan_network
        ).grid(
            row=0,
            column=1,
            padx=10
        )

        tk.Button(
            button_frame,
            text="EXPORT CSV",
            font=("Arial", 12, "bold"),
            bg="#ffaa00",
            fg="black",
            padx=20,
            pady=10,
            command=self.export_csv
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        tk.Button(
            button_frame,
            text="CLEAR",
            font=("Arial", 12, "bold"),
            bg="#ff5555",
            fg="white",
            padx=20,
            pady=10,
            command=self.clear_records
        ).grid(
            row=0,
            column=3,
            padx=10
        )

        # Attendance table
        table_frame = tk.LabelFrame(
            self.root,
            text=" Attendance Records ",
            font=("Arial", 14, "bold"),
            fg="#00e5ff",
            bg="#18232c"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        columns = (
            "Student Name",
            "Register No",
            "IP Address",
            "MAC Address",
            "Date",
            "Time",
            "Status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=130,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Status
        self.status_label = tk.Label(
            self.root,
            text="System Ready",
            font=("Arial", 12, "bold"),
            fg="#00ff88",
            bg="#101820"
        )
        self.status_label.pack(pady=10)

    # ==================================================
    # NETWORK INFORMATION
    # ==================================================

    def get_network_info(self):

        try:

            hostname = socket.gethostname()

            ip = socket.gethostbyname(
                hostname
            )

            mac = ":".join(
                [
                    f"{(uuid.getnode() >> element) & 0xff:02x}"
                    for element in range(
                        0, 8 * 6, 8
                    )
                ][::-1]
            )

            self.hostname_label.config(
                text=f"Computer: {hostname}"
            )

            self.ip_label.config(
                text=f"IP Address: {ip}"
            )

            self.mac_label.config(
                text=f"MAC Address: {mac}"
            )

        except Exception:

            self.hostname_label.config(
                text="Computer: Unknown"
            )

            self.ip_label.config(
                text="IP Address: Unknown"
            )

            self.mac_label.config(
                text="MAC Address: Unknown"
            )

    # ==================================================
    # MARK ATTENDANCE
    # ==================================================

    def mark_attendance(self):

        name = self.name_entry.get().strip()
        reg = self.reg_entry.get().strip()

        if name == "" or reg == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter Student Name and Register Number."
            )

            return

        hostname = socket.gethostname()

        try:
            ip = socket.gethostbyname(
                hostname
            )
        except:
            ip = "Unknown"

        mac = ":".join(
            [
                f"{(uuid.getnode() >> element) & 0xff:02x}"
                for element in range(
                    0, 8 * 6, 8
                )
            ][::-1]
        )

        now = datetime.now()

        date = now.strftime(
            "%d-%m-%Y"
        )

        time = now.strftime(
            "%H:%M:%S"
        )

        # Prevent duplicate attendance
        for record in self.attendance:

            if record["reg"] == reg and record["date"] == date:

                messagebox.showinfo(
                    "Already Marked",
                    "Attendance is already marked for this student today."
                )

                return

        record = {
            "name": name,
            "reg": reg,
            "ip": ip,
            "mac": mac,
            "date": date,
            "time": time,
            "status": "Present"
        }

        self.attendance.append(
            record
        )

        self.table.insert(
            "",
            "end",
            values=(
                name,
                reg,
                ip,
                mac,
                date,
                time,
                "Present"
            )
        )

        self.status_label.config(
            text=f"Attendance marked for {name}",
            fg="#00ff88"
        )

        self.name_entry.delete(
            0,
            tk.END
        )

        self.reg_entry.delete(
            0,
            tk.END
        )

    # ==================================================
    # NETWORK SCANNER
    # ==================================================

    def scan_network(self):

        self.status_label.config(
            text="Scanning local network...",
            fg="#ffaa00"
        )

        try:

            hostname = socket.gethostname()

            local_ip = socket.gethostbyname(
                hostname
            )

            parts = local_ip.split(".")

            if len(parts) != 4:

                raise Exception(
                    "Unable to determine local network."
                )

            network_prefix = ".".join(
                parts[:3]
            )

            found = []

            for i in range(1, 255):

                ip = f"{network_prefix}.{i}"

                result = subprocess.run(
                    [
                        "ping",
                        "-n",
                        "1",
                        "-w",
                        "100",
                        ip
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                if result.returncode == 0:

                    found.append(ip)

            messagebox.showinfo(
                "Network Scan",
                "Active devices found:\n\n"
                + "\n".join(found)
            )

            self.status_label.config(
                text=f"Network scan completed - {len(found)} devices found",
                fg="#00ff88"
            )

        except Exception as e:

            messagebox.showerror(
                "Scan Error",
                str(e)
            )

            self.status_label.config(
                text="Network scan failed",
                fg="#ff5555"
            )

    # ==================================================
    # EXPORT CSV
    # ==================================================

    def export_csv(self):

        if not self.attendance:

            messagebox.showwarning(
                "No Records",
                "There are no attendance records to export."
            )

            return

        filename = (
            "attendance_"
            + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".csv"
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Student Name",
                    "Register Number",
                    "IP Address",
                    "MAC Address",
                    "Date",
                    "Time",
                    "Status"
                ]
            )

            for record in self.attendance:

                writer.writerow(
                    [
                        record["name"],
                        record["reg"],
                        record["ip"],
                        record["mac"],
                        record["date"],
                        record["time"],
                        record["status"]
                    ]
                )

        messagebox.showinfo(
            "Export Successful",
            f"Attendance saved as:\n{os.path.abspath(filename)}"
        )

    # ==================================================
    # CLEAR RECORDS
    # ==================================================

    def clear_records(self):

        if not self.attendance:

            return

        confirm = messagebox.askyesno(
            "Confirm",
            "Delete all attendance records?"
        )

        if confirm:

            self.attendance.clear()

            for item in self.table.get_children():

                self.table.delete(item)

            self.status_label.config(
                text="All records cleared",
                fg="#ff5555"
            )


# ======================================================
# MAIN PROGRAM
# ======================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = NetworkAttendanceSystem(
        root
    )

    root.mainloop()