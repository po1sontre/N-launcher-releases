import os
import hashlib
import json
from pathlib import Path

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def calculate_folder_hash(folder_path):
    """Calculate hash for entire folder by hashing all files"""
    hash_sha256 = hashlib.sha256()
    
    for root, dirs, files in os.walk(folder_path):
        # Sort for consistent hashing
        dirs.sort()
        files.sort()
        
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
    
    return hash_sha256.hexdigest()

def generate_checksums():
    """Generate checksums for all files and folders"""
    checksums = {}
    
    # Files to check
    files_to_check = [
        "launcher.exe",
        "regulation.bin", 
        "update.exe",
        "game_actions_480.vdf",
        "fps_unlocker_config.json",
        "launcher_config.ini"
    ]
    
    # Folders to check
    folders_to_check = [
        "online_patch",
        "templates", 
        "fps unlock",
        "nograssnoshadows",
        "mods"
    ]
    
    print("Generating checksums for Nightreign Launcher v1.01.03...")
    print("=" * 50)
    
    # Check files
    for file_name in files_to_check:
        if os.path.exists(file_name):
            file_hash = calculate_file_hash(file_name)
            file_size = os.path.getsize(file_name)
            checksums[file_name] = {
                "hash": file_hash,
                "size": file_size,
                "type": "file"
            }
            print(f"✓ {file_name}: {file_hash[:16]}... ({file_size:,} bytes)")
        else:
            print(f"✗ {file_name}: Not found")
    
    # Check folders
    for folder_name in folders_to_check:
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            folder_hash = calculate_folder_hash(folder_name)
            checksums[folder_name] = {
                "hash": folder_hash,
                "type": "folder"
            }
            print(f"✓ {folder_name}/: {folder_hash[:16]}...")
        else:
            print(f"✗ {folder_name}/: Not found")
    
    # Save to checksums.json
    with open("checksums.json", "w") as f:
        json.dump(checksums, f, indent=2)
    
    print("=" * 50)
    print(f"✅ Checksums saved to checksums.json")
    print(f"📊 Total files/folders processed: {len(checksums)}")
    return checksums

if __name__ == "__main__":
    generate_checksums() 