import socket
import subprocess
import platform
from datetime import datetime


def print_header():
    print("\n" + "=" * 60)
    print("             AUTOTECH | NETWORK DIAGNOSTICS")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Computer:  {socket.gethostname()}")
    print(f"Operating System: {platform.system()}")
    print("=" * 60)


def check_internet():
    print("\n--- Internet Connectivity ---")

    host = "8.8.8.8"

    try:
        result = subprocess.run(
            ["ping", "-n", "4", host],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode == 0:
            print(f"Status: Connected to {host}")
        else:
            print(f"Status: Unable to reach {host}")

        print(result.stdout)

    except subprocess.TimeoutExpired:
        print("Status: Connection test timed out.")

    except Exception as error:
        print(f"Error: {error}")


def check_dns():
    print("\n--- DNS Resolution ---")

    domain = "google.com"

    try:
        ip_address = socket.gethostbyname(domain)
        print(f"Domain: {domain}")
        print(f"Resolved IP: {ip_address}")
        print("Status: DNS resolution successful.")

    except socket.gaierror:
        print("Status: DNS resolution failed.")


def show_network_config():
    print("\n--- Network Configuration ---")

    try:
        result = subprocess.run(
            ["ipconfig"],
            capture_output=True,
            text=True,
            timeout=15
        )

        print(result.stdout)

    except Exception as error:
        print(f"Error: {error}")


def main():
    print_header()

    check_internet()
    check_dns()
    show_network_config()

    print("\n" + "=" * 60)
    print("          NETWORK DIAGNOSTICS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()