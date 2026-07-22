import json
from colorama import Fore, Style, init

init(autoreset=True)  # Automatically reset color after each print

MAX_LIST_ITEMS = 20


def print_section(title, content, color=Fore.CYAN):
    print(f"\n{color}{'-' * 40}")
    print(f"{title.upper()}")
    print(f"{'-' * 40}{Style.RESET_ALL}")
    if isinstance(content, dict):
        for k, v in content.items():
            if isinstance(v, dict):
                print(f"{Fore.YELLOW}{k}:")
                for sk, sv in v.items():
                    print(f"  {Style.DIM}{sk}: {sv}")
            else:
                print(f"{Fore.YELLOW}{k}: {Style.RESET_ALL}{v}")
    elif isinstance(content, list):
        for item in content:
            print(f"- {item}")
    else:
        print(content)
    print()


def bounded_list(items, max_items=MAX_LIST_ITEMS):
    if not isinstance(items, list):
        return items
    if len(items) <= max_items:
        return items
    return items[:max_items] + [f"... {len(items) - max_items} more"]


def unique_list(items):
    if not isinstance(items, list):
        return items
    return sorted(set(items))


def normalize_report(results):
    metadata = results.get("metadata", {})
    certificate = results.get("certificate_info", {})
    certificates = certificate.get("certificates", [])
    first_certificate = certificates[0] if certificates else {}

    permissions = results.get("permissions") or metadata.get("Permissions", [])
    component_counts = results.get("component_counts") or {
        "permissions": len(permissions),
        "activities": len(metadata.get("Activities", [])),
        "services": len(metadata.get("Services", [])),
        "broadcast_receivers": len(metadata.get("Broadcast Receivers", [])),
        "content_providers": len(metadata.get("Content Providers", [])),
    }

    return {
        "metadata": {
            "APK Path": results.get("apk_path"),
            "Package": results.get("package_name") or metadata.get("Package Name"),
            "App Name": results.get("app_name") or metadata.get("App Name"),
            "Version": results.get("version_name") or metadata.get("Version Name"),
            "Version Code": results.get("version_code") or metadata.get("Version Code"),
            "Main Activity": metadata.get("Main Activity"),
            "Target SDK": metadata.get("Target SDK"),
            "Min SDK": metadata.get("Min SDK"),
        },
        "certificate": {
            "Is APK Signed?": certificate.get("is_signed", certificate.get("Is signed")),
            "V1 Signature?": certificate.get("is_signed_v1"),
            "V2 Signature?": certificate.get("is_signed_v2"),
            "V3 Signature?": certificate.get("is_signed_v3"),
            "Certificate Count": len(certificates) or len(certificate.get("Signatures", [])),
            "Subject": first_certificate.get("subject"),
            "Issuer": first_certificate.get("issuer"),
            "Valid From": first_certificate.get("not_valid_before"),
            "Valid Until": first_certificate.get("not_valid_after"),
            "SHA1": first_certificate.get("sha1") or results.get("cert_sha1"),
            "SHA256": first_certificate.get("sha256") or results.get("cert_sha256"),
        },
        "component_counts": component_counts,
        "permissions": unique_list(permissions),
        "suspicious_behavior": {
            category: unique_list(methods)
            for category, methods in results.get("suspicious_behavior", {}).items()
        },
        "permission_api_map": {
            permission: {
                "declared": data.get("declared"),
                "references": unique_list(data.get("references", [])),
            }
            if isinstance(data, dict)
            else unique_list(data)
            for permission, data in results.get("permission_api_map", {}).items()
        },
        "exported_components": unique_list(results.get("exported_components", [])),
        "evidence_model": results.get("evidence_model", {}),
    }


def render_dashboard(results):
    normalized = normalize_report(results)

    # 1. Basic Info
    print_section("App Metadata", normalized["metadata"])

    # 2. Certificate Info
    print_section("Certificate and Signing Info", normalized["certificate"], color=Fore.MAGENTA)

    # 3. Component counts
    print_section("Component Counts", normalized["component_counts"], color=Fore.GREEN)

    # 4. Permissions
    print_section("Permissions", bounded_list(normalized["permissions"]), color=Fore.YELLOW)

    # 5. Static behavior signals
    if normalized["suspicious_behavior"]:
        suspicious_summary = {
            category: bounded_list(methods)
            for category, methods in normalized["suspicious_behavior"].items()
        }
        print_section("Static API Signals", suspicious_summary, color=Fore.RED)

    if normalized["permission_api_map"]:
        api_map = {}
        for permission, data in normalized["permission_api_map"].items():
            if isinstance(data, dict):
                declared = "declared" if data.get("declared") else "not declared"
                api_map[f"{permission} ({declared})"] = bounded_list(data.get("references", []))
            else:
                api_map[permission] = bounded_list(data)
        print_section("Permission API Map", api_map, color=Fore.BLUE)

    if normalized["exported_components"]:
        print_section("Exported Components", bounded_list(normalized["exported_components"]), color=Fore.CYAN)

    if normalized["evidence_model"]:
        print_section("Evidence Model", normalized["evidence_model"], color=Fore.LIGHTBLACK_EX)

    if "error" in results:
        print_section("Error", results["error"], color=Fore.LIGHTRED_EX)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python dashboard.py <results_json_file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        results = json.load(f)

    render_dashboard(results)
