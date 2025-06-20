# 🌙 Nightreign Launcher - Changelog

---

## [1.01.03] - 2024-12-19

### ✨ New Features & Improvements

#### 🎮 **Enhanced FPS Unlock System**
- **Completely redesigned FPS unlock functionality**
- Now copies all files from "fps unlock" folder directly to game directory
- No more separate executable - integrated directly into launcher
- Includes `dinput8.dll`, `mod_loader_config.ini`, and mods folder
- **Removes 60 FPS cap instantly** with one click

#### ⚡ **Performance Mode**
- **New performance settings** in Game Settings dialog
- Apply "No Grass & Shadows" settings with one click
- Disables grass rendering and shadow effects for better performance
- Perfect for lower-end systems or competitive play

#### 🎯 **Fresh Install Support**
- **Fixed game folder detection** for new installations
- Now validates using `nightreign.exe` instead of `nrsc_launcher.exe`
- Users can select game folder even before patching
- **Clear guidance** when `nrsc_launcher.exe` is missing
- No more confusing red "Select Folder" button for valid installations

### 🔧 **UI & UX Improvements**

#### 🎨 **Streamlined Interface**
- **Removed player count buttons** - simplified interface
- No more unnecessary player count selection
- Cleaner, more focused UI design

#### 🛡️ **Reduced User Anxiety**
- **Removed alarming antivirus warning popup**
- Added gentle antivirus tips in welcome message instead
- Less intimidating first-time experience
- Still provides helpful guidance when needed

#### 📝 **Better User Guidance**
- **Enhanced welcome dialog** with contextual messages
- Different guidance for patched vs unpatched games
- Clear step-by-step instructions for new users
- Restart reminder after patching

### 🔄 **Mod System Improvements**

#### 🎯 **Simplified Reset Function**
- **"Reset to Normal" now uses launcher's regulation.bin**
- No dependency on backup files
- Uses same regulation.bin as online patch (the default)
- More reliable and consistent behavior

#### 🎯 **Better Mod Management**
- Direct copy from launcher folder to game folder
- Consistent with other launcher operations
- Improved error handling and user feedback

### 🐛 **Bug Fixes**

#### 🎯 **Game Folder Detection**
- Fixed validation logic for clean installations
- Proper handling of both patched and unpatched games
- Better error messages and user guidance

#### 🔧 **File Operations**
- Improved error handling in file copy operations
- Better feedback when operations fail
- More reliable file management

### 📋 **Technical Improvements**

#### 🧹 **Code Cleanup**
- Removed unused player count logic
- Simplified game folder validation
- Better separation of concerns
- More maintainable codebase

#### 🔧 **Error Handling**
- Enhanced error messages throughout
- Better user guidance for common issues
- More informative status updates

---

## [1.01.02] - 2024-12-XX

### 🔧 **Previous Version Features**
- **Launch Game** - Start with admin privileges
- **Update Game** - Download and install latest version
- **Patch Game** - Install required online files
- **Verify Files** - Check game structure and Steam status
- **Controller Fix** - Install Steam controller configurations
- **Backup Saves** - Create backups of your save files
- **Game Settings** - Apply mods, performance settings, and FPS unlock
- **Custom Themes** - Multiple color themes available
- **Folder Management** - Easy game and Steam directory selection

### 🎯 **Core Features**
- Welcome screen on first launch
- Patch notes/version history
- Troubleshooting feature
- Steam folder selection in settings
- Improved update process handling
- Automatic regulation file moving after updates
- Resizable window
- Various bug fixes and stability improvements

---

## [1.01.01] - 2024-12-XX

### 🎯 **Initial Release Features**
- Basic launcher functionality
- Game folder selection
- Simple update system
- Core game management features

---

## 🔄 **Update System**

### **Version 1.01.03+**
- Automatic update checking
- Incremental file updates
- Backup and rollback capabilities
- Progress tracking and error recovery

### **Previous Versions**
- Manual updates via zip files
- Full reinstallation required

---

## 📋 **File Requirements**

### **Required Files (v1.01.03)**
- `launcher.exe` - Main launcher executable
- `online_patch/` - Game patching files
- `templates/` - Steam controller templates
- `fps unlock/` - FPS unlocker files
- `nograssnoshadows/` - Performance settings
- `regulation.bin` - Game regulation file
- `update.exe` - Game updater
- `game_actions_480.vdf` - Steam controller configuration

### **Optional Files**
- `mods/` - Game modification files
- `fps_unlocker_config.json` - FPS unlocker configuration
- `launcher_config.ini` - Launcher configuration

---

## 🤝 **Support**

- **Discord:** [Join our community](https://discord.gg/YDtHQNqnqj)
- **Issues:** Report bugs on GitHub
- **Contributions:** Pull requests welcome

---

## ⚠️ **Important Notes**

### **Breaking Changes**
- Player count selection removed in v1.01.03
- Antivirus warning popup removed in v1.01.03
- Game folder validation logic changed in v1.01.03

### **Migration Guide**
- Users upgrading from v1.01.02: No action required
- Users upgrading from v1.01.01: Minor updates recommended
- Users upgrading from v1.00.xx or earlier: Full reinstall recommended

---

## 👨‍💻 **Credits**

**Built with ❤️ by po1sontre**

---

*For detailed installation instructions, see the README.md file.* 