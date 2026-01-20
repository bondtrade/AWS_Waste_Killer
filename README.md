# AWS Waste Killer 🔪💰

**Stop bleeding money on detached EBS volumes.**

A single-file Python script to find and delete orphaned AWS EBS volumes (hard drives that aren't attached to any server but still cost you money).

**Cost:** $0 (Free & Open Source)
**Safety:** Read-Only by default. Your credentials never leave your machine.

## 🚀 Quick Start (5 Seconds)

### Option 1: Run via Curl (The Fast Way)

```bash
curl -O https://raw.githubusercontent.com/bondtrade/AWS_Waste_Killer/master/aws_waste_killer.py
python aws_waste_killer.py
```

### Option 2: Clone & Run

```bash
git clone https://github.com/bondtrade/AWS_Waste_Killer.git
cd aws-waste-killer
python aws_waste_killer.py
```

## 🛠️ Requirements

- Python 3.8+
- AWS Credentials configured (`aws configure` or `~/.aws/credentials`)
- `boto3` library:

  ```bash
  pip install boto3
  ```

## 🛡️ Safety First

- **Dry-Run by Default**: Running the script without flags ONLY lists waste. It deletes nothing.
- **Manual Confirmation**: You must type `yes` to authorize any deletion.
- **Transparency**: The code is a single file (`aws_waste_killer.py`). Audit it yourself in 30 seconds.

## 📄 Example Output

```text
================================================================================
 AWS_Waste_Killer v0.1.0 - DETACHED VOLUME REPORT
================================================================================
Region          | Volume ID              | Size (GB)  | Monthly ($) 
--------------------------------------------------------------------------------
us-east-1       | vol-0abc123456789     | 100        | $10.00      
eu-west-1       | vol-0xyz987654321     | 50         | $5.00       
--------------------------------------------------------------------------------
TOTAL POTENTIAL SAVINGS: $15.00 / month
================================================================================
```

To actually delete these volumes, run:

```bash
python aws_waste_killer.py --confirm
```

## ⚠️ Disclaimer

This tool deletes cloud resources. While it checks for the "available" (detached) state, you are responsible for your own infrastructure. **Always check the dry-run output before confirming.**
