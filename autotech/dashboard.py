import subprocess
import sys
import os
from datetime import datetime


# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def print_header():
    os.system("cls" if os.name == "nt" else "clear")

    print("=" * 65)
    print("                  AUTOTECH")
    print("          IT SUPPORT AUTOMATION TOOLKIT")
    print("=" * 65)
    print(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)


def print_menu():
    print("\n              MAIN DASHBOARD")
    print("-" * 65)

    print("  [1] System Information")
    print("  [2] Network Diagnostics")
    print("  [3] Disk Health & Storage")
    print("  [4] Temporary File Cleanup")
    print("  [5] Troubleshooting Report")
    print("  [6] View Saved Reports")
    print("  [0] Exit AutoTech")

    print("-" * 65)


def run_tool(script_name):
    script_path = os.path.join(BASE_DIR, script_name)

    if not os.path.exists(script_path):
        print(f"\nError: {script_name} was not found.")
        input("\nPress Enter to return to the dashboard...")
        return

    print(f"\nLaunching {script_name}...\n")

    try:
        subprocess.run([sys.executable, script_path], check=False)
    except Exception as error:
        print(f"\nError launching tool: {error}")

    input("\nPress Enter to return to the dashboard...")


def view_reports():
    reports_dir = os.path.join(BASE_DIR, "reports")

    print("\n--- SAVED TROUBLESHOOTING REPORTS ---")

    if not os.path.exists(reports_dir):
        print("\nNo reports folder found.")
        input("\nPress Enter to return...")
        return

    reports = sorted(
        [
            file for file in os.listdir(reports_dir)
            if file.endswith(".txt")
        ],
        reverse=True
    )

    if not reports:
        print("\nNo reports available.")
        input("\nPress Enter to return...")
        return

    for index, report in enumerate(reports, start=1):
        print(f"[{index}] {report}")

    print("\nEnter a report number to view it.")
    print("Enter 0 to return to the dashboard.")

    choice = input("\nYour choice: ").strip()

    if choice == "0":
        return

    try:
        report_index = int(choice) - 1

        if 0 <= report_index < len(reports):
            report_path = os.path.join(reports_dir, reports[report_index])

            with open(report_path, "r", encoding="utf-8") as file:
                content = file.read()

            print("\n" + "=" * 65)
            print(content)
            print("=" * 65)

            input("\nPress Enter to return...")
        else:
            print("\nInvalid report number.")
            input("\nPress Enter to return...")

    except ValueError:
        print("\nPlease enter a valid number.")
        input("\nPress Enter to return...")


def main():
    while True:
        print_header()
        print_menu()

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            run_tool("system_info.py")

        elif choice == "2":
            run_tool("network_diagnostics.py")

        elif choice == "3":
            run_tool("disk_health.py")

        elif choice == "4":
            run_tool("cleanup.py")

        elif choice == "5":
            run_tool("troubleshooting_report.py")

        elif choice == "6":
            view_reports()

        elif choice == "0":
            print("\nThank you for using AutoTech!")
            print("Exiting dashboard...")
            break

        else:
            print("\nInvalid option. Please select a valid menu item.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()