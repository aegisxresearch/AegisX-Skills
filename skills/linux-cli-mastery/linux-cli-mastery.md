# Linux CLI Mastery

## Overview
Panduan Linux CLI: file operations, text processing, scripting, dan server management.

---

## File Operations

### Essential Commands
```bash
# Navigation
pwd                    # Print working directory
ls -la                 # List all files with details
cd /path/to/dir        # Change directory
cd ~                   # Go to home directory
cd -                   # Go to previous directory

# File manipulation
touch file.txt         # Create empty file
mkdir -p dir/subdir    # Create directory recursively
cp -r source/ dest/    # Copy directory recursively
mv old.txt new.txt     # Move/rename file
rm -rf directory/      # Remove directory (CAREFUL!)

# Find files
find . -name "*.js"    # Find files by name
find . -type f -mtime -7  # Files modified in last 7 days
locate filename        # Quick find (uses index)
```

### Permissions
```bash
# View permissions
ls -la
# -rw-r--r-- 1 user group 1234 Jan 15 10:00 file.txt
# │││ │││ │││
# │││ │││ └─ Others: read
# │││ └──── Group: read
# └─────── User: read, write

# Change permissions
chmod 755 script.sh    # rwxr-xr-x
chmod +x script.sh     # Add execute permission
chmod -R 644 directory/ # Recursive change

# Change ownership
chown user:group file.txt
chown -R user:group directory/
```

---

## Text Processing

### grep (Search)
```bash
# Basic search
grep "pattern" file.txt

# Case insensitive
grep -i "pattern" file.txt

# Recursive search
grep -r "pattern" directory/

# With context
grep -C 3 "pattern" file.txt  # 3 lines before/after

# Count matches
grep -c "pattern" file.txt

# Only filenames
grep -l "pattern" *.txt
```

### sed (Stream Editor)
```bash
# Replace text
sed 's/old/new/g' file.txt

# Replace in-place
sed -i 's/old/new/g' file.txt

# Delete lines
sed '/pattern/d' file.txt

# Insert line after pattern
sed '/pattern/a\new line' file.txt

# Extract line range
sed -n '10,20p' file.txt
```

### awk (Text Processing)
```bash
# Print specific columns
awk '{print $1, $3}' file.txt

# Custom delimiter
awk -F: '{print $1, $3}' /etc/passwd

# Pattern matching
awk '/pattern/ {print $0}' file.txt

# Calculate sum
awk '{sum += $1} END {print sum}' numbers.txt

# Count lines
awk 'END {print NR}' file.txt
```

---

## Piping & Redirection

### Pipes
```bash
# Chain commands
cat file.txt | grep "error" | sort | uniq -c | sort -rn

# Find large files
find . -type f -exec ls -lh {} \; | awk '{print $5, $9}' | sort -rh | head -10

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

### Redirection
```bash
# Output to file (overwrite)
command > file.txt

# Output to file (append)
command >> file.txt

# Redirect stderr
command 2> error.log

# Redirect both stdout and stderr
command &> all.log

# Discard output
command > /dev/null 2>&1

# Pipe stderr
command 2>&1 | grep "error"
```

---

## ️ Process Management

```bash
# List processes
ps aux
ps aux | grep nginx

# Kill process
kill PID
kill -9 PID           # Force kill
killall nginx         # Kill by name

# Background processes
command &             # Run in background
bg                    # Resume in background
fg                    # Bring to foreground
jobs                  # List background jobs

# System monitoring
top                   # Real-time process monitor
htop                  # Better top (if installed)
df -h                 # Disk usage
free -h               # Memory usage
uptime                # System uptime
```bash

---

## Network Commands

```bash
# DNS lookup
nslookup example.com
dig example.com

# Network connections
netstat -tuln         # List listening ports
ss -tuln              # Modern netstat
lsof -i :80           # What's using port 80

# HTTP requests
curl -X GET https://api.example.com
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com

# Download files
wget https://example.com/file.zip
curl -O https://example.com/file.zip

# SSH
ssh user@hostname
ssh -i key.pem user@hostname
scp file.txt user@hostname:/path/
```

---

## Bash Scripting

### Script Template
```bash
#!/bin/bash
set -euo pipefail

# Variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/var/log/myscript.log"

# Functions
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    log "ERROR: $*" >&2
    exit 1
}

# Main
main() {
    log "Starting script..."
    
    # Your code here
    
    log "Script completed successfully"
}

# Run main function
main "$@"
```

### Useful Patterns
```bash
# Check if file exists
if [[ -f "$file" ]]; then
    echo "File exists"
fi

# Loop through files
for file in *.txt; do
    echo "Processing $file"
done

# Read input
read -p "Enter your name: " name

# Conditional
if [[ "$condition" == "true" ]]; then
    echo "Yes"
else
    echo "No"
fi
```

---

## CLI Checklist

### Daily Workflow
- [ ] Use aliases for common commands
- [ ] Master pipe operators
- [ ] Use tab completion
- [ ] Learn keyboard shortcuts (Ctrl+R, Ctrl+A, Ctrl+E)

### Scripting
- [ ] Always use `set -euo pipefail`
- [ ] Quote variables: `"$variable"`
- [ ] Use `[[ ]]` instead of `[ ]`
- [ ] Add comments for complex logic

---

## References
- https://linuxcommand.org/
- https://ss64.com/bash/
- https://shellcheck.net/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
