#!/usr/bin/env python3
"""
Script untuk mengupdate URL IPA di semua file plist
agar mengarah ke GitHub raw URL
"""

import os
import re
from pathlib import Path

# GitHub repository configuration
GITHUB_REPO = "xyzarco/plist"
GITHUB_BRANCH = "main"
GITHUB_BASE_URL = f"https://github.com/{GITHUB_REPO}/raw/refs/heads/{GITHUB_BRANCH}"

def update_plist_url(plist_path, app_type):
    """
    Update IPA URL in plist file to point to GitHub raw URL
    
    Args:
        plist_path: Path to plist file
        app_type: 'ksign' or 'esign'
    """
    
    # Read plist file
    with open(plist_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get filename without extension
    filename = os.path.basename(plist_path)
    base_name = filename.replace('.plist', '')
    
    # Construct IPA filename (same as plist but with .ipa extension)
    ipa_filename = f"{base_name}.ipa"
    
    # Construct GitHub raw URL
    github_url = f"{GITHUB_BASE_URL}/old/ipa_files/{app_type}/{ipa_filename}"
    
    # Find and replace the URL in plist
    # Pattern: <string>https://download.khoindvn.io.vn/iPA/xxxxx.ipa</string>
    pattern = r'<string>https://download\.khoindvn\.(io\.vn|eu\.org)/iPA/[^<]+\.ipa</string>'
    replacement = f'<string>{github_url}</string>'
    
    # Check if pattern exists
    if re.search(pattern, content):
        # Replace the URL
        new_content = re.sub(pattern, replacement, content)
        
        # Write back to file
        with open(plist_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, github_url
    else:
        return False, "Pattern not found"

def main():
    # Base directory
    base_dir = Path(r"C:\Users\Wow\Documents\plist\old\plist_files")
    
    print("=" * 80)
    print("PLIST URL UPDATER - GitHub Raw URLs")
    print("=" * 80)
    print(f"GitHub Repository: {GITHUB_REPO}")
    print(f"Branch: {GITHUB_BRANCH}")
    print(f"Base URL: {GITHUB_BASE_URL}")
    print("=" * 80)
    print()
    
    # Statistics
    total_files = 0
    success_count = 0
    failed_count = 0
    
    # Process KSign plists
    ksign_dir = base_dir / "ksign"
    if ksign_dir.exists():
        ksign_files = list(ksign_dir.glob("*.plist"))
        print(f"📦 Processing {len(ksign_files)} KSign plist files...")
        print("-" * 80)
        
        for plist_file in sorted(ksign_files):
            total_files += 1
            filename = plist_file.name
            
            success, result = update_plist_url(plist_file, "ksign")
            
            if success:
                print(f"✓ {filename}")
                print(f"  → {result}")
                success_count += 1
            else:
                print(f"✗ {filename}")
                print(f"  → Error: {result}")
                failed_count += 1
        
        print()
    
    # Process ESign plists
    esign_dir = base_dir / "esign"
    if esign_dir.exists():
        esign_files = list(esign_dir.glob("*.plist"))
        print(f"📦 Processing {len(esign_files)} ESign plist files...")
        print("-" * 80)
        
        for plist_file in sorted(esign_files):
            total_files += 1
            filename = plist_file.name
            
            success, result = update_plist_url(plist_file, "esign")
            
            if success:
                print(f"✓ {filename}")
                print(f"  → {result}")
                success_count += 1
            else:
                print(f"✗ {filename}")
                print(f"  → Error: {result}")
                failed_count += 1
        
        print()
    
    # Summary
    print("=" * 80)
    print("UPDATE COMPLETE!")
    print("=" * 80)
    print(f"Total files processed: {total_files}")
    print(f"✓ Successfully updated: {success_count}")
    print(f"✗ Failed: {failed_count}")
    print("=" * 80)
    
    if success_count > 0:
        print()
        print("✅ All plist files now point to GitHub raw URLs!")
        print(f"   Format: {GITHUB_BASE_URL}/old/ipa_files/[type]/[filename].ipa")

if __name__ == "__main__":
    main()
