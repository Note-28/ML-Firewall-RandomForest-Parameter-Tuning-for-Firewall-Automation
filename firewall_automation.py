import re
import subprocess
import os
print("File opened successfully.")
def extract_parameters(file_path):
    parameters = {
        'sttl': [], 'ct_state_ttl': [], 'rate': [], 'dload': [], 'sload': [],
        'sbytes': [], 'ct_dst_src_ltm': [], 'smean': [], 'ct_srv_dst': [], 'dbytes': []
    }
    regex_patterns = {
        'sttl': re.compile(r'sttl\s*<=?\s*([\d.]+)'),
        'ct_state_ttl': re.compile(r'ct_state_ttl\s*<=?\s*([\d.]+)'),
        'rate': re.compile(r'rate\s*<=?\s*([\d.]+)'),
        'dload': re.compile(r'dload\s*<=?\s*([\d.]+)'),
        'sload': re.compile(r'sload\s*<=?\s*([\d.]+)'),
        'sbytes': re.compile(r'sbytes\s*<=?\s*([\d.]+)'),
        'ct_dst_src_ltm': re.compile(r'ct_dst_src_ltm\s*<=?\s*([\d.]+)'),
        'smean': re.compile(r'smean\s*<=?\s*([\d.]+)'),
        'ct_srv_dst': re.compile(r'ct_srv_dst\s*<=?\s*([\d.]+)'),
        'dbytes': re.compile(r'dbytes\s*<=?\s*([\d.]+)')
    }
    try:
        with open(file_path, 'r') as file:
            for line in file:
                for param, regex in regex_patterns.items():
                    match = regex.search(line)
                    if match:
                        parameters[param].append(float(match.group(1)))
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error reading file: {str(e)}")

    return parameters
def apply_firewall_rules(params):
    try:
        subprocess.run("iptables -F 2>/dev/null", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error flushing iptables: {str(e)}")

    max_rate_limit = 1000000  
    rule_sets = [
        ('sttl', lambda x: f"iptables -A INPUT -m ttl --ttl-lt {int(x)} -j DROP"),
        ('ct_state_ttl', lambda x: f"iptables -A INPUT -m conntrack --ctstate INVALID -m ttl --ttl-eq {int(x)} -j DROP"),
        ('rate', lambda x: f"iptables -A INPUT -m limit --limit {int(x)}/second -j ACCEPT" if int(x) > 0 and int(x) <= max_rate_limit else "iptables -A INPUT -j ACCEPT"),
        ('dload', lambda x: f"iptables -A INPUT -m length --length {int(x)} -j DROP"),
        ('sload', lambda x: f"iptables -A OUTPUT -m length --length {int(x)} -j ACCEPT"),
        ('sbytes', lambda x: f"iptables -A INPUT -m length --length {int(x)} -j DROP"),
        ('ct_dst_src_ltm', lambda x: f"iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -m ttl --ttl-eq {int(x)} -j ACCEPT"),
        ('smean', lambda x: f"iptables -A INPUT -m length --length {int(x)} -j DROP"),
        ('ct_srv_dst', lambda x: f"iptables -A INPUT -m conntrack --ctstate NEW -m ttl --ttl-eq {int(x)} -j ACCEPT"),
        ('dbytes', lambda x: f"iptables -A INPUT -m length --length {int(x)} -j DROP")
    ]

    for param, command_func in rule_sets:
        for value in params[param]:
            try:
                command = command_func(value)
                if "iptables -A INPUT -m limit --limit" in command and int(value) == 0:
                    continue
                
                subprocess.run(command + " 2>/dev/null", shell=True, check=True)
                print(f"Rule applied successfully: {command}")
            except subprocess.CalledProcessError:
                pass  

# Main execution
if __name__ == "__main__":
    file_path = os.path.join('Main', 'Forest_Tree_output.txt')
    
    parameters = extract_parameters(file_path)
    if parameters:  
        apply_firewall_rules(parameters)
