"""
AutoTech - System Information Tool
Collects basic computer and operating-system details using Python's standard library.
Run: python system_info.py
"""

from datetime import datetime
import os
import platform
import shutil
import socket


def get_memory_info():
    """Return RAM details on Windows; gracefully report when unavailable."""
    if platform.system() != "Windows":
        return "RAM details: use the platform's system monitor (Windows-specific function)."

    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            total_gb = status.ullTotalPhys / (1024 ** 3)
            available_gb = status.ullAvailPhys / (1024 ** 3)
            used_percent = status.dwMemoryLoad
            return (
                f"Total RAM: {total_gb:.2f} GB\n"
                f"Available RAM: {available_gb:.2f} GB\n"
                f"RAM usage: {used_percent}%"
            )
    except (AttributeError, OSError):
        pass

    return "RAM details could not be retrieved."


def get_disk_info():
    """Report usage for the drive containing the current working directory."""
    target = os.environ.get("SystemDrive", "C:") + "\\" if platform.system() == "Windows" else "/"
    try:
        usage = shutil.disk_usage(target)
        total = usage.total / (1024 ** 3)
        used = usage.used / (1024 ** 3)
        free = usage.free / (1024 ** 3)
        return (
            f"Drive checked: {target}\n"
            f"Total: {total:.2f} GB\n"
            f"Used: {used:.2f} GB\n"
            f"Free: {free:.2f} GB"
        )
    except OSError as exc:
        return f"Disk details unavailable: {exc}"


def main():
    separator = "=" * 58
    print("\n" + separator)
    print("             AUTOTECH | SYSTEM INFORMATION")
    print(separator)
    print(f"Generated:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Computer name:    {socket.gethostname()}")
    print(f"Operating system: {platform.system()} {platform.release()}")
    print(f"OS version:       {platform.version()}")
    print(f"Architecture:     {platform.machine()}")
    print(f"Processor:        {platform.processor() or 'Not reported'}")
    print(f"Python version:   {platform.python_version()}")
    print(f"Current user:     {os.environ.get('USERNAME') or os.environ.get('USER') or 'Not reported'}")
    print("\n--- Memory ---")
    print(get_memory_info())
    print("\n--- Disk ---")
    print(get_disk_info())
    print(separator)
    print("Note: This tool only reads system information; it changes nothing.")
    print(separator + "\n")


if __name__ == "__main__":
    main()
