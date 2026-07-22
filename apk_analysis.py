import argparse
import json
import os
import subprocess
import xml.etree.ElementTree as ET

# Keywords to look for in smali files
DATA_ACCESS_KEYWORDS = [
    'getDeviceId', 'getSubscriberId', 'getSimSerialNumber',
    'getLastKnownLocation', 'getLatitude', 'getLongitude',
    'getAccounts', 'getInstalledPackages', 'getMacAddress',
    'getAdvertisingIdInfo', 'getInputStream', 'System.loadLibrary',
    'DexClassLoader', 'PathClassLoader', 'Runtime;->exec',
    'ProcessBuilder;->start', 'SharedPreferences',
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
    parser = argparse.ArgumentParser(description="Decompile an APK with apktool and scan smali for privacy-relevant API references.")
    parser.add_argument("apk", help="Path to the APK file")
    parser.add_argument("-d", "--decompile-dir", default="apk_decompiled", help="Directory for apktool output")
    parser.add_argument("-o", "--output", default="apk_code_scan.json", help="JSON output path for scan findings")
    parser.add_argument("--skip-decompile", action="store_true", help="Scan an existing decompiled directory without running apktool")
    parser.add_argument("--keyword", action="append", dest="keywords", help="Additional keyword to scan for; can be passed multiple times")
    args = parser.parse_args()

    keywords = DATA_ACCESS_KEYWORDS + (args.keywords or [])

    if not args.skip_decompile:
        run_apktool(args.apk, args.decompile_dir)
    elif not os.path.isdir(args.decompile_dir):
        raise SystemExit(f"Decompiled directory not found: {args.decompile_dir}")

    manifest_path = os.path.join(args.decompile_dir, "AndroidManifest.xml")
    permissions = parse_permissions(manifest_path)
    print("\n[+] Permissions Used:")
    for perm in permissions:
        print("  -", perm)

    findings = search_smali_code(args.decompile_dir, keywords)
    print("\n[+] Data Access Code Patterns Found:")
    for item in findings:
        print(f"  - {item['keyword']} in {item['file']} (Line {item['line']}): {item['code']}")

    report = {
        "apk_path": args.apk,
        "decompile_dir": args.decompile_dir,
        "permissions": permissions,
        "keywords": keywords,
        "finding_count": len(findings),
        "findings": findings,
    }
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nScan report saved to: {args.output}")

if __name__ == "__main__":
    main()
