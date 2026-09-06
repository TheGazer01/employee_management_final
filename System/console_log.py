import time

from art import text2art
from colorama import init as colorama_init
from termcolor import colored
from tabulate import tabulate
from tqdm import tqdm

colorama_init(autoreset=True)

TABLE_HEADERS = ["Name", "Age", "Employee ID", "Department", "Position"]


def show_banner():
    banner = text2art("EMS", font="small")
    print(colored(banner, "blue"))
    print(colored("   Employee Management System - starting up...", "yellow"))
    print()


def show_loading_bar():
    for _ in tqdm(range(100), desc="Loading", ncols=60, colour="green"):
        time.sleep(0.01)
    print()


def log_success(msg):
    print(colored(f"[OK] {msg}", "green"))


def log_error(msg):
    print(colored(f"[ERROR] {msg}", "red"))


def log_info(msg):
    print(colored(f"[i] {msg}", "cyan"))


def log_employee_table(employees):
    if not employees:
        log_info("No employees to show.")
        return
    rows = [emp.to_row() for emp in employees]
    print(tabulate(rows, headers=TABLE_HEADERS, tablefmt="fancy_grid"))