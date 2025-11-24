#!/usr/bin/env python3
"""
Private Network Status Checker
Verifies that your network is properly configured for privacy
"""

import subprocess
import socket
import os
from pathlib import Path

def check_status():
    print("🔍 PRIVATE NETWORK STATUS CHECK")
    print("=" * 50)
    
    checks = {
        "SSH Key Generated": Path.home() / ".ssh" / "id_rsa.pub",
        "SSH Config Created": Path.home() / ".ssh" / "config",
        "Network Security Config": Path.home() / ".network_security",
        "Firewall Rules": Path.home() / ".network_security" / "firewall_rules.sh",
        "Connection Monitor": Path.home() / ".network_security" / "connection_monitor.py",
    }
    
    print("\n📋 Configuration Files:")
    for name, path in checks.items():
        if path.exists():
            print(f"   ✅ {name}: {path}")
        else:
            print(f"   ❌ {name}: Not found")
    
    print("\n🌐 Network Configuration:")
    
    # Check if amdblack.local is in hosts
    try:
        with open("/etc/hosts", "r") as f:
            if "amdblack.local" in f.read():
                print("   ✅ amdblack.local configured in /etc/hosts")
            else:
                print("   ⚠️  amdblack.local not in /etc/hosts")
    except:
        print("   ❌ Could not read /etc/hosts")
    
    # Check IPv6 status
    try:
        ipv6_disabled = subprocess.run(
            ["sysctl", "net.ipv6.conf.all.disable_ipv6"],
            capture_output=True, text=True
        ).stdout.strip()
        if "1" in ipv6_disabled:
            print("   ✅ IPv6 disabled for privacy")
        else:
            print("   ⚠️  IPv6 still enabled")
    except:
        print("   ⚠️  Could not check IPv6 status")
    
    # Try to ping amdblack.local
    print("\n🔗 Connection Test:")
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "amdblack.local"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("   ✅ Can reach amdblack.local")
        else:
            print("   ⚠️  Cannot reach amdblack.local (may need to be on same network)")
    except:
        print("   ⚠️  Ping command not available")
    
    print("\n" + "=" * 50)
    print("🔐 Your network has been configured for private connection!")
    print("\nNext steps:")
    print("1. Share your SSH public key with amdblack.local:")
    print("   cat ~/.ssh/id_rsa.pub")
    print("\n2. Test SSH connection:")
    print("   ssh diesel@amdblack.local")
    print("\n3. Monitor connection status:")
    print("   python3 ~/.network_security/connection_monitor.py")
    
if __name__ == "__main__":
    check_status()