import argparse
import json
from collections import defaultdict
from androguard.misc import AnalyzeAPK
from lxml import etree 

# === Suspicious API categories ===
SUSPICIOUS_APIS = {
    "Dynamic Code Loading": [
        "Ldalvik/system/DexClassLoader;-><init>",
        "Ljava/lang/reflect/Method;->invoke",
        "Ldalvik/system/PathClassLoader;-><init>"
    ],
    "SMS Abuse": [
        "Landroid/telephony/SmsManager;->sendTextMessage",
        "Landroid/content/Intent;->setAction:sendto"
    ],
    "Privacy Invasion": [
        "Landroid/hardware/Camera;->open",
        "Landroid/media/MediaRecorder;->start",
        "Landroid/location/LocationManager;->getLastKnownLocation"
    ],
    "Command Execution": [
        "Ljava/lang/Runtime;->exec",
        "Ljava/lang/ProcessBuilder;->start"
    ]
}

# === Permission to API Map ===
PERMISSION_API_MAP = {
    "android.permission.ACCESS_FINE_LOCATION": ["Landroid/location/LocationManager;->getLastKnownLocation"],
    "android.permission.CAMERA": ["Landroid/hardware/Camera;->open"],
    "android.permission.READ_SMS": ["Landroid/telephony/SmsManager;->getMessagesFromIcc"],
    "android.permission.SEND_SMS": ["Landroid/telephony/SmsManager;->sendTextMessage"],
    "android.permission.RECORD_AUDIO": ["Landroid/media/MediaRecorder;->start"],
}

def detect_suspicious_calls(dx):
    findings = {category: [] for category in SUSPICIOUS_APIS}
    for method in dx.get_methods():
        full_method = method.get_method().get_class_name() + "->" + method.get_method().get_name()
        for category, apis in SUSPICIOUS_APIS.items():
            if any(api in full_method for api in apis):
                findings[category].append(full_method)
    return findings

def detect_exported_components(a):
    exported = []

    manifest = a.get_android_manifest_xml()

    for elem in manifest.iter():
        print(elem.tag, elem.attrib)

    for elem in manifest.iter():
        # Check only for component types
        if elem.tag in ['activity', 'service', 'receiver', 'provider']:
            name = elem.attrib.get('{http://schemas.android.com/apk/res/android}name')
            exported_attr = elem.attrib.get('{http://schemas.android.com/apk/res/android}exported')

            if exported_attr == "true" and name:
                exported.append(f"{elem.tag}: {name}")

    return exported

def extract_metadata(a):
    return {
        "App Name": a.get_app_name(),
        "Package Name": a.get_package(),
        "Version Name": a.get_androidversion_name(),
        "Version Code": a.get_androidversion_code(),
        "Permissions": a.get_permissions(),
        "Activities": a.get_activities(),
        "Main Activity": a.get_main_activity(),
        "Target SDK": a.get_target_sdk_version(),
        "Min SDK": a.get_min_sdk_version(),
        "Services": a.get_services(),
        "Broadcast Receivers": a.get_receivers(),
        "Content Providers": a.get_providers()
    }

def extract_certificate(a):
    cert_info = {"Is signed": a.is_signed()}
    if a.is_signed():
        cert_info["Signatures"] = [str(s) for s in a.get_certificates()]
    return cert_info

def map_permissions(dx):
    results = defaultdict(list)
    for method in dx.get_methods():
        full_method = method.get_method().get_class_name() + "->" + method.get_method().get_name()
        for perm, apis in PERMISSION_API_MAP.items():
            if any(api in full_method for api in apis):
                results[perm].append(full_method)
    return dict(results)

def main():
    parser = argparse.ArgumentParser(description="Comprehensive APK Analyzer using Androguard")
    parser.add_argument("apk", help="Path to the APK file")
    parser.add_argument("-o", "--output", help="Output report file (JSON)", default="apk_analysis_report.json")
    args = parser.parse_args()

    print("[*] Loading APK and analyzing...")
    a, d, dx = AnalyzeAPK(args.apk)

    print("[*] Extracting certificate and metadata...")
    cert_info = extract_certificate(a)
    metadata = extract_metadata(a)

    print("[*] Detecting suspicious API calls...")
    suspicious = detect_suspicious_calls(dx)

    print("[*] Mapping API usage to permissions...")
    permission_map = map_permissions(dx)

    print("[*] Checking exported components...")
    exported = detect_exported_components(a)

    full_report = {
        "apk_path": args.apk,
        "certificate_info": cert_info,
        "metadata": metadata,
        "suspicious_behavior": suspicious,
        "permission_api_map": permission_map,
        "exported_components": exported
    }

    with open(args.output, "w") as f:
        json.dump(full_report, f, indent=4)
    print(f"\n✅ Full APK report saved to: {args.output}")

if __name__ == "__main__":
    main()
