from flask import Flask, render_template
import platform
import socket
import sys
import shutil
import subprocess
import getpass
import psutil
import re
import os
from datetime import datetime
from autotech.cleanup import get_cleanup_summary, format_size
from autotech.troubleshooting_report import generate_report, save_report
app = Flask(__name__)


@app.route("/")
def dashboard():
    # ==========================================
    # SYSTEM INFORMATION
    # ==========================================
    system_info = {
        "hostname": socket.gethostname(),
        "os": platform.system() + " " + platform.release(),
        "processor": platform.processor() or "Not available",
        "python_version": sys.version.split()[0]
    }

    # ==========================================
    # DISK INFORMATION
    # ==========================================
    disk = shutil.disk_usage("C:\\")
    disk_info = {
        "total": round(disk.total / (1024 ** 3), 2),
        "used": round(disk.used / (1024 ** 3), 2),
        "free": round(disk.free / (1024 ** 3), 2),
        "usage_percent": round((disk.used / disk.total) * 100, 1)
    }

    # ==========================================
    # NETWORK CONNECTIVITY
    # ==========================================
    network_status = "Offline"

    try:
        result = subprocess.run(
            ["ping", "-n", "1", "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            network_status = "Online"
    except Exception:
        network_status = "Offline"

    # ==========================================
    # SEND DATA TO DASHBOARD
    # ==========================================
    return render_template(
        "dashboard.html",
        system_info=system_info,
        disk_info=disk_info,
        network_status=network_status
    )


@app.route("/system-info")
def system_information():

    system_info = {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "Not available",
        "python_version": sys.version.split()[0],
        "username": getpass.getuser()
    }



    # Memory information
    memory_data = psutil.virtual_memory()

    memory = {
        "total": round(memory_data.total / (1024 ** 3), 2),
        "available": round(memory_data.available / (1024 ** 3), 2),
        "used": round(memory_data.used / (1024 ** 3), 2),
        "percent": memory_data.percent
    }
   
        # CPU information
    cpu_info = {
        "cores": psutil.cpu_count(logical=False),
        "logical_processors": psutil.cpu_count(logical=True),
        "usage_percent": psutil.cpu_percent(interval=1)
    }


             # System uptime
    boot_time = psutil.boot_time()

    uptime_seconds = int(
        __import__("time").time() - boot_time
    )

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    uptime = {
        "days": days,
        "hours": hours,
        "minutes": minutes
    }

    return render_template(
        "system_info.html",
        system_info=system_info,
        memory=memory,
        cpu_info=cpu_info,
        uptime=uptime
    )



@app.route("/network")
def network_diagnostics():

    # ==========================================
    # HOST INFORMATION
    # ==========================================

    hostname = socket.gethostname()

    # Local IP address
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "Not available"


    # ==========================================
    # NETWORK ADAPTER INFORMATION
    # ==========================================

    adapters = []

    for interface, addresses in psutil.net_if_addrs().items():

        ipv4_address = "Not available"
        mac_address = "Not available"

        for address in addresses:

            if address.family == socket.AF_INET:
                ipv4_address = address.address

            elif getattr(psutil, "AF_LINK", None) == address.family:
                mac_address = address.address

        adapters.append({
            "name": interface,
            "ip": ipv4_address,
            "mac": mac_address
        })


    # ==========================================
    # DEFAULT GATEWAY & DNS
    # ==========================================

    gateway = "Not available"
    dns_servers = []

    try:

        result = subprocess.run(
            ["ipconfig", "/all"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        output = result.stdout

        # Default Gateway
        gateway_match = re.search(
            r"Default Gateway[ .]*:\s*([0-9.]+)",
            output
        )

        if gateway_match:
            gateway = gateway_match.group(1)

        # DNS Servers
        dns_matches = re.findall(
            r"DNS Servers[ .]*:\s*([0-9.]+)",
            output
        )

        dns_servers = list(dict.fromkeys(dns_matches))

    except Exception:
        pass


    # ==========================================
    # INTERNET CONNECTIVITY
    # ==========================================

    internet_status = "Offline"

    try:

        result = subprocess.run(
            ["ping", "-n", "1", "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            internet_status = "Online"

    except Exception:
        internet_status = "Offline"


    # ==========================================
    # PING & LATENCY TEST
    # ==========================================

    ping_target = "8.8.8.8"
    ping_status = "Failed"
    ping_latency = "N/A"

    try:

        result = subprocess.run(
            ["ping", "-n", "1", ping_target],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:

            ping_status = "Successful"

            latency_match = re.search(
                r"time[=<]\s*(\d+)ms",
                result.stdout,
                re.IGNORECASE
            )

            if latency_match:
                ping_latency = f"{latency_match.group(1)} ms"

    except Exception:

        ping_status = "Failed"


    # ==========================================
    # SEND DATA TO NETWORK PAGE
    # ==========================================

    return render_template(
        "network.html",
        hostname=hostname,
        local_ip=local_ip,
        adapters=adapters,
        gateway=gateway,
        dns_servers=dns_servers,
        internet_status=internet_status,
        ping_target=ping_target,
        ping_status=ping_status,
        ping_latency=ping_latency
    )
    

@app.route("/disk-health")
def disk_health():

    disks = []

    # Get all Windows disk partitions
    for partition in psutil.disk_partitions():

        # Skip drives that cannot be accessed
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue

        total_gb = round(usage.total / (1024 ** 3), 2)
        used_gb = round(usage.used / (1024 ** 3), 2)
        free_gb = round(usage.free / (1024 ** 3), 2)

        usage_percent = usage.percent

        # Determine storage status
        if usage_percent >= 90:
            status = "Critical"
        elif usage_percent >= 75:
            status = "Warning"
        else:
            status = "Healthy"

        disks.append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "filesystem": partition.fstype,
            "total": total_gb,
            "used": used_gb,
            "free": free_gb,
            "usage_percent": usage_percent,
            "status": status
        })

    return render_template(
        "disk_health.html",
        disks=disks
    )

@app.route("/run-disk-diagnostics")
def run_disk_diagnostics():

    results = []

    # ==========================================
    # CHECK AVAILABLE DISKS
    # ==========================================

    partitions = psutil.disk_partitions()

    if not partitions:

        results.append({
            "name": "Disk Detection",
            "value": "No drives detected",
            "status": "Failed"
        })

    else:

        results.append({
            "name": "Disk Detection",
            "value": f"{len(partitions)} drive(s) detected",
            "status": "Passed"
        })


    # ==========================================
    # CHECK EACH DRIVE
    # ==========================================

    for partition in partitions:

        try:

            usage = psutil.disk_usage(
                partition.mountpoint
            )

            total_gb = round(
                usage.total / (1024 ** 3),
                2
            )

            used_gb = round(
                usage.used / (1024 ** 3),
                2
            )

            free_gb = round(
                usage.free / (1024 ** 3),
                2
            )

            usage_percent = usage.percent


            # Determine health

            if usage_percent >= 90:

                status = "Critical"

            elif usage_percent >= 75:

                status = "Warning"

            else:

                status = "Healthy"


            results.append({
                "name": f"{partition.mountpoint} Storage",
                "value": (
                    f"{used_gb} GB used / "
                    f"{free_gb} GB free / "
                    f"{total_gb} GB total"
                ),
                "status": status
            })


        except PermissionError:

            results.append({
                "name": f"{partition.mountpoint} Access",
                "value": "Access denied",
                "status": "Warning"
            })


        except Exception as error:

            results.append({
                "name": f"{partition.mountpoint} Check",
                "value": str(error),
                "status": "Failed"
            })


    # ==========================================
    # SUMMARY
    # ==========================================

    passed = sum(
        1
        for result in results
        if result["status"] == "Passed"
        or result["status"] == "Healthy"
    )

    warnings = sum(
        1
        for result in results
        if result["status"] == "Warning"
    )

    failed = sum(
        1
        for result in results
        if result["status"] == "Failed"
        or result["status"] == "Critical"
    )


    # ==========================================
    # CREATE REPORT FOLDER
    # ==========================================

    report_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "reports"
    )

    os.makedirs(
        report_folder,
        exist_ok=True
    )


    # ==========================================
    # CREATE REPORT FILE
    # ==========================================

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_filename = (
        f"disk_report_{timestamp}.txt"
    )

    report_path = os.path.join(
        report_folder,
        report_filename
    )


    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as report:

        report.write(
            "AUTOTECH DISK DIAGNOSTIC REPORT\n"
        )

        report.write(
            "================================\n\n"
        )

        report.write(
            "Generated: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )


        for result in results:

            report.write(
                f"{result['name']}\n"
            )

            report.write(
                f"Value: {result['value']}\n"
            )

            report.write(
                f"Status: {result['status']}\n\n"
            )


        report.write(
            "--------------------------------\n"
        )

        report.write(
            f"Passed Checks: {passed}\n"
        )

        report.write(
            f"Warnings: {warnings}\n"
        )

        report.write(
            f"Failed/Critical Checks: {failed}\n"
        )

        report.write(
            "--------------------------------\n"
        )


    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    return render_template(
        "disk_report.html",
        results=results,
        passed=passed,
        warnings=warnings,
        failed=failed
    )

@app.route("/reports")
def reports():

    report_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "reports"
    )

    reports = []

    if os.path.exists(report_folder):

        for filename in os.listdir(report_folder):

            if filename.endswith(".txt"):

                file_path = os.path.join(
                    report_folder,
                    filename
                )

                modified_time = os.path.getmtime(file_path)

                reports.append({
                    "filename": filename,
                    "modified": datetime.fromtimestamp(
                        modified_time
                    ).strftime("%Y-%m-%d %H:%M:%S")
                })

    # Newest reports first
    reports.sort(
        key=lambda report: report["modified"],
        reverse=True
    )

    return render_template(
        "reports.html",
        reports=reports
    )


from flask import request, redirect, url_for, flash
from autotech.cleanup import (
    get_cleanup_summary,
    format_size,
    clean_selected_files
)

@app.route("/cleanup", methods=["GET", "POST"])
def cleanup():

    if request.method == "POST":
        selected_paths = request.form.getlist("selected_files")

        if not selected_paths:
            flash("Select at least one file to clean.", "warning")
            return redirect(url_for("cleanup"))

        # Refresh the preview and allow only files currently listed.
        current_files = get_cleanup_summary()["files"]
        allowed_paths = {
            os.path.realpath(item["path"])
            for item in current_files
        }

        safe_paths = [
            path for path in selected_paths
            if os.path.realpath(path) in allowed_paths
        ]

        if not safe_paths:
            flash(
                "No valid files were selected. Refresh the preview.",
                "warning"
            )
            return redirect(url_for("cleanup"))

        results = clean_selected_files(safe_paths)

        return render_template(
            "cleanup_result.html",
            results=results
        )

    cleanup_data = get_cleanup_summary()

    return render_template(
        "cleanup.html",
        temp_folder=cleanup_data["temp_folder"],
        file_count=cleanup_data["file_count"],
        total_size=format_size(cleanup_data["total_size"]),
        files=cleanup_data["files"],
        format_size=format_size
    )



@app.route("/reports/<filename>")
def view_report(filename):

    report_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "reports"
    )

    file_path = os.path.join(
        report_folder,
        filename
    )

    # Only allow .txt reports
    if not filename.endswith(".txt"):
        return "Invalid report file.", 400

    # Make sure the requested file exists
    if not os.path.isfile(file_path):
        return "Report not found.", 404

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as report_file:

        report_content = report_file.read()

    return render_template(
        "view_report.html",
        filename=filename,
        report_content=report_content
    )        


@app.route("/generate-full-report", methods=["POST"])
def generate_full_report():

    try:
        # Generate the complete troubleshooting report.
        report_content = generate_report()

        # Save it to the existing report generator's folder.
        filepath = save_report(report_content)

        filename = os.path.basename(filepath)

        return render_template(
            "full_report_result.html",
            filename=filename,
            report_content=report_content,
            success=True
        )

    except Exception as error:
        app.logger.exception("Full troubleshooting report failed")

        return render_template(
            "full_report_result.html",
            filename=None,
            report_content=None,
            success=False,
            error_message=str(error)
        ), 500


def collect_diagnostic_history():
    """Read saved troubleshooting reports for historical comparison."""

    project_folder = os.path.dirname(os.path.abspath(__file__))

    report_folders = [
        os.path.join(project_folder, "reports"),
        os.path.join(project_folder, "autotech", "reports")
    ]

    history = []
    seen_files = set()

    for folder in report_folders:
        if not os.path.isdir(folder):
            continue

        for filename in os.listdir(folder):
            if not filename.endswith(".txt"):
                continue

            filepath = os.path.realpath(
                os.path.join(folder, filename)
            )

            if filepath in seen_files:
                continue

            seen_files.add(filepath)

            try:
                with open(
                    filepath, "r", encoding="utf-8"
                ) as report_file:
                    content = report_file.read()

                # Only include full troubleshooting reports.
                if "TROUBLESHOOTING REPORT" not in content:
                    continue

                def extract(pattern, default="Not recorded"):
                    match = re.search(
                        pattern, content, re.IGNORECASE | re.MULTILINE
                    )
                    return match.group(1).strip() if match else default

                generated = extract(
                    r"Generated:\s*(.+)"
                )

                disk_usage = extract(
                    r"Disk Usage:\s*([0-9]+(?:\.[0-9]+)?%)"
                )

                disk_status = extract(
                    r"Disk Status:\s*(HEALTHY|WARNING|CRITICAL)"
                )

                internet = extract(
                    r"Internet Connectivity:\s*(.+)"
                )

                dns = extract(
                    r"DNS Resolution:\s*(.+)"
                )

                history.append({
                    "filename": filename,
                    "generated": generated,
                    "disk_usage": disk_usage,
                    "disk_status": disk_status,
                    "internet": internet,
                    "dns": dns,
                    "modified": os.path.getmtime(filepath)
                })

            except (OSError, UnicodeError):
                continue

    history.sort(
        key=lambda item: item["modified"],
        reverse=True
    )

    return history


@app.route("/diagnostic-history")
def diagnostic_history():
    history = collect_diagnostic_history()

    return render_template(
        "diagnostic_history.html",
        history=history
    )



if __name__ == "__main__":
    app.run(debug=True)