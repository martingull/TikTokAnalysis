import os
import subprocess
import xml.etree.ElementTree as ET

APK_FILE = "TikTok_39.2.1_APKPure.apk"
DECOMPILE_DIR = "tiktok_decompiled"

# Keywords to look for in smali files
DATA_ACCESS_KEYWORDS = [
    'getDeviceId', 'getSubscriberId', 'getSimSerialNumber',
    'getLastKnownLocation', 'getLatitude', 'getLongitude',
    'getAccounts', 'getInstalledPackages', 'getMacAddress',
    'getAdvertisingIdInfo', 'getInputStream', 'System.loadLibrary',
]

def run_apktool(apk_file, output_dir):
    print("[*] Decompiling APK using apktool...")
    subprocess.run(["apktool", "d", apk_file, "-o", output_dir, "-f"], check=True)

def parse_permissions(manifest_path):
    print("[*] Extracting permissions from AndroidManifest.xml...")
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    permissions = []
    for elem in root.findall(".//uses-permission"):
        perm = elem.attrib.get('{http://schemas.android.com/apk/res/android}name')
        if perm:
            permissions.append(perm)
    return permissions

def search_smali_code(directory, keywords):
    print("[*] Scanning Smali code for data access patterns...")
    findings = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".smali"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for idx, line in enumerate(lines):
                        for keyword in keywords:
                            if keyword in line:
                                findings.append({
                                    "file": path,
                                    "line": idx + 1,
                                    "keyword": keyword,
                                    "code": line.strip()
                                })
    return findings

def main():
    run_apktool(APK_FILE, DECOMPILE_DIR)

    manifest_path = os.path.join(DECOMPILE_DIR, "AndroidManifest.xml")
    permissions = parse_permissions(manifest_path)
    print("\n[+] Permissions Used:")
    for perm in permissions:
        print("  -", perm)

    findings = search_smali_code(DECOMPILE_DIR, DATA_ACCESS_KEYWORDS)
    print("\n[+] Data Access Code Patterns Found:")
    for item in findings:
        print(f"  - {item['keyword']} in {item['file']} (Line {item['line']}): {item['code']}")

if __name__ == "__main__":
    main()
