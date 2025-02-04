import os
import shutil
import psutil
import smtplib
import time
from email.mime.text import MIMEText

# Email configuration
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'
TO_EMAIL = 'recipient@example.com'

def send_email(report):
    msg = MIMEText(report)
    msg['Subject'] = 'System Health Report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

def check_disk_usage(disk):
    du = shutil.disk_usage(disk)
    free_percentage = du.free / du.total * 100
    return free_percentage > 20

def check_memory_usage():
    memory = psutil.virtual_memory()
    return memory.available > 500 * 1024 * 1024  # More than 500 MB available

def check_cpu_usage():
    return psutil.cpu_percent(interval=1) < 80  # Less than 80% CPU usage

def monitor_running_services():
    services = []
    for service in psutil.win_service_iter():
        services.append((service.name(), service.status()))
    return services

def generate_report():
    report = []
    
    report.append(f"Disk Usage: {'OK' if check_disk_usage('/') else 'WARNING'}")
    report.append(f"Memory Usage: {'OK' if check_memory_usage() else 'WARNING'}")
    report.append(f"CPU Usage: {'OK' if check_cpu_usage() else 'WARNING'}")
    
    services_status = monitor_running_services()
    report.append("Running Services:")
    for name, status in services_status:
        report.append(f"{name}: {status}")

    return "\n".join(report)

def main_menu():
    while True:
        print("\nSystem Health Check Menu")
        print("1. Check Disk Usage")
        print("2. Monitor Running Services")
        print("3. Assess Memory Usage")
        print("4. Evaluate CPU Usage")
        print("5. Send Comprehensive Report via Email")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == '1':
            print(f"Disk Usage: {'OK' if check_disk_usage('/') else 'WARNING'}")
        elif choice == '2':
            services_status = monitor_running_services()
            for name, status in services_status:
                print(f"{name}: {status}")
        elif choice == '3':
            print(f"Memory Usage: {'OK' if check_memory_usage() else 'WARNING'}")
        elif choice == '4':
            print(f"CPU Usage: {'OK' if check_cpu_usage() else 'WARNING'}")
        elif choice == '5':
            report = generate_report()
            send_email(report)
            print("Report sent via email.")
        elif choice == '6':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    while True:
        main_menu()
        time.sleep(14400)  # Wait for four hours before showing the menu again
