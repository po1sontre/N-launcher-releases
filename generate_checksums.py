import os
import hashlib
import json
from pathlib import Path

def is_valid_filename(filename):
    """Check if filename is valid for file operations"""
    # Check for invalid characters
    invalid_chars = '<>:"|?*'
    if any(char in filename for char in invalid_chars):
        return False
    
    # Check for reserved names
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                     'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                     'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    if filename.upper() in reserved_names:
        return False
    
    return True

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file"""
    try:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except (OSError, IOError) as e:
        print(f"⚠️  Warning: Could not read file {file_path}: {e}")
        return None

def calculate_folder_hash(folder_path):
    """Calculate hash for entire folder by hashing all files"""
    hash_sha256 = hashlib.sha256()
    processed_files = 0
    skipped_files = 0
    
    for root, dirs, files in os.walk(folder_path):
        # Sort for consistent hashing
        dirs.sort()
        files.sort()
        
        for file in files:
            # Skip files with invalid names
            if not is_valid_filename(file):
                print(f"⚠️  Warning: Skipping file with invalid name: {file}")
                skipped_files += 1
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
                processed_files += 1
            except (OSError, IOError) as e:
                print(f"⚠️  Warning: Could not read file {file_path}: {e}")
                skipped_files += 1
                continue
    
    if skipped_files > 0:
        print(f"📊 Folder {folder_path}: Processed {processed_files} files, skipped {skipped_files} files")
    
    return hash_sha256.hexdigest()

def generate_checksums():
    """Generate checksums for all files and folders and update version.json"""
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
            if file_hash:
                file_size = os.path.getsize(file_name)
                checksums[file_name] = {
                    "hash": file_hash,
                    "size": file_size,
                    "type": "file"
                }
                print(f"✓ {file_name}: {file_hash[:16]}... ({file_size:,} bytes)")
            else:
                print(f"✗ {file_name}: Could not calculate hash")
        else:
            print(f"✗ {file_name}: Not found")
    
    # Check folders and their contents
    for folder_name in folders_to_check:
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            # Add folder entry
            folder_hash = calculate_folder_hash(folder_name)
            if folder_hash:
                checksums[folder_name] = {
                    "hash": folder_hash,
                    "type": "folder"
                }
                print(f"✓ {folder_name}/: {folder_hash[:16]}...")
            
            # Add individual files within the folder
            for root, dirs, files in os.walk(folder_name):
                for file in files:
                    if is_valid_filename(file):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, '.')
                        
                        file_hash = calculate_file_hash(file_path)
                        if file_hash:
                            file_size = os.path.getsize(file_path)
                            checksums[relative_path] = {
                                "hash": file_hash,
                                "size": file_size,
                                "type": "file"
                            }
                            print(f"  ✓ {relative_path}: {file_hash[:16]}... ({file_size:,} bytes)")
                        else:
                            print(f"  ✗ {relative_path}: Could not calculate hash")
                    else:
                        print(f"  ⚠️  Skipping invalid filename: {file}")
            else:
                print(f"✗ {folder_name}/: Not found")
    
    # Save to checksums.json
    with open("checksums.json", "w") as f:
        json.dump(checksums, f, indent=2)
    
    print("=" * 50)
    print(f"✅ Checksums saved to checksums.json")
    print(f"📊 Total files/folders processed: {len(checksums)}")
    
    # Update version.json with hashes
    update_version_json(checksums)
    
    return checksums

def update_version_json(checksums):
    """Update version.json with the calculated hashes"""
    try:
        # Load existing version.json
        if os.path.exists("version.json"):
            with open("version.json", "r") as f:
                version_data = json.load(f)
        else:
            print("❌ version.json not found! Creating new one...")
            version_data = {
                "version": "1.01.03",
                "build_date": "2024-12-19",
                "min_required_version": "1.00.00",
                "changelog": "Enhanced FPS unlock system, performance mode, fresh install support, and improved UI",
                "files": {},
                "update_server": "https://github.com/po1sontre/N-launcher-releases",
                "download_base_url": "https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/",
                "changelog_url": "https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/changelog.md"
            }
        
        # Update files section with hashes
        files = version_data.get("files", {})
        
        # Clean up old folder entries with trailing slashes
        keys_to_remove = []
        for key in files.keys():
            if key.endswith('/') and key.rstrip('/') in checksums:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del files[key]
            print(f"🗑️  Removed old entry: {key}")
        
        for file_name, file_info in checksums.items():
            if file_name in files:
                # Update existing file info with hash
                files[file_name]["hash"] = file_info["hash"]
                if file_info["type"] == "file":
                    files[file_name]["size"] = file_info["size"]
                elif file_info["type"] == "folder":
                    files[file_name]["is_folder"] = True
                    files[file_name]["size"] = 0
            else:
                # Add new file info
                if file_info["type"] == "file":
                    # Handle files within folders
                    if '/' in file_name or '\\' in file_name:
                        # This is a file within a folder - convert backslashes to forward slashes for URL
                        url_path = file_name.replace('\\', '/')
                        files[file_name] = {
                            "hash": file_info["hash"],
                            "size": file_info["size"],
                            "url": f"https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/{url_path}",
                            "required": True
                        }
                    else:
                        # This is a root file
                        files[file_name] = {
                            "hash": file_info["hash"],
                            "size": file_info["size"],
                            "url": f"https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/{file_name}",
                            "required": True
                        }
                elif file_info["type"] == "folder":
                    url_path = file_name.replace('\\', '/')
                    files[file_name] = {
                        "hash": file_info["hash"],
                        "size": 0,
                        "url": f"https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/{url_path}/",
                        "required": True,
                        "is_folder": True
                    }
        
        version_data["files"] = files
        
        # Save updated version.json
        with open("version.json", "w") as f:
            json.dump(version_data, f, indent=2)
        
        print(f"✅ version.json updated with {len(checksums)} file hashes")
        
        # Show summary of what was updated
        print("\n📋 Files updated in version.json:")
        for file_name in checksums.keys():
            print(f"  • {file_name}")
            
    except Exception as e:
        print(f"❌ Error updating version.json: {e}")

if __name__ == "__main__":
    generate_checksums() 