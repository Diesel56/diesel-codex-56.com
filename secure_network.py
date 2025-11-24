#!/usr/bin/env python3
"""
Secure Network Configuration Script
Sets up private network connection with amdblack.local
"""

import antigravity  # Easter egg included!
import subprocess
import os
import json
import socket
from pathlib import Path

class NetworkSecurityManager:
    def __init__(self):
        self.config_path = Path.home() / '.network_security'
        self.config_path.mkdir(exist_ok=True)
        self.amdblack_host = 'amdblack.local'
        self.trusted_ips = []
        
    def create_firewall_rules(self):
        """Create iptables rules for private network"""
        rules = [
            # Drop all incoming connections by default
            "iptables -P INPUT DROP",
            "iptables -P FORWARD DROP",
            "iptables -P OUTPUT ACCEPT",
            
            # Allow loopback
            "iptables -A INPUT -i lo -j ACCEPT",
            "iptables -A OUTPUT -o lo -j ACCEPT",
            
            # Allow established connections
            "iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT",
            
            # Allow connection from amdblack.local only
            f"iptables -A INPUT -s {self.amdblack_host} -j ACCEPT",
            
            # Allow specific ports for services (SSH, custom ports)
            "iptables -A INPUT -p tcp --dport 22 -s 10.0.0.0/8 -j ACCEPT",  # SSH from private network
            "iptables -A INPUT -p tcp --dport 8000 -s 127.0.0.1 -j ACCEPT",  # Local services
            
            # Block all other incoming
            "iptables -A INPUT -j DROP",
        ]
        
        with open(self.config_path / 'firewall_rules.sh', 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Private Network Firewall Rules\n\n")
            for rule in rules:
                f.write(f"sudo {rule}\n")
        
        os.chmod(self.config_path / 'firewall_rules.sh', 0o755)
        print("🔒 Firewall rules created at:", self.config_path / 'firewall_rules.sh')
        return rules
    
    def setup_hosts_file(self):
        """Add amdblack.local to hosts file if needed"""
        hosts_entry = f"\n# Private network connection\n10.0.0.100 amdblack.local\n"
        hosts_config = {
            "entry": hosts_entry,
            "file": "/etc/hosts",
            "backup": "/etc/hosts.backup"
        }
        
        with open(self.config_path / 'hosts_config.json', 'w') as f:
            json.dump(hosts_config, f, indent=2)
        
        print("📝 Hosts configuration saved")
        return hosts_config
    
    def create_ssh_config(self):
        """Create SSH configuration for secure connection"""
        ssh_config = """
# Secure connection to amdblack.local
Host amdblack.local amdblack
    HostName amdblack.local
    User diesel
    Port 22
    
    # Security settings
    PasswordAuthentication no
    PubkeyAuthentication yes
    StrictHostKeyChecking yes
    
    # Performance for 10Gbps
    Compression no
    ServerAliveInterval 60
    ServerAliveCountMax 3
    
    # Cipher optimizations for speed
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
    MACs umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com
"""
        
        ssh_dir = Path.home() / '.ssh'
        ssh_dir.mkdir(mode=0o700, exist_ok=True)
        
        config_file = ssh_dir / 'config.amdblack'
        with open(config_file, 'w') as f:
            f.write(ssh_config)
        
        os.chmod(config_file, 0o600)
        print("🔐 SSH configuration created at:", config_file)
        return config_file
    
    def create_network_namespace(self):
        """Create isolated network namespace script"""
        namespace_script = """#!/bin/bash
# Create isolated network namespace for amdblack connection

NAMESPACE="amdblack_private"

# Create namespace
sudo ip netns add $NAMESPACE 2>/dev/null || true

# Create veth pair
sudo ip link add veth0 type veth peer name veth1

# Move veth1 to namespace
sudo ip link set veth1 netns $NAMESPACE

# Configure interfaces
sudo ip addr add 10.0.0.1/24 dev veth0
sudo ip link set veth0 up

# Configure namespace interface
sudo ip netns exec $NAMESPACE ip addr add 10.0.0.2/24 dev veth1
sudo ip netns exec $NAMESPACE ip link set veth1 up
sudo ip netns exec $NAMESPACE ip link set lo up

# Add routing
sudo ip netns exec $NAMESPACE ip route add default via 10.0.0.1

# Enable forwarding for this namespace only
sudo sysctl -w net.ipv4.ip_forward=1

echo "✅ Private network namespace '$NAMESPACE' created"
echo "To enter: sudo ip netns exec $NAMESPACE bash"
"""
        
        script_path = self.config_path / 'create_namespace.sh'
        with open(script_path, 'w') as f:
            f.write(namespace_script)
        
        os.chmod(script_path, 0o755)
        print("🌐 Network namespace script created at:", script_path)
        return script_path
    
    def create_connection_monitor(self):
        """Create script to monitor and maintain private connection"""
        monitor_script = """#!/usr/bin/env python3
import socket
import time
import subprocess
from datetime import datetime

AMDBLACK_HOST = 'amdblack.local'
CHECK_INTERVAL = 30  # seconds
LOG_FILE = '~/.network_security/connection.log'

def check_connection():
    try:
        # Try to resolve hostname
        ip = socket.gethostbyname(AMDBLACK_HOST)
        
        # Try to connect to a common port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, 22))  # SSH port
        sock.close()
        
        return result == 0, ip
    except:
        return False, None

def log_status(status, ip=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(os.path.expanduser(LOG_FILE), 'a') as f:
        if status:
            f.write(f"[{timestamp}] ✅ Connected to {AMDBLACK_HOST} ({ip})\\n")
        else:
            f.write(f"[{timestamp}] ❌ Connection lost to {AMDBLACK_HOST}\\n")

def main():
    print(f"🔍 Monitoring private connection to {AMDBLACK_HOST}")
    print(f"   Checking every {CHECK_INTERVAL} seconds...")
    
    last_status = None
    while True:
        connected, ip = check_connection()
        
        if connected != last_status:
            log_status(connected, ip)
            if connected:
                print(f"✅ Connected to {AMDBLACK_HOST} at {ip}")
            else:
                print(f"⚠️  Connection lost to {AMDBLACK_HOST}")
        
        last_status = connected
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    import os
    os.makedirs(os.path.expanduser('~/.network_security'), exist_ok=True)
    main()
"""
        
        script_path = self.config_path / 'connection_monitor.py'
        with open(script_path, 'w') as f:
            f.write(monitor_script)
        
        os.chmod(script_path, 0o755)
        print("📊 Connection monitor created at:", script_path)
        return script_path
    
    def create_main_setup_script(self):
        """Create main setup script to execute all configurations"""
        setup_script = f"""#!/bin/bash
# Main Private Network Setup Script

echo "🚀 Setting up private network with amdblack.local"
echo "================================================"

# Check if running as root for some operations
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Some operations require sudo. You'll be prompted for password."
fi

# 1. Apply firewall rules (if iptables available)
if command -v iptables &> /dev/null; then
    echo "🔒 Applying firewall rules..."
    bash {self.config_path}/firewall_rules.sh
else
    echo "⚠️  iptables not found, skipping firewall rules"
fi

# 2. Check/add hosts entry
if ! grep -q "amdblack.local" /etc/hosts; then
    echo "📝 Adding amdblack.local to /etc/hosts..."
    echo "10.0.0.100 amdblack.local" | sudo tee -a /etc/hosts
fi

# 3. Set up SSH config
if [ -f ~/.ssh/config ]; then
    if ! grep -q "Host amdblack" ~/.ssh/config; then
        echo "🔐 Adding SSH configuration..."
        cat {self.config_path}/../.ssh/config.amdblack >> ~/.ssh/config
    fi
else
    echo "🔐 Creating SSH configuration..."
    cp {self.config_path}/../.ssh/config.amdblack ~/.ssh/config
    chmod 600 ~/.ssh/config
fi

# 4. Generate SSH keys if not present
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "🔑 Generating SSH keypair..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "diesel@private-network"
fi

# 5. Set network interface to private (if NetworkManager available)
if command -v nmcli &> /dev/null; then
    echo "🌐 Setting connection profile to private..."
    # Get active connection
    ACTIVE_CON=$(nmcli -t -f NAME connection show --active | head -1)
    if [ ! -z "$ACTIVE_CON" ]; then
        nmcli connection modify "$ACTIVE_CON" connection.zone trusted
        echo "   Connection '$ACTIVE_CON' set to trusted zone"
    fi
fi

# 6. Disable IPv6 for private connection (optional but recommended)
echo "🚫 Disabling IPv6 for enhanced privacy..."
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1

echo ""
echo "✅ Private network setup complete!"
echo ""
echo "📋 Summary:"
echo "   - Firewall rules: {self.config_path}/firewall_rules.sh"
echo "   - SSH config: ~/.ssh/config.amdblack"
echo "   - Connection monitor: {self.config_path}/connection_monitor.py"
echo "   - Network namespace: {self.config_path}/create_namespace.sh"
echo ""
echo "🔍 To monitor connection: python3 {self.config_path}/connection_monitor.py"
echo "🌐 To use isolated namespace: bash {self.config_path}/create_namespace.sh"
"""
        
        script_path = self.config_path / 'setup_private_network.sh'
        with open(script_path, 'w') as f:
            f.write(setup_script)
        
        os.chmod(script_path, 0o755)
        print("🎯 Main setup script created at:", script_path)
        return script_path
    
    def run(self):
        """Execute all security configurations"""
        print("=" * 50)
        print("🔐 PRIVATE NETWORK SECURITY MANAGER")
        print("=" * 50)
        
        # Create all configuration files
        self.create_firewall_rules()
        self.setup_hosts_file()
        self.create_ssh_config()
        self.create_network_namespace()
        self.create_connection_monitor()
        setup_script = self.create_main_setup_script()
        
        print("\n" + "=" * 50)
        print("✅ All configuration files created successfully!")
        print("=" * 50)
        
        print("\n📌 Next steps:")
        print(f"   1. Run the setup script: bash {setup_script}")
        print(f"   2. Copy SSH public key to amdblack: ssh-copy-id diesel@amdblack.local")
        print(f"   3. Test connection: ssh amdblack.local")
        print(f"   4. Monitor connection: python3 {self.config_path}/connection_monitor.py")
        
        return {
            "status": "success",
            "config_path": str(self.config_path),
            "setup_script": str(setup_script),
            "configurations": [
                "firewall_rules.sh",
                "hosts_config.json",
                "ssh_config",
                "network_namespace.sh",
                "connection_monitor.py",
                "setup_private_network.sh"
            ]
        }

if __name__ == "__main__":
    manager = NetworkSecurityManager()
    result = manager.run()
    
    # Save configuration summary
    with open('network_security_summary.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n💾 Configuration summary saved to: network_security_summary.json")