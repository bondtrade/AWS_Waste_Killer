import sys
import argparse
import logging
from typing import Any
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# --- CONSTANTS (Hardcoded per Tiny Tool Protocol) ---
APP_NAME = "AWS_Waste_Killer"
VERSION = "0.1.0"
DEFAULT_REGION = "us-east-1"
VOLUME_STATE_FILTER = "available"
EBS_MONTHLY_COST_PER_GB = 0.10

# --- SETUP LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(APP_NAME)

def get_regions(region_arg=None):
    """Return a list of regions to scan."""
    client = boto3.client('ec2', region_name=DEFAULT_REGION)
    if region_arg:
        return [region_arg]
    try:
        response = client.describe_regions()
        return [r['RegionName'] for r in response['Regions']]
    except NoCredentialsError:
        logger.error("No AWS credentials found. Please run 'aws configure'.")
        sys.exit(1)
    except ClientError as e:
        logger.error(f"Failed to list regions: {e}")
        sys.exit(1)

def scan_region(region):
    """Scan a single region for detached volumes."""
    ec2: Any = boto3.resource('ec2', region_name=region)
    waste_found = []
    
    try:
        # Filter for 'available' (detached) volumes
        volumes = ec2.volumes.filter(
            Filters=[{'Name': 'status', 'Values': [VOLUME_STATE_FILTER]}]
        )
        
        for vol in volumes:
            cost = vol.size * EBS_MONTHLY_COST_PER_GB
            waste_found.append({
                'Region': region,
                'VolumeId': vol.id,
                'SizeGB': vol.size,
                'MonthlyCost': cost
            })
            
    except ClientError as e:
        logger.warning(f"Skipping region {region}: {e}")
        
    return waste_found

def print_report(all_waste):
    """Print the ASCII report and return total savings."""
    print("\n" + "="*80)
    print(f" {APP_NAME} v{VERSION} - DETACHED VOLUME REPORT")
    print("="*80)
    
    if not all_waste:
        print("No detached volumes found. You are saving money!")
        return 0.0

    print(f"{'Region':<15} | {'Volume ID':<22} | {'Size (GB)':<10} | {'Monthly ($)':<12}")
    print("-" * 80)
    
    total_savings = 0.0
    for item in all_waste:
        print(f"{item['Region']:<15} | {item['VolumeId']:<22} | {item['SizeGB']:<10} | ${item['MonthlyCost']:.2f}")
        total_savings += item['MonthlyCost']
        
    print("-" * 80)
    print(f"TOTAL POTENTIAL SAVINGS: ${total_savings:.2f} / month")
    print("="*80 + "\n")
    return total_savings

def delete_volumes(all_waste):
    """Delete the volumes after final confirmation."""
    confirm = input("DANGER: Type 'yes' to DELETE these volumes forever: ")
    if confirm.strip().lower() != 'yes':
        logger.info("Deletion aborted.")
        return

    for item in all_waste:
        try:
            ec2: Any = boto3.resource('ec2', region_name=item['Region'])
            vol = ec2.Volume(item['VolumeId'])
            vol.delete()
            logger.info(f"Deleted: {item['VolumeId']} ({item['Region']})")
        except ClientError as e:
            logger.error(f"Failed to delete {item['VolumeId']}: {e}")

def main():
    parser = argparse.ArgumentParser(description=f"{APP_NAME} v{VERSION} - Find & Delete Waste")
    parser.add_argument("--region", help="Scan specific region only")
    parser.add_argument("--confirm", action="store_true", help="Enable deletion mode (requires 'yes' confirmation later)")
    args = parser.parse_args()

    mode = "DELETION MODE" if args.confirm else "DRY RUN (Safe Mode)"
    logger.info(f"Starting {APP_NAME} v{VERSION}. Mode: {mode}")

    regions = get_regions(args.region)
    all_waste = []
    
    for region in regions:
        # Simple progress indicator for the user
        print(f"Scanning {region}...", end='\r', flush=True) 
        all_waste.extend(scan_region(region))
    
    print(" " * 40, end='\r') # Clear progress line
    
    total_savings = print_report(all_waste)

    if args.confirm and total_savings > 0:
        delete_volumes(all_waste)
    elif total_savings > 0:
        logger.info("Run with --confirm to enable deletion mode.")

if __name__ == "__main__":
    main()
