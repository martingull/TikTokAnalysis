import argparse
import hashlib
import json
from collections import defaultdict
from androguard.misc import AnalyzeAPK
from androguard.util import get_certificate_name_string

try:
    from loguru import logger as loguru_logger
except ImportError:
    loguru_logger = None

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
        "Landroid/location/LocationManager;->getLastKnownLocation",
        "Landroid/telephony/TelephonyManager;->getDeviceId",
        "Landroid/telephony/TelephonyManager;->getSubscriberId",
        "Landroid/telephony/TelephonyManager;->getSimSerialNumber",
        "Landroid/accounts/AccountManager;->getAccounts",
        "Landroid/content/pm/PackageManager;->getInstalledPackages",
        "Landroid/net/wifi/WifiInfo;->getMacAddress",
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
    "android.permission.READ_CONTACTS": ["Landroid/accounts/AccountManager;->getAccounts"],
    "android.permission.QUERY_ALL_PACKAGES": ["Landroid/content/pm/PackageManager;->getInstalledPackages"],
}

def detect_suspicious_calls(dx):
    findings = {category: [] for category in SUSPICIOUS_APIS}
    for method in dx.get_methods():
        full_method = method.get_method().get_class_name() + "->" + method.get_method().get_name()
        for category, apis in SUSPICIOUS_APIS.items():
            if any(api in full_method for api in apis):
                findings[category].append(full_method)
    return {category: sorted(set(methods)) for category, methods in findings.items()}


def android_attr(elem, name):
    return elem.attrib.get(f"{{http://schemas.android.com/apk/res/android}}{name}")


def local_name(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag


def detect_exported_components(a):
    exported = []
    manifest = a.get_android_manifest_xml()

    for elem in manifest.iter():
        component_type = local_name(elem.tag)
        if component_type in ["activity", "service", "receiver", "provider"]:
            name = android_attr(elem, "name")
            exported_attr = android_attr(elem, "exported")

            if exported_attr == "true" and name:
                exported.append(f"{component_type}: {name}")

    return sorted(set(exported))

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

def isoformat(value):
    native = getattr(value, "native", value)
    return native.isoformat() if hasattr(native, "isoformat") else str(native)


def certificate_record(cert):
    der = cert.dump()
    return {
        "subject": get_certificate_name_string(cert.subject, short=True),
        "issuer": get_certificate_name_string(cert.issuer, short=True),
        "serial_number": str(cert.serial_number),
        "not_valid_before": isoformat(cert.not_valid_before),
        "not_valid_after": isoformat(cert.not_valid_after),
        "sha1": hashlib.sha1(der).hexdigest(),
        "sha256": hashlib.sha256(der).hexdigest(),
        "signature_algorithm": cert.signature_algo,
    }


def extract_certificate(a):
    cert_info = {
        "is_signed": a.is_signed(),
        "is_signed_v1": a.is_signed_v1(),
        "is_signed_v2": a.is_signed_v2(),
        "is_signed_v3": a.is_signed_v3(),
        "signature_names": a.get_signature_names(),
        "certificates": [],
    }
    if a.is_signed():
        cert_info["certificates"] = [certificate_record(cert) for cert in a.get_certificates()]

    # Legacy keys keep old dashboard/report consumers working while the normalized
    # keys above become the preferred schema.
    cert_info["Is signed"] = cert_info["is_signed"]
    cert_info["Signatures"] = [
        cert["sha256"] for cert in cert_info["certificates"]
    ]
    return cert_info

def map_permissions(dx, declared_permissions=None):
    declared = set(declared_permissions or [])
    results = defaultdict(list)
    for method in dx.get_methods():
        full_method = method.get_method().get_class_name() + "->" + method.get_method().get_name()
        for perm, apis in PERMISSION_API_MAP.items():
            if any(api in full_method for api in apis):
                results[perm].append(full_method)
    return {
        perm: {
            "declared": perm in declared,
            "references": sorted(set(methods)),
        }
        for perm, methods in results.items()
    }


def component_counts(metadata):
    return {
        "permissions": len(metadata.get("Permissions", [])),
        "activities": len(metadata.get("Activities", [])),
        "services": len(metadata.get("Services", [])),
        "broadcast_receivers": len(metadata.get("Broadcast Receivers", [])),
        "content_providers": len(metadata.get("Content Providers", [])),
    }

def main():
    parser = argparse.ArgumentParser(description="Static Android APK analyzer using Androguard")
    parser.add_argument("apk", help="Path to the APK file")
    parser.add_argument("-o", "--output", help="Output report file (JSON)", default="apk_analysis_report.json")
    parser.add_argument("--verbose", action="store_true", help="Keep verbose Androguard logging enabled")
    args = parser.parse_args()

    if not args.verbose and loguru_logger is not None:
        loguru_logger.remove()

    print("[*] Loading APK and analyzing...")
    a, d, dx = AnalyzeAPK(args.apk)

    print("[*] Extracting certificate and metadata...")
    cert_info = extract_certificate(a)
    metadata = extract_metadata(a)

    print("[*] Detecting suspicious API calls...")
    suspicious = detect_suspicious_calls(dx)

    print("[*] Mapping API usage to permissions...")
    permission_map = map_permissions(dx, metadata.get("Permissions", []))

    print("[*] Checking exported components...")
    exported = detect_exported_components(a)

    full_report = {
        "analysis_schema_version": 1,
        "apk_path": args.apk,
        "app_name": metadata.get("App Name"),
        "package_name": metadata.get("Package Name"),
        "version_name": metadata.get("Version Name"),
        "version_code": metadata.get("Version Code"),
        "permissions": metadata.get("Permissions", []),
        "component_counts": component_counts(metadata),
        "certificate_info": cert_info,
        "metadata": metadata,
        "suspicious_behavior": suspicious,
        "permission_api_map": permission_map,
        "exported_components": exported,
        "evidence_model": {
            "declared_permission": "Permission appears in AndroidManifest.xml; this is capability evidence, not proof of runtime collection.",
            "static_api_reference": "API reference appears in bytecode; this is code-presence evidence, not proof a user flow triggers it.",
            "exported_component": "Component is declared exported in the manifest and may be callable by other apps subject to Android rules and app-side checks."
        },
    }

    with open(args.output, "w") as f:
        json.dump(full_report, f, indent=4)
    print(f"\nFull APK report saved to: {args.output}")

if __name__ == "__main__":
    main()
