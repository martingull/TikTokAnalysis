import json
from colorama import Fore, Style, init

init(autoreset=True)  # Automatically reset color after each print


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


def render_dashboard(results):
    # 1. Basic Info
    print_section("App Metadata", {
        "Package": results.get("package_name"),
        "App Name": results.get("app_name"),
        "Version": results.get("version_name"),
        "Version Code": results.get("version_code"),
        "File Size (bytes)": results.get("file_size_bytes"),
    })

    # 2. Certificate Info
    cert_info = {
        "Signing Type": results.get("signing_type"),
        "SHA1": results.get("cert_sha1"),
        "SHA256": results.get("cert_sha256"),
        "Is APK Signed?": results.get("is_signed"),
        "Valid Signature?": results.get("is_valid_signature"),
        "Certificate Details": results.get("certificate_details", {})
    }

    print_section("Certificate and Signing Info", cert_info, color=Fore.MAGENTA)

    # 3. DEX Info
    if "dex" in results:
        print_section("DEX Analysis", results["dex"], color=Fore.GREEN)

    # 4. Manifest Info
    if "manifest" in results:
        print_section("Manifest Analysis", results["manifest"], color=Fore.BLUE)

    # 5. Permissions
    if "permissions" in results:
        print_section("Permissions", results["permissions"], color=Fore.YELLOW)

    # 6. Network/URLs
    if "urls" in results:
        print_section("Extracted URLs", results["urls"], color=Fore.RED)

    # 7. Extras or Errors
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
