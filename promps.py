
PRIVACY_PROMPT = """

When performing a privacy and security analysis on a reversed-engineered APK file, you're essentially looking for clues about how the app handles sensitive data, interacts with the device, and potentially communicates with external servers. Here's a comprehensive list of things to look for:

**I. Data Handling and Storage:**

* **Sensitive Data in Plaintext:**
    * **Hardcoded API Keys/Credentials:** Look for strings that resemble API keys, usernames, passwords, or tokens directly embedded in the code, especially in `strings.xml`, Java code, or native libraries.
    * **Personal Identifiable Information (PII):** Search for email addresses, phone numbers, addresses, social security numbers, or other sensitive data being stored without encryption.
    * **Financial Data:** Credit card numbers, bank account details, payment gateway credentials.
* **Local Storage Mechanisms:**
    * **SharedPreferences:** Check for sensitive data stored in `SharedPreferences` without encryption. These are easily accessible.
    * **Internal/External Storage:** Analyze if the app writes sensitive files (e.g., databases, logs, temporary files) to internal or external storage without proper encryption and access controls.
    * **SQLite Databases:** Examine SQLite databases (if present) for unencrypted sensitive data. Look at the database schema and contents.
* **Data Encryption:**
    * **Absence of Encryption:** Identify instances where sensitive data is handled or stored without any apparent encryption.
    * **Weak Encryption Algorithms:** If encryption is used, try to determine the algorithm. Look for outdated or known-weak algorithms (e.g., DES, RC4).
    * **Hardcoded Encryption Keys/IVs:** If encryption keys or Initialization Vectors (IVs) are hardcoded, they can be easily extracted and used to decrypt data.

**II. Permissions and Device Interaction:**

* **Dangerous Permissions:**
    * Review `AndroidManifest.xml` for declared permissions, especially those categorized as "dangerous" (e.g., `READ_CONTACTS`, `ACCESS_FINE_LOCATION`, `CAMERA`, `RECORD_AUDIO`, `READ_SMS`, `CALL_PHONE`).
    * Assess if the requested permissions are genuinely necessary for the app's stated functionality.
* **Undocumented/Unnecessary Permissions:** Look for permissions that don't seem to align with the app's purpose, which might indicate malicious intent or over-privileging.
* **Runtime Permission Requests:** Observe how and when the app requests runtime permissions. Does it prompt the user clearly, or attempt to gain permissions surreptitiously?
* **Interaction with Other Apps/Components:**
    * **Broadcast Receivers, Services, Content Providers:** Analyze how these components are exposed and if they have proper access controls (e.g., `android:exported="true"` without permission checks can be a vulnerability).
    * **Inter-Process Communication (IPC):** Look for Intents that send sensitive data to other apps or components without proper validation or protection.
* **Device Identifiers:**
    * **IMEI, Android ID, Advertising ID:** Check if the app is collecting and transmitting these identifiers, and how they are used.
    * **MAC Address:** Collection of MAC addresses is often unnecessary and can raise privacy concerns.
* **Camera/Microphone Usage:** Look for code that accesses the camera or microphone, especially if it's not immediately apparent why the app needs this functionality.

**III. Network Communication:**

* **Unencrypted Communication (HTTP):**
    * Look for network requests using `http://` instead of `https://`. This exposes data to eavesdropping.
    * Analyze network traffic for sensitive data being sent over unencrypted channels.
* **Weak TLS/SSL Implementations:**
    * **Trust All Certificates (HostnameVerifier, TrustManager):** Search for code that blindly accepts all SSL certificates, making the app vulnerable to Man-in-the-Middle (MitM) attacks.
    * **Outdated TLS Versions:** Check if the app is using older, less secure TLS versions (e.g., TLS 1.0, 1.1).
    * **Certificate Pinning:** The absence of certificate pinning (where the app only trusts specific server certificates) can be a security weakness.
* **Sensitive Data in Network Requests/Responses:**
    * Examine network requests (URLs, headers, body) and responses for sensitive data, even if HTTPS is used.
    * Look for personally identifiable information, session tokens, passwords, or other credentials.
* **Third-Party APIs and SDKs:**
    * **Analytics SDKs:** Identify which analytics SDKs are used (e.g., Google Analytics, Firebase Analytics, Mixpanel) and what data they collect.
    * **Advertising SDKs:** Determine which ad networks are integrated and what user data they access.
    * **Social Media SDKs:** How are social media accounts linked and what permissions are requested?
    * **Data Sharing with Third Parties:** Look for explicit or implicit data sharing with third-party services that might not be transparent to the user.
* **Command and Control (C2) Communication:** In malicious APKs, look for patterns of communication with suspicious IP addresses or domains, often involving encrypted or obfuscated data.

**IV. Code Obfuscation and Tampering Detection:**

* **Obfuscation Techniques:**
    * **ProGuard/DexGuard:** Identify if the code has been obfuscated. While not a security vulnerability in itself, it makes analysis harder.
    * **String Encryption/Obfuscation:** Look for methods used to encrypt or obfuscate strings, especially those containing sensitive information (e.g., URLs, API keys).
* **Anti-Tampering/Anti-Reversing Measures:**
    * **Root Detection:** Code that checks if the device is rooted and potentially alters behavior.
    * **Debugger Detection:** Code that detects if a debugger is attached.
    * **Emulator Detection:** Code that detects if the app is running on an emulator.
    * **Integrity Checks:** Code that verifies the integrity of the APK file or its components to detect modifications.

**V. Logs and Debugging Information:**

* **Excessive Logging:** Look for `Log.d()`, `Log.v()`, `Log.i()`, etc., that print sensitive data to Logcat, which can be accessed by other apps with `READ_LOGS` permission.
* **Debuggable Flag:** Check if `android:debuggable="true"` is set in `AndroidManifest.xml` in a production build, as this can expose the app to debugging tools and vulnerabilities.

**VI. Android Manifest and Resources:**

* **Content Providers:** Check if any Content Providers are exposed and whether they have appropriate permission protection.
* **Services and Broadcast Receivers:** Analyze exposed services and receivers for potential injection or unauthorized access.
* **URIs and Schemes:** Look for custom URI schemes and how they are handled, as they can be a source of vulnerabilities.

**Tools and Techniques for Analysis:**

* **Decompilers:** Jadx, Bytecode Viewer, APKTool (for decompiling resources and manifest).
* **Static Analysis Tools:** MobSF (Mobile Security Framework), Androguard, QARK.
* **Dynamic Analysis Tools:** Frida, Xposed, Magisk modules (for runtime manipulation and observation).
* **Network Proxies:** Burp Suite, OWASP ZAP (for intercepting and analyzing network traffic).
* **Text Editors/Grep:** For searching for specific strings, patterns, or regular expressions.

By systematically going through this checklist, you can identify potential privacy and security risks within a reversed-engineered APK, providing valuable insights into the app's behavior and potential vulnerabilities.

"""