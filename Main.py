#!/usr/bin/env python3
"""
Scannerv2 Main Script
====================

This script provides a command-line and graphical interface for Scannerv2.
Allows scanning websites for various web vulnerabilities.
"""

import os
import sys
import argparse
import time
from datetime import datetime

try:
    import pygame.mixer
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

class ColorPrinter:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    
    @staticmethod
    def colorize(color, text):
        return f"{color}{text}{ColorPrinter.RESET}"

def play_sound(sound_file):
    """Play a sound file using pygame mixer."""
    if not HAS_PYGAME:
        return
    
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Warning: Could not play sound ({e})")

def banner():
    """Display ASCII art banner for Scannerv2."""
    banner_text = r"""
╔═╗╦  ╔═╗╔═╗╔═╗╗ ╦╔═══╗╔═╗╔═╗
║ ∈║╚═╗║╣ ║ ║║ ║╚═╗ ║╣ ╠═╝╚═╗
╚══╩═╩╝╚═╝╚═╝╚═╝╩ ╩╚═══╝╚═╝╚══╝
"""
    print(ColorPrinter.colorize(ColorPrinter.GREEN, banner_text))

def show_menu():
    """Show command-line menu."""
    print("\n===== Scannerv2 Menu =====")
    print("\n1. Start New Scan")
    print("2. View Scan History")
    print("3. Export Results")
    print("4. Settings")
    print("5. Quit\n")
    
    choice = input("Select an option [1-5]: ")
    return choice

def scan_website(url, verbose=False):
    """Simulate scanning a website for vulnerabilities."""
    banner()
    print(ColorPrinter.colorize(ColorPrinter.YELLOW, f"\n[+] Starting scan for {url}..."))
    
    findings = {
        "url": url,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "findings": []
    }
    
    # Simulate scanning process
    print(ColorPrinter.colorize(ColorPrinter.BLUE, "[*] Checking for open directories..."))
    time.sleep(1)
    
    print(ColorPrinter.colorize(ColorPrinter.BLUE, "[*] Running vulnerability scans..."))
    time.sleep(2)
    
    print(ColorPrinter.colorize(ColorPrinter.YELLOW, "[*] Analyzing SSL/TLS configuration..."))
    time.sleep(1)
    
    # Generate random findings
    import random
    num_findings = random.randint(1, 5)
    
    if num_findings > 0:
        print(ColorPrinter.colorize(ColorPrinter.RED, "[!] Potential vulnerabilities found!"))
        for i in range(num_findings):
            finding_type = "SQL Injection"
            severity = "High"
            recommendation = "Implement prepared statements to prevent SQL injection."
            
            findings["findings"].append({
                "type": finding_type,
                "severity": severity,
                "recommendation": recommendation
            })
            
            print(ColorPrinter.colorize(ColorPrinter.RED, f"  [Finding {i+1}]"))
            print(ColorPrinter.colorize(ColorPrinter.RED, f"      Type: {finding_type}"))
            print(ColorPrinter.colorize(ColorPrinter.RED, f"      Severity: {severity}"))
            print(ColorPrinter.colorize(ColorPrinter.RED, f"      Recommendation: {recommendation}\n"))
    else:
        print(ColorPrinter.colorize(ColorPrinter.GREEN, "[+] No vulnerabilities detected.\n"))
    
    print(ColorPrinter.colorize(ColorPrinter.GREEN, "[+] Scan completed successfully!\n"))
    
    # Save scan history
    save_scan(findings)
    return findings

def save_scan(scan_data):
    """Save scan findings to file."""
    filename = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join("scans", filename)
    
    try:
        if not os.path.exists("scans"):
            os.makedirs("scans")
            
        with open(filepath, "w") as f:
            import json
            json.dump(scan_data, f, indent=4)
        
        print(ColorPrinter.colorize(ColorPrinter.GREEN, f"[+] Scan saved to {filepath}"))
        play_sound("scan_complete.wav")
    except Exception as e:
        print(ColorPrinter.colorize(ColorPrinter.RED, f"[!] Failed to save scan: {e}"))

def view_history():
    """List previous scan history."""
    banner()
    print("\n===== Scan History =====\n")
    
    scans_dir = "scans"
    if not os.path.exists(scans_dir) or not os.listdir(scans_dir):
        print(ColorPrinter.colorize(ColorPrinter.YELLOW, "No previous scans found."))
        return
        
    scans = sorted(os.listdir(scans_dir), reverse=True)
    
    for i, scan_file in enumerate(scans[:10]):  # Show last 10 scans
        timestamp = scan_file.replace(".json", "").split("_")[1]
        date_str = datetime.strptime(timestamp, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        print(f"{i+1}) Scan ID: {scan_file}, Date: {date_str}")
        
    print("\nEnter s<scan_num> to view a specific scan, or press Enter to go back.")
    choice = input("Selection: ").strip()
    
    if choice.startswith("s") and len(choice) > 1:
        try:
            scan_index = int(choice[1:]) - 1
            if 0 <= scan_index < len(scans):
                display_scan_details(scans[scan_index])
            else:
                print(ColorPrinter.colorize(ColorPrinter.RED, "Invalid scan index selected."))
        except ValueError:
            print(ColorPrinter.colorize(ColorPrinter.RED, "Invalid selection format."))
            
def display_scan_details(filename):
    """Display detailed information about a specific scan."""
    filepath = os.path.join("scans", filename)
    
    try:
        with open(filepath, "r") as f:
            import json
            scan_data = json.load(f)
            
        banner()
        print(f"\n===== Scan Details: {filename} =====\n")
        
        print(ColorPrinter.colorize(ColorPrinter.YELLOW, 
              f"URL: {scan_data['url']}"))
        print(ColorPrinter.colorize(ColorPrinter.YELLOW, 
              f"Date: {scan_data['scan_time']}\n"))
              
        if scan_data["findings"]:
            print(ColorPrinter.colorize(ColorPrinter.RED, "[!] Vulnerabilities Found:\n"))
            
            for i, finding in enumerate(scan_data["findings"], 1):
                print(ColorPrinter.colorize(ColorPrinter.RED, f"Finding {i}:"))
                print(
