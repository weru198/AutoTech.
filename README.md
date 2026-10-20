
# AutoTech — IT Support Automation Toolkit

AutoTech is a Python-based IT support toolkit designed to help technicians inspect system information, troubleshoot network connectivity, monitor disk usage, review diagnostic history, and generate troubleshooting reports through a web dashboard.

## Features

- **System Information:** View computer and operating-system information.
- **Network Diagnostics:** Run connectivity checks, DNS resolution tests, and network configuration checks.
- **Disk Health:** Review storage capacity, used space, available space, and usage warnings.
- **Temporary File Cleanup:** Preview temporary files, select files for cleanup, and confirm before deletion. The current cleanup implementation skips recently modified files and validates selected files before attempting removal.
- **Troubleshooting Reports:** Generate and save diagnostic reports.
- **Diagnostic History:** Review previous reports and open saved report details.
- **Disk Usage Trend:** Visualize disk usage measurements recorded in saved reports.

## Technology Stack

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- Chart.js
- psutil

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- pip
- Git (optional, for cloning the repository)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/weru198/AutoTech.git
   ```

2. Open the project directory:

   ```bash
   cd AutoTech
   ```

3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the Application

From the project root, run:

```bash
python app.py
```

Open the local dashboard in your browser:

http://127.0.0.1:5000/

If `python` is not available on your PATH, use the full path to your Python interpreter.

## Project Structure

```text
AutoTech/
├── app.py
├── requirements.txt
├── autotech/
│   ├── cleanup.py
│   ├── dashboard.py
│   ├── disk_health.py
│   ├── network_diagnostics.py
│   ├── system_info.py
│   └── troubleshooting_report.py
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── cleanup.html
    ├── cleanup_result.html
    ├── dashboard.html
    ├── diagnostic_history.html
    ├── disk_health.html
    ├── disk_report.html
    ├── full_report_result.html
    ├── network.html
    ├── network_report.html
    ├── reports.html
    ├── system_info.html
    └── view_report.html
```

## Safety and Limitations

- Diagnostic reports can contain computer and network details. Generated reports are excluded from the repository by `.gitignore`.
- The cleanup tool requires explicit confirmation and attempts to validate selected files before deleting them.
- Run cleanup cautiously. Files may be in use, and filesystem changes can occur between validation and deletion.
- Disk usage checks indicate storage capacity, not the physical health of a disk.
- The disk usage chart relies on Chart.js from a CDN and therefore requires internet access to load the chart library.
- This project is a portfolio and learning tool, not a replacement for enterprise endpoint management or monitoring software.

## Future Improvements

- Integrate AutoTech diagnostics with the SmartDesk IT ticketing system.
- Improve automated diagnostic recommendations and error handling.
- Add more testing, documentation, and interface refinements.

## Author

**Alex Waweru**

GitHub: https://github.com/weru198

Portfolio: https://aw-portfolio-t7ll.vercel.app/
