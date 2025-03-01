# brute_force_detection

A Python-based brute force detection system designed to monitor and mitigate brute force attacks. This project includes various scripts for monitoring logs, detecting brute force attempts, and blocking/unblocking malicious IPs. The logs are analyzed from /var/log/authlog to identify suspicious login activity.

## Project Structure

- main.py: The main entry point for running the brute force detection system.
- scripts/monitor.py: Monitors the /var/log/authlog file for login attempts and continuously tracks log file changes to identify new failed login attempts
- scripts/detect.py: Analyzes authentication logs to identify and track patterns of brute force attacks.
- scripts/block.py: Blocks IP addresses identified as malicious.
- scripts/unblock.py: Unblocks IP addresses after a certain amount of time.

## Requirements

- Python 3.x
- Linux-based system (for /var/log/authlog)

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/SDIKIYOUSRA/brute_force_detection.git
   cd brute_force_detection
