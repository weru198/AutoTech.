import os
import socket
import shutil
import platform
import subprocess
from datetime import datetime


def get_system_info():
    return {
        "Computer": socket.gethostname(),
        "Operating System": platform.platform(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
        "Python Version": platform.python_version()
    }


def get_network_info():
    results = {}

    # Internet connectivity
    try:
        ping = subprocess.run(
            ["ping", "-n", "2", "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=10
        )

        results["Internet Connectivity"] = (
            "Connected" if ping.returncode == 0 else "Connection Failed"
        )

    except Exception:
        results["Internet Connectivity"] = "Test Error"

    # DNS resolution
    try:
        ip_address = socket.gethostbyname("google.com")
        results["DNS Resolution"] = f"Successful ({ip_address})"

    except socket.gaierror:
        results["DNS Resolution"] = "Failed"

    return results


def get_disk_info():
    total, used, free = shutil.disk_usage("C:\\")

    usage = (used / total) * 100

    if usage >= 90:
        status = "CRITICAL"
    elif usage >= 80:
        status = "WARNING"
    else:
        status = "HEALTHY"

    return {
        "Total Storage": f"{total / (1024 ** 3):.2f} GB",
        "Used Storage": f"{used / (1024 ** 3):.2f} GB",
        "Free Storage": f"{free / (1024 ** 3):.2f} GB",
        "Disk Usage": f"{usage:.1f}%",
        "Disk Status": status
    }


def get_recommendations(network_info, disk_info):
    """Generate recommendations from diagnostic results."""

    recommendations = []

    # Network checks
    if network_info.get("Internet Connectivity") == "Connection Failed":
        recommendations.append(
            "NETWORK: Check the network adapter, Wi-Fi or Ethernet "
            "connection, gateway and firewall settings. A failed ping "
            "alone does not prove that internet access is unavailable."
        )

    if network_info.get("DNS Resolution") == "Failed":
        recommendations.append(
            "DNS: Check DNS server configuration and test name resolution "
            "using an approved diagnostic tool."
        )

    # Disk checks
    disk_status = disk_info.get("Disk Status")

    if disk_status == "CRITICAL":
        recommendations.append(
            "STORAGE: Disk usage is critically high. Review large files, "
            "logs and temporary files before deciding what can be removed. "
            "Back up important data first."
        )

    elif disk_status == "WARNING":
        recommendations.append(
            "STORAGE: Disk usage is elevated. Review available space and "
            "plan appropriate storage maintenance."
        )

    # Default when checks don't flag an issue
    if not recommendations:
        recommendations.append(
            "No issues were flagged by the available checks. "
            "This does not guarantee that every system component is healthy."
        )

    return recommendations



def generate_report():
    report = []

    # Run each diagnostic once per report.
    system_info = get_system_info()
    network_info = get_network_info()
    disk_info = get_disk_info()
    recommendations = get_recommendations(network_info, disk_info)

    report.append("=" * 65)
    report.append("             AUTOTECH | TROUBLESHOOTING REPORT")
    report.append("=" * 65)

    report.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    report.append("")

    report.append("--- SYSTEM INFORMATION ---")
    for key, value in system_info.items():
        report.append(f"{key}: {value}")

    report.append("\n--- NETWORK DIAGNOSTICS ---")
    for key, value in network_info.items():
        report.append(f"{key}: {value}")

    report.append("\n--- DISK HEALTH ---")
    for key, value in disk_info.items():
        report.append(f"{key}: {value}")

    report.append("\n--- AUTOMATED RECOMMENDATIONS ---")
    for number, recommendation in enumerate(recommendations, start=1):
        report.append(f"{number}. {recommendation}")

    report.append("\n" + "=" * 65)
    report.append("           END OF TROUBLESHOOTING REPORT")
    report.append("=" * 65)

    return "\n".join(report)





def save_report(report):
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(report)

    return filepath


def main():
    print("\nGenerating troubleshooting report...\n")

    report = generate_report()

    print(report)

    filepath = save_report(report)

    print(f"\nReport saved successfully:\n{filepath}")


if __name__ == "__main__":
    main()