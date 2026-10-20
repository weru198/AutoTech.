import shutil
import platform
from datetime import datetime


def print_header():
    print("\n" + "=" * 60)
    print("             AUTOTECH | DISK HEALTH & STORAGE")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Operating System: {platform.system()}")
    print("=" * 60)


def check_disk(drive):
    print(f"\n--- Drive: {drive} ---")

    try:
        total, used, free = shutil.disk_usage(drive)

        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        free_gb = free / (1024 ** 3)
        usage_percent = (used / total) * 100

        print(f"Total Storage:     {total_gb:.2f} GB")
        print(f"Used Storage:      {used_gb:.2f} GB")
        print(f"Free Storage:      {free_gb:.2f} GB")
        print(f"Storage Usage:     {usage_percent:.1f}%")

        if usage_percent >= 90:
            print("Status: CRITICAL - Disk space is almost full!")
        elif usage_percent >= 80:
            print("Status: WARNING - Disk space is running low.")
        else:
            print("Status: HEALTHY - Sufficient storage available.")

    except OSError as error:
        print(f"Error checking drive: {error}")


def main():
    print_header()

    if platform.system() == "Windows":
        drives = ["C:\\"]

        for drive in drives:
            check_disk(drive)
    else:
        check_disk("/")

    print("\n" + "=" * 60)
    print("           DISK HEALTH CHECK COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()