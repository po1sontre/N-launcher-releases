import os
import hashlib
import json
import zipfile
import shutil
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

def create_folder_zip(folder_name):
    """Create a ZIP file for a folder and return its hash"""
    zip_filename = f"{folder_name.replace('/', '_').replace('\\', '_')}.zip"
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_name):
                for file in files:
                    if is_valid_filename(file):
                        file_path = os.path.join(root, file)
                        # Use relative path within the ZIP
                        arcname = os.path.relpath(file_path, folder_name)
                        zipf.write(file_path, arcname)
        
        # Calculate hash of the ZIP file
        zip_hash = calculate_file_hash(zip_filename)
        zip_size = os.path.getsize(zip_filename)
        
        print(f"✓ Created {zip_filename}: {zip_hash[:16]}... ({zip_size:,} bytes)")
        return zip_filename, zip_hash, zip_size
        
    except Exception as e:
        print(f"✗ Failed to create ZIP for {folder_name}: {e}")
        return None, None, None

def generate_checksums():
    """Generate checksums for all files and folders and update version.json"""
    checksums = {}
    
    # Individual files to check (not in folders)
    individual_files = [
        "launcher.exe",
        "regulation.bin", 
        "update.exe",
        "game_actions_480.vdf",
        "fps_unlocker_config.json",
        "launcher_config.ini"
    ]
    
    # Folders to create ZIP files for
    folders_to_zip = [
        "online_patch",
        "templates", 
        "fps unlock",
        "nograssnoshadows",
        "mods"
    ]
    
    print("Generating checksums for Nightreign Launcher v1.01.03...")
    print("Using ZIP-based folder downloads for better efficiency")
    print("=" * 60)
    
    # Process individual files
    print("\n📄 Processing individual files:")
    for file_name in individual_files:
        if os.path.exists(file_name):
            file_hash = calculate_file_hash(file_name)
            if file_hash:
                file_size = os.path.getsize(file_name)
                checksums[file_name] = {
                    "hash": file_hash,
                    "size": file_size,
                    "url": f"https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/{file_name}",
                    "required": True
                }
                print(f"✓ {file_name}: {file_hash[:16]}... ({file_size:,} bytes)")
            else:
                print(f"✗ {file_name}: Could not calculate hash")
        else:
            print(f"✗ {file_name}: Not found")
    
    # Process folders by creating ZIP files
    print("\n📦 Creating ZIP files for folders:")
    for folder_name in folders_to_zip:
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            zip_filename, zip_hash, zip_size = create_folder_zip(folder_name)
            
            if zip_filename and zip_hash:
                # Add the folder as a ZIP download
                checksums[folder_name] = {
                    "hash": zip_hash,
                    "size": zip_size,
                    "url": f"https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/{zip_filename}",
                    "required": True,
                    "is_folder": True,
                    "zip_file": zip_filename
                }
                print(f"✓ {folder_name}/: Will be downloaded as {zip_filename}")
            else:
                print(f"✗ {folder_name}/: Failed to create ZIP")
        else:
            print(f"✗ {folder_name}/: Not found")
    
    # Save to checksums.json
    with open("checksums.json", "w") as f:
        json.dump(checksums, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ Checksums saved to checksums.json")
    print(f"📊 Total files/folders processed: {len(checksums)}")
    
    # Update version.json with new structure
    update_version_json(checksums)
    
    return checksums

def update_version_json(checksums):
    """Update version.json with the calculated hashes and ZIP structure"""
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
                "changelog": "Enhanced FPS unlock system, performance mode, fresh install support, and improved UI. Now uses ZIP-based downloads for better efficiency.",
                "files": {},
                "update_server": "https://github.com/po1sontre/N-launcher-releases",
                "download_base_url": "https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/",
                "changelog_url": "https://raw.githubusercontent.com/po1sontre/N-launcher-releases/refs/heads/main/changelog.md"
            }
        
        # Clean up the files section completely
        print("🧹 Cleaning up version.json to remove duplicates...")
        old_files_count = len(version_data.get("files", {}))
        version_data["files"] = {}
        
        # Add all entries from checksums
        for file_name, file_info in checksums.items():
            version_data["files"][file_name] = {
                "hash": file_info["hash"],
                "size": file_info["size"],
                "url": file_info["url"],
                "required": file_info.get("required", True)
            }
            
            # Add is_folder flag for folders
            if file_info.get("is_folder"):
                version_data["files"][file_name]["is_folder"] = True
        
        # Save updated version.json
        with open("version.json", "w") as f:
            json.dump(version_data, f, indent=2)
        
        new_files_count = len(version_data["files"])
        print(f"✅ version.json cleaned and updated!")
        print(f"📊 Removed {old_files_count} old entries, added {new_files_count} clean entries")
        
        # Show summary of what was updated
        print("\n📋 Files in version.json:")
        individual_files = 0
        folder_zips = 0
        
        for file_name in sorted(version_data["files"].keys()):
            file_info = version_data["files"][file_name]
            if file_info.get("is_folder"):
                print(f"  📦 {file_name}/ (ZIP download)")
                folder_zips += 1
            else:
                print(f"  📄 {file_name}")
                individual_files += 1
        
        print(f"\n📊 Summary: {individual_files} individual files, {folder_zips} folder ZIPs")
        
        # List created ZIP files
        print("\n📦 Created ZIP files:")
        for file_name, file_info in checksums.items():
            if file_info.get("is_folder"):
                zip_file = file_info.get("zip_file", f"{file_name.replace('/', '_').replace('\\', '_')}.zip")
                print(f"  ✓ {zip_file}")
            
    except Exception as e:
        print(f"❌ Error updating version.json: {e}")

def cleanup_temp_zips():
    """Clean up temporary ZIP files after processing"""
    print("\n🧹 Cleaning up temporary ZIP files...")
    
    folders_to_zip = [
        "online_patch",
        "templates", 
        "fps unlock",
        "nograssnoshadows",
        "mods"
    ]
    
    for folder_name in folders_to_zip:
        zip_filename = f"{folder_name.replace('/', '_').replace('\\', '_')}.zip"
        if os.path.exists(zip_filename):
            try:
                os.remove(zip_filename)
                print(f"✓ Removed {zip_filename}")
            except Exception as e:
                print(f"⚠️  Could not remove {zip_filename}: {e}")

if __name__ == "__main__":
    generate_checksums()
    
    # Always keep ZIP files for repository upload
    print("\n" + "=" * 60)
    print("✅ ZIP files kept for repository upload.")
    print("📦 Ready to commit and push to releases repo!") 