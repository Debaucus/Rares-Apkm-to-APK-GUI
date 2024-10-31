
# Rare's APKM to APK GUI Tool

A GUI tool to simplify the installation of `.apkm` and `.apk` files on Android devices using ADB. This application allows users to install multiple APK files across multiple devices, with options for extracting `.apkm` files, saving APKs to a folder, and updating installations.

## Features
- **APKM Extraction**: Extracts `.apkm` files into their individual APK components.
- **Multi-Device Support**: Allows installation on multiple connected devices.
- **Save APK Option**: Saves extracted APK files to a specified output folder.
- **Automatic Retry with Forced Install**: Attempts a regular installation first, then retries with force if any errors occur.

---

## Installation

### Requirements
- Python 3.x
- ADB (Android Debug Bridge) installed and added to your system PATH.
- Android device(s) connected via USB or network.

### Step 1: Clone the Repository
Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/Rares-APKM-to-APK-GUI-Tool.git
cd Rares-APKM-to-APK-GUI-Tool
```

### Step 2: Set Up a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment.

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Mac/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Requirements
Install any required packages.

```bash
pip install -r requirements.txt
```

> **Note**: Most dependencies are standard libraries. Only additional installations will be made if required.

---

## Usage

1. **Run the Application**
   ```bash
   python main.py
   ```

2. **Load APKM/APK Files**  
   - Click on **Load APKM or APK Files** and select one or multiple `.apkm` or `.apk` files.

3. **Select Devices**
   - If multiple devices are connected, select the target devices for installation. You can choose **Select All** to install on all available devices.

4. **Save APK to Output Folder (Optional)**
   - Enable this option if you want the extracted APK files saved to an `output` folder.

5. **Install APKs**
   - Click **Install APKs**. The tool will attempt a normal install first; if it fails, it retries with force update enabled.

6. **View Logs**
   - Check the verbose log window for detailed messages about the installation progress and any errors.

---

## Known Issues
- If ADB is not set up correctly, the tool will not detect connected devices. Ensure that ADB is installed and accessible from the command line.
