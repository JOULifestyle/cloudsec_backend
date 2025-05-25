# cwpp/runtime_scanner.py
from datetime import datetime
import socket
import platform
import random

def run_runtime_checks():
    # Simulated runtime security checks
    findings = []

    if platform.system() != "Linux":
        findings.append({"type": "OS Warning", "message": "Non-Linux system detected"})

    try:
        s = socket.socket()
        s.bind(("0.0.0.0", 8888))
        findings.append({"type": "Open Port", "message": "Port 8888 is open to public"})
        s.close()
    except Exception:
        pass

    if random.random() > 0.5:
        findings.append({"type": "Package Alert", "message": "Outdated curl package found"})

    return {
        "scan_type": "CWPP",
        "timestamp": datetime.utcnow().isoformat(),
        "findings": findings
    }
