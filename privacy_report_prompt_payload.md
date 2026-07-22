## System Message

When performing a privacy and security analysis on a reversed-engineered APK file, you're essentially looking for clues about how the app handles sensitive data, interacts with the device, and potentially communicates with external servers.

Write for a mixed audience of technical journalists, software engineers, security reviewers, and product/privacy people. The report should be readable without Android reverse-engineering expertise, but precise enough that coders can trace each claim back to evidence.

Important reporting rules:

* Separate capability from observed behavior. A manifest permission is capability evidence, not proof of collection.
* Separate static code presence from runtime behavior. A bytecode or smali reference is code-presence evidence, not proof that a user flow triggers it.
* Do not imply surveillance, exfiltration, or malicious intent unless the supplied evidence proves it.
* Prefer clear severity language: high concern, medium concern, low concern, unknown, or needs dynamic validation.
* Explain why each finding matters in plain English.
* Include enough technical detail for developers: permissions, APIs, component names, and source-slice paths when supplied.
* State limitations prominently.
* If the app is TikTok, Snapchat, Instagram, or another consumer social app, frame the analysis as a privacy assessment of a large consumer technology product rather than as a claim about nationality or politics.

Use this checklist when analyzing the supplied APK evidence:

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

## User Message

Create the final publishable privacy assessment report from the evidence below.

Audience: technical journalists, software engineers, privacy reviewers, and informed readers.

Required structure:
1. Clear headline and one-paragraph summary.
2. Key findings ranked by concern level.
3. Evidence table that distinguishes manifest permissions, static API references, exported components, and source reconstruction targets.
4. Plain-English explanation of why each issue matters.
5. Technical appendix with file/class/API references.
6. Limitations and what dynamic testing would be needed next.

Use only the supplied evidence. Do not invent runtime behavior or network traffic.

Evidence brief:

# Android APK Privacy Assessment: TikTok

## Scope

- APK path: `TikTok_39.2.1_APKPure.apk`
- Package: `com.zhiliaoapp.musically`
- Version: `39.2.1` / `2023902010`
- Main activity: `com.ss.android.ugc.aweme.splash.SplashActivity`
- SDK range: min `21`, target `34`

This report is written for arbitrary consumer Android APKs, including TikTok, Snapchat, Instagram, or similar social apps. The working premise is that modern consumer tech can be intrusive, but every claim below is limited to the evidence found in the analyzed APK.

## Executive Summary

The APK declares 51 permissions and 53 exported components. Static analysis found privacy-relevant API references and source-reconstruction targets, but no dynamic runtime testing has been performed in this milestone.

The strongest publishable claims at this stage are capability and code-presence claims. Runtime collection, transmission, and user-flow triggering still need dynamic validation before they are described as observed behavior.

## Evidence Model

- Declared permission: capability appears in the manifest; this does not prove collection.
- Static API reference: bytecode or smali references an API; this does not prove a user flow triggers it.
- Source reconstruction: a smali class has been selected for readable reconstruction because it supports a finding.
- Source finding packet: line-cited smali evidence and optional JADX reading context have been extracted for review.
- Runtime behavior: not assessed in this milestone.

## App Surface

| Metric | Count |
| --- | --- |
| Permissions | 51 |
| Activities | 407 |
| Services | 83 |
| Broadcast receivers | 42 |
| Content providers | 24 |
| Exported components | 53 |

## Findings

### Certificate And Signing

**Evidence grade:** APK signing metadata. **Source:** Androguard certificate extraction. **Confidence:** high.

| Field | Value |
| --- | --- |
| Signed | True |
| V1 signature | True |
| V2 signature | True |
| V3 signature | True |
| Certificate count | 1 |
| Subject | C=86, ST=Shanghai, L=Shanghai, O=musical.ly Inc., OU=android, CN=musical.ly |
| Issuer | C=86, ST=Shanghai, L=Shanghai, O=musical.ly Inc., OU=android, CN=musical.ly |
| Valid from | 2015-04-28T04:27:17+00:00 |
| Valid until | 2040-04-21T04:27:17+00:00 |
| SHA-256 | 9041803e91bcb814b4b4399fb5c85a91640b755e5e8ba76813814bf4cf2ab5ba |

Certificate metadata identifies the APK signer and helps compare whether two APK samples share the same signing lineage. It is not, by itself, proof that the analyzed APK came from an official app store channel.

### Sensitive Permissions

**Evidence grade:** declared permission. **Source:** AndroidManifest.xml via Androguard report. **Confidence:** high.

| Permission | Privacy area |
| --- | --- |
| android.permission.ACCESS_ADSERVICES_AD_ID | advertising identifier |
| android.permission.ACCESS_COARSE_LOCATION | approximate location |
| android.permission.BLUETOOTH_CONNECT | nearby Bluetooth devices |
| android.permission.CAMERA | camera |
| android.permission.POST_NOTIFICATIONS | notifications |
| android.permission.READ_CONTACTS | contacts |
| android.permission.READ_EXTERNAL_STORAGE | external storage |
| android.permission.READ_MEDIA_AUDIO | audio |
| android.permission.READ_MEDIA_IMAGES | images |
| android.permission.READ_MEDIA_VIDEO | videos |
| android.permission.RECORD_AUDIO | microphone |
| android.permission.WRITE_EXTERNAL_STORAGE | external storage writes |
| com.google.android.gms.permission.AD_ID | Google advertising identifier |

### Exported Components

**Evidence grade:** manifest declaration. **Source:** Androguard exported component extraction. **Confidence:** medium.

| Component |
| --- |
| activity: com.aweme.account.login.OTLIntentHandlerActivity |
| activity: com.byted.cast.usbsource.usbdisplaysource.UsbSourceActivity |
| activity: com.bytedance.android.livesdk.game.broadcast.mirror.activity.UsbSourceProxyActivity |
| activity: com.bytedance.effectcreatormobile.creatortiktok.preview.CKENewEffectEditorActivity |
| activity: com.bytedance.effectcreatormobile.effectimgcreator.EffectImgCreatorActivity |
| activity: com.bytedance.globalpayment.googlepayapi.PIPOPayActivity |
| activity: com.bytedance.pipo.checkout.sdk.internal.CheckoutActivity |
| activity: com.bytedance.pipo.checkout.sdk.internal.PIManagementActivity |
| activity: com.bytedance.sdk.account.OneTapLoginActivity |
| activity: com.facebook.CustomTabActivity |
| activity: com.kakao.sdk.auth.AuthCodeHandlerActivity |
| activity: com.ss.android.account.share.data.write.activity.ShareDataActivity |
| activity: com.ss.android.sdk.activity.BootstrapActivity |
| activity: com.ss.android.ugc.aweme.deeplink.AppLinkHandlerV2 |
| activity: com.ss.android.ugc.aweme.deeplink.DeepLinkActivityV2 |
| activity: com.ss.android.ugc.aweme.main.MainActivity |
| activity: com.ss.android.ugc.aweme.share.SystemShareActivity |
| activity: com.ss.android.ugc.aweme.share.linkshare.OpenLinkShareActivity |
| activity: com.ss.android.ugc.aweme.share.linkshare.OpenLinkShareMainActivity |
| activity: com.ss.android.ugc.aweme.shortvideo.ui.VideoRecordPermissionActivity |
| activity: com.ss.android.ugc.gamora.recorder.sticker.aigc.AIGCGenerationDraftCompatActivity |
| activity: com.ss.n_project.opensdk_tt.ui.Lemon8AuthActivity |
| activity: com.ss.n_project.opensdk_tt.ui.WebAuthActivity |
| activity: com.tokopedia.loginkit.view.LoginLauncherActivity |
| activity: com.zhiliaoapp.musically.openauthorize.AwemeAuthorizedActivity |

Only the first 25 exported components are shown here; total exported components: 53.

### Static API Signals

**Evidence grade:** static API reference. **Source:** Androguard bytecode analysis. **Confidence:** medium.

| Category | Unique references | Examples |
| --- | --- | --- |
| Dynamic Code Loading | 3 | Ldalvik/system/DexClassLoader;-><init>, Ldalvik/system/PathClassLoader;-><init>, Ljava/lang/reflect/Method;->invoke |
| SMS Abuse | 0 |  |
| Privacy Invasion | 2 | Landroid/hardware/Camera;->open, Landroid/location/LocationManager;->getLastKnownLocation |
| Command Execution | 2 | Ljava/lang/ProcessBuilder;->start, Ljava/lang/Runtime;->exec |

### Permission-To-API Mapping

**Evidence grade:** static API reference. **Source:** Androguard permission/API map. **Confidence:** medium.

| Permission | Declared in manifest | Mapped references |
| --- | --- | --- |
| android.permission.CAMERA | True | Landroid/hardware/Camera;->open |
| android.permission.ACCESS_FINE_LOCATION | False | Landroid/location/LocationManager;->getLastKnownLocation |

## Source Reconstruction Targets

**Evidence grade:** source reconstruction shortlist. **Source:** privacy keyword inventory over decompiled smali. **Confidence:** medium.

| File | Class | Categories | Matches |
| --- | --- | --- | --- |
| smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali | Lcom/google/android/gms/ads/identifier/AdvertisingIdClient | identifiers, network_telemetry | 54 |
| smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali | Lcom/bytedance/helios/statichook/config/ApiHookConfig | camera_microphone, contacts_accounts, identifiers, installed_apps, location, network_telemetry | 78 |
| smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali | Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread | camera_microphone | 290 |
| smali_classes17/X/0eGv.1.smali | LX/0eGv | camera_microphone, contacts_accounts, dynamic_loading, identifiers, installed_apps, local_storage, location, network_telemetry | 149 |
| smali_classes16/X/0awA.2.smali | LX/0awA | installed_apps | 2 |
| smali_classes17/X/0dMp.1.smali | LX/0dMp | local_storage | 189 |
| smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali | Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener | network_telemetry | 217 |
| smali_classes11/X/0PuX.2.smali | LX/0PuX | dynamic_loading | 42 |
| smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali | Lcom/bytedance/android/live/wallet/WalletExchange | command_execution, local_storage | 13 |
| smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali | Lcom/ss/android/vesdk/audio/TEAudioRecord | camera_microphone | 154 |

## Source Finding Packets

**Evidence grade:** line-cited static source evidence. **Source:** apktool smali with optional JADX context. **Confidence:** medium.

| Priority | Smali file | Class | JADX source | Categories | Evidence lines |
| --- | --- | --- | --- | --- | --- |
| 1 | smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali | Lcom/google/android/gms/ads/identifier/AdvertisingIdClient | jadx_decompiled/sources/com/google/android/gms/ads/identifier/AdvertisingIdClient.java | identifiers, network_telemetry | 1:identifiers:AdvertisingId, 38:identifiers:AdvertisingId, 53:identifiers:AdvertisingId |
| 2 | smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali | Lcom/bytedance/helios/statichook/config/ApiHookConfig | jadx_selected/ApiHookConfig.java | camera_microphone, contacts_accounts, identifiers, installed_apps, location, network_telemetry | 50:identifiers:getDeviceId, 193:network_telemetry:okhttp, 229:network_telemetry:okhttp |
| 3 | smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali | Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread | not supplied | camera_microphone | 1:camera_microphone:AudioRecord, 8:camera_microphone:AudioRecord, 18:camera_microphone:AudioRecord |
| 4 | smali_classes17/X/0eGv.1.smali | LX/0eGv | not supplied | camera_microphone, contacts_accounts, dynamic_loading, identifiers, installed_apps, local_storage, location, network_telemetry | 7:contacts_accounts:AccountManager, 59:contacts_accounts:AccountManager, 63:contacts_accounts:getAccounts |
| 5 | smali_classes16/X/0awA.2.smali | LX/0awA | not supplied | installed_apps | 239:installed_apps:queryIntentActivities, 464:installed_apps:queryIntentActivities |
| 6 | smali_classes17/X/0dMp.1.smali | LX/0dMp | not supplied | local_storage | 144:local_storage:SharedPreferences, 610:local_storage:SharedPreferences, 618:local_storage:SharedPreferences |
| 7 | smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali | Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener | not supplied | network_telemetry | 1:network_telemetry:okhttp, 17:network_telemetry:okhttp, 54:network_telemetry:okhttp |
| 8 | smali_classes11/X/0PuX.2.smali | LX/0PuX | not supplied | dynamic_loading | 111:dynamic_loading:ClassLoader, 119:dynamic_loading:ClassLoader, 252:dynamic_loading:ClassLoader |

The excerpts below are review aids. Publishable claims still need human confirmation of control flow and triggerability.

#### `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali`

- Class: `Lcom/google/android/gms/ads/identifier/AdvertisingIdClient`
- JADX source: `jadx_decompiled/sources/com/google/android/gms/ads/identifier/AdvertisingIdClient.java`
- Categories: `identifiers`, `network_telemetry`

Smali evidence:
- Line 1, `identifiers`, `AdvertisingId`: `.class public Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;`
- Line 38, `identifiers`, `AdvertisingId`: `iput-object v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LIZLLL:Ljava/lang/Object;`

JADX reading context:
- Line 34: `public class AdvertisingIdClient {`
- Line 68: `public AdvertisingIdClient(boolean z, Context context, boolean z2) {`

#### `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`

- Class: `Lcom/bytedance/helios/statichook/config/ApiHookConfig`
- JADX source: `jadx_selected/ApiHookConfig.java`
- Categories: `camera_microphone`, `contacts_accounts`, `identifiers`, `installed_apps`, `location`, `network_telemetry`

Smali evidence:
- Line 50, `identifiers`, `getDeviceId`: `const-string v0, "This class is used as a dictionary maintains.\nDictionary layout:\n |---- key: API ID, an integer value\n |---- value: {API ID, API name hash code, API related resource id(may be empty), API related resource name(maybe empty), permissions(maybe empty), permis...`
- Line 193, `network_telemetry`, `okhttp`: `const-string v7, "okhttp3.OkHttpClient$Builder.build"`

JADX reading context:
- Line 1257: `desc = "This class is used as a dictionary maintains.\nDictionary layout:\n |---- key: API ID, an integer value\n |---- value: {API ID, API name hash code, API related resource id(may be empty), API related resource name(maybe empty), permissions(maybe empty), permission type(...`
- Line 1276: `LIZIZ.put(400100, new C1089340eSA(400100, "okhttp3.OkHttpClient$Builder.build", "oh", "OkHttp", new String[0], new String[]{"ok_http"}, new String[]{"6399108190750172076"}, "before"));`

#### `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`

- Class: `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread`
- JADX source: `not supplied`
- Categories: `camera_microphone`

Smali evidence:
- Line 1, `camera_microphone`, `AudioRecord`: `.class public Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;`
- Line 8, `camera_microphone`, `AudioRecord`: `value = Lcom/byted/cast/capture/audio/AudioRecorder;`


## Reviewed Source Notes

The following notes are human-reviewed interpretation of selected source packets. They should carry more weight than unreviewed packet excerpts, but they still do not prove runtime behavior unless explicitly labeled as observed.

# Reviewed Source Notes

These notes are the first reviewed interpretation layer for selected Path 2 source packets. They are meant to improve the generated privacy report, but they do not establish runtime behavior unless explicitly marked as observed.

## Review Summary

| Priority | Source packet | Reviewed status | Report value |
| --- | --- | --- | --- |
| 1 | `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali` | reviewed, static-only | High value for explaining TikTok/ByteDance sensitive API monitoring hooks |
| 2 | `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali` | reviewed, static-only | Medium value for advertising identifier capability and Google telemetry context |
| 3 | `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali` | reviewed, static-only | High value for network telemetry validation planning |
| 4 | `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali` | reviewed, static-only | High value for actual audio-capture capability in cast/media flows |
| 5 | `smali_classes17/X/0eGv.1.smali` | reviewed, static-only | High value as a broad sensitive-API wrapper and hook bridge |
| 6 | `smali_classes16/X/0awA.2.smali` | reviewed, static-only | Medium value for installed-app/app-to-app resolution behavior |
| 7 | `smali_classes17/X/0dMp.1.smali` | reviewed, static-only | Medium value for local preferences/config persistence |
| 8 | `smali_classes11/X/0PuX.2.smali` | reviewed, likely false-positive static signal | Low privacy value; ClassLoader use is parcelable reconstruction, not dynamic Dex loading |
| 9 | `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali` | reviewed, static-only | Medium value for wallet state, live telemetry labels, and bounded locale command execution |
| 10 | `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali` | reviewed, static-only | High value for video SDK microphone capture capability and privacy-cert wrappers |

## 1. `ApiHookConfig`

- Smali evidence: `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`
- JADX reading context: `jadx_selected/ApiHookConfig.java`
- Runtime observed: `false`
- Confidence: `medium-high` for static interpretation; `unknown` for runtime behavior
- Report finding supported: TikTok contains a ByteDance/Helios API hook dictionary for monitoring or intercepting privacy-sensitive API calls.

### Reconstructed Behavior

`ApiHookConfig` appears to build two core maps:

- An action-invoker map that includes `NetworkInvoker`, `ApiCallingActionInvoker`, `ApiCallingActionNewArchInvoker`, and `PermissionPopUpActionInvoker`.
- A large API dictionary mapping numeric API IDs to method names, resource/data categories, invoker IDs, and invocation modes such as `before` or `around`.

The class description says the dictionary is used at runtime to monitor sensitive API usage and gives `getDeviceId/getSSID` as examples of APIs that are not allowed in TikTok. The JADX output shows network hooks for URL connection, OkHttp, and ByteDance Retrofit/TTNet builders and calls. It also shows hooks for installed-app queries, camera open, AudioRecord calls, location manager calls, and TelephonyManager `getDeviceId`.

### Data Or Capabilities Touched

- Network clients and telemetry: URLConnection, OkHttp, Retrofit, TTNet.
- Device identifiers: `TelephonyManager.getDeviceId`.
- Location: `LocationManager.getLastKnownLocation`, `getCurrentLocation`, `requestLocationUpdates`, and related GNSS/listener APIs.
- Camera/audio: `Camera.open`, `AudioRecord.startRecording`, `AudioRecord.read`, stop/release calls.
- Installed-app queries: `PackageManager.queryIntentActivities`.
- Permission or API-use governance: `PermissionPopUpActionInvoker` and inventory/action invokers.

### Evidence Anchors

- `source_findings.md`: line 50 smali description says the class is a dictionary for monitoring sensitive API usage.
- `jadx_selected/ApiHookConfig.java`: lines 68-69 register `NetworkInvoker` and `ApiCallingActionInvoker`.
- `jadx_selected/ApiHookConfig.java`: line 1251 registers `PermissionPopUpActionInvoker`.
- `jadx_selected/ApiHookConfig.java`: lines 1275-1283 register URLConnection, OkHttp, Retrofit, and TTNet hooks.
- `jadx_selected/ApiHookConfig.java`: line 1313 registers `PackageManager.queryIntentActivities`.
- `jadx_selected/ApiHookConfig.java`: lines 1406 and 1421-1424 register camera and AudioRecord hooks.
- `jadx_selected/ApiHookConfig.java`: lines 1439-1467 register location hooks.
- `jadx_selected/ApiHookConfig.java`: line 1447 registers `TelephonyManager.getDeviceId`.

### What This Proves

The APK contains a ByteDance/TikTok hook configuration for privacy-sensitive API monitoring or interception. This is stronger than a generic keyword hit because the class explicitly describes a sensitive API dictionary and maps concrete Android APIs to action invokers.

### What This Does Not Prove

This does not prove misuse, covert collection, transmission, or that each listed API is called in a user flow. The hook system may be a compliance/governance mechanism intended to prevent misuse. Runtime validation is needed to determine when hooks fire and what events or data are emitted.

### Runtime Follow-Up

- Use proxy capture and logs during launch, login, browse, camera, upload, contact sync, location, and share flows.
- Look for telemetry events or network calls that correspond to API-hook categories.
- Confirm whether events include raw sensitive values, hashed identifiers, permission state, call-site names, or only aggregate governance metadata.

## 2. `AdvertisingIdClient`

- Smali evidence: `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali`
- JADX reading context: `jadx_decompiled/sources/com/google/android/gms/ads/identifier/AdvertisingIdClient.java`
- Runtime observed: `false`
- Confidence: `medium` for static interpretation; `unknown` for runtime behavior
- Report finding supported: The APK contains Google advertising ID client code and telemetry related to Advertising ID access.

### Reconstructed Behavior

The class is a Google Advertising ID client implementation. It manages a service connection, retrieves an advertising ID and limit-ad-tracking value through `Info(this.LIZIZ.getId(), this.LIZIZ.LLLIZZ(true))`, and contains a telemetry helper that can send diagnostic parameters to `https://pagead2.googlesyndication.com/pagead/gen_204?id=gmob-apps`.

The telemetry helper appears to send metadata such as app context, limit-ad-tracking state, advertising ID length, error class, experiment ID, tag, and elapsed time. The reviewed snippet does not show the raw advertising ID being sent in that diagnostic call; it records `ad_id_size` rather than the ID value.

### Data Or Capabilities Touched

- Google Advertising ID.
- Limit-ad-tracking setting.
- Diagnostic telemetry about Advertising ID access.
- Google endpoint `pagead2.googlesyndication.com`.

### Evidence Anchors

- `jadx_decompiled/sources/com/google/android/gms/ads/identifier/AdvertisingIdClient.java`: lines 139-145 build telemetry for `AdvertisingIdClient` and the Google `gen_204` endpoint.
- `jadx_decompiled/sources/com/google/android/gms/ads/identifier/AdvertisingIdClient.java`: line 303 constructs an `Info` object from `getId()` and limit-ad-tracking state.

### What This Proves

The APK contains code capable of obtaining the Google Advertising ID and limit-ad-tracking state, and the code includes a diagnostic telemetry path for Advertising ID client behavior.

### What This Does Not Prove

This does not prove TikTok calls this code during normal use, sends the raw Advertising ID to TikTok or third parties, or ignores user ad-tracking preferences. This may be bundled Google Play Services-style code or SDK code.

### Runtime Follow-Up

- Capture launch, login, ad/feed, and reset-ad-ID flows.
- Look for Advertising ID, app set ID, attribution IDs, or equivalent identifiers in first-party and third-party requests.
- Check whether consent and limit-ad-tracking state change the observed traffic.

## 3. `OkHttpEventListener`

- Smali evidence: `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali`
- Runtime observed: `false`
- Confidence: `medium` for static interpretation; `unknown` for data sensitivity
- Report finding supported: The APK contains ByteDance APM instrumentation for OkHttp network events.

### Reconstructed Behavior

`OkHttpEventListener` appears to wrap or extend an OkHttp event listener and collect network timing, request/response header, URL, socket, response-code, byte-count, and server-timing metadata into an `OkHttpRecord`. The smali shows fields for request and response headers as JSON objects, a URL string, DNS/connect/request/response timing fields, and a call to `MonitorTool.monitorSLA`.

This is plausibly performance or reliability monitoring, not necessarily privacy-invasive by itself. Its privacy importance depends on which URLs and headers are captured, whether headers are redacted, and whether the resulting monitor payload leaves the device.

### Data Or Capabilities Touched

- Request URL.
- Request headers and response headers.
- Remote socket/host/port information.
- HTTP response code.
- Sent and received byte counts.
- DNS, TCP, TLS, request, response, and server-timing metrics.
- Trace headers such as `x-tt-trace-host`, `x_tt_trace_id`, `x_tt_trace_tag`, and content encoding.

### Evidence Anchors

- `tiktok_decompiled/smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali`: lines 17-37 define `OkHttpRecord`, request/response header JSON, timing fields, and URL.
- Same file: lines 1123-1190 add `requestHeader` and `responseHeader` data to a JSON payload.
- Same file: lines 1211-1235 pass duration, start time, URL, remote socket, response code, and JSON payload to `MonitorTool.monitorSLA`.
- Same file: lines 2365-2397 read request URL and request headers.
- Same file: lines 2744-2856 extract trace/content headers and response headers.

### What This Proves

The APK contains network instrumentation that can collect HTTP metadata and timing information for OkHttp traffic.

### What This Does Not Prove

This does not prove request bodies, response bodies, credentials, tokens, or PII are collected. It also does not prove the monitoring payload is sent externally in the reviewed flow. Header redaction behavior still needs source review or runtime capture.

### Runtime Follow-Up

- Capture traffic during launch, login, feed browsing, search, profile view, posting/upload, and logout.
- Identify APM/monitoring endpoints and inspect whether request URLs, headers, trace IDs, account IDs, or auth tokens are included.
- Check whether sensitive headers are redacted before telemetry transmission.

## 4. `AudioRecorder$AudioThread`

- Smali evidence: `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`
- Runtime observed: `false`
- Confidence: `high` for audio-capture capability; `unknown` for user-flow activation and transmission
- Report finding supported: The APK contains a concrete audio-recording thread in a ByteDance cast/media capture package.

### Reconstructed Behavior

`AudioRecorder$AudioThread` initializes Android `AudioRecord`, supports both microphone capture and `MediaProjection` playback capture, starts recording, repeatedly reads PCM audio, passes captured frames to `onAudioFrameAvailable`, then stops and releases recorder resources. The code path includes safety or adapter interfaces around start, stop, and release operations.

The package name and log strings point to cast/media capture functionality. That makes the finding privacy-relevant, but not by itself evidence of covert microphone recording.

### Data Or Capabilities Touched

- Microphone audio capture through `AudioRecord`.
- System/playback audio capture through `MediaProjection` and `AudioPlaybackCaptureConfiguration`.
- PCM audio buffers passed to the app's audio-frame handling callback.
- Noise suppression and acoustic echo cancellation resources.

### Evidence Anchors

- Same file: line 458 calls `AudioRecord.getMinBufferSize`.
- Same file: lines 615, 697, and 742 access `MediaProjection` and construct an `AudioPlaybackCaptureConfiguration`.
- Same file: lines 867-900 build an `AudioRecord` using `AudioRecord$Builder`.
- Same file: lines 932-978 create a microphone `AudioRecord`.
- Same file: lines 2115-2220 start audio recording through adapter/safety interfaces.
- Same file: lines 2323, 2489, and 2505 read audio through the `LX/0eGv` wrapper.
- Same file: lines 2469, 2694, 2854, and 3073 pass audio frames to `onAudioFrameAvailable`.
- Same file: lines 3135-3252 and 3480-3906 stop and release recorder resources.

### What This Proves

The APK contains code capable of capturing microphone or playback audio in a cast/media path.

### What This Does Not Prove

This does not prove capture happens without user action, without Android permission prompts, during normal feed browsing, or that audio leaves the device. Runtime validation is needed.

### Runtime Follow-Up

- Exercise screen casting, live, upload, recording, and microphone flows.
- Watch Android permission prompts, logcat privacy-hook events, and proxy traffic during start/stop transitions.
- Confirm whether audio frames remain local to the feature or are uploaded.

## 5. `X/0eGv`

- Smali evidence: `smali_classes17/X/0eGv.1.smali`
- JADX reading context: `jadx_decompiled/sources/X/C1082370eGv.java`
- Runtime observed: `false`
- Confidence: `high` that this is a sensitive-API wrapper/hook bridge; `unknown` for runtime event content
- Report finding supported: The APK contains a broad generated or obfuscated wrapper around Android privacy-sensitive APIs.

### Reconstructed Behavior

`X/0eGv` wraps calls to many Android APIs that expose accounts, installed-app state, camera, audio, location, sensors, clipboard, content resolver data, Wi-Fi details, telephony details, cookies, network connections, and third-party attribution or auth SDK flows. It appears to be the low-level invocation bridge used by the higher-level Helios/Pumbaa sensitive API hook configuration.

Because this class contains wrappers rather than product features, it should be interpreted as instrumentation/governance infrastructure unless runtime evidence shows data collection beyond API-use metadata.

### Data Or Capabilities Touched

- Accounts and account types.
- Installed-app and intent resolution.
- Camera and camera2 operations.
- Location APIs.
- AudioRecord start, read, stop, and release.
- Sensors, clipboard, content resolver, Wi-Fi, telephony, cookies, and network builders.
- URLConnection, OkHttp, Retrofit, and ByteDance networking.

### Evidence Anchors

- Same file: lines 7-326 wrap `AccountManager.getAccounts` and `getAccountsByType`.
- Same file: lines 7370-7539 wrap `PackageManager.queryIntentActivities`.
- Same file: lines 7571-7861 wrap `Camera.open`.
- Same file: lines 10283-10450 wrap `CameraManager.openCamera`.
- Same file: lines 10817-10967 wrap `LocationManager.getLastKnownLocation`.
- Same file: lines 11370-12265 wrap `AudioRecord.read`, `startRecording`, `stop`, and `release`.
- Same file: lines 14826-15507 wrap Wi-Fi info access, including SSID and connection info.
- Same file: lines 18480-19869 wrap telephony network, SIM, and listener APIs.
- Same file: lines 20750-21284 wrap WebView/CookieManager cookie access.
- Same file: lines 36250-37219 wrap URLConnection, OkHttp, and Retrofit builders.

### What This Proves

The APK includes a broad privacy-sensitive API wrapper surface. Combined with `ApiHookConfig`, this materially improves confidence that the app has centralized sensitive API monitoring or interception infrastructure.

### What This Does Not Prove

This does not prove each wrapped API is called by TikTok features, that sensitive values are collected, or that governance events are transmitted externally.

### Runtime Follow-Up

- Correlate wrapper categories with logcat and traffic while exercising permissions and feature flows.
- Determine whether hook events contain raw values, call-site metadata, permission state, hashed values, or only counters.

## 6. `X/0awA`

- Smali evidence: `smali_classes16/X/0awA.2.smali`
- Runtime observed: `false`
- Confidence: `medium` for app-to-app resolution behavior; `unknown` for telemetry
- Report finding supported: The APK contains code that resolves external app handlers and inspects intent filters.

### Reconstructed Behavior

`X/0awA` obtains `PackageManager`, resolves an activity or service for an intent, calls the `X/0eGv` wrapper for `queryIntentActivities`, and inspects `IntentFilter` authorities and paths. The context suggests custom tabs, deep links, auth, or app-to-app integration rather than a broad installed-app inventory scan.

### Data Or Capabilities Touched

- App/package presence through `resolveActivity`, `resolveService`, and `queryIntentActivities`.
- Intent-filter authorities and paths.
- External app/service integration state.

### Evidence Anchors

- Same file: line 170 obtains `PackageManager`.
- Same file: line 199 calls `resolveActivity`.
- Same file: lines 231 and 456 call `LX/0eGv.LJJIZ` for `queryIntentActivities`.
- Same file: line 322 calls `resolveService`.
- Same file: lines 527-547 inspect `IntentFilter` authorities and paths.

### What This Proves

The APK can check which installed apps or services can handle selected intents.

### What This Does Not Prove

This does not prove the app performs broad installed-app inventory collection or sends app-presence results off-device.

### Runtime Follow-Up

- Exercise share, login, external-link, custom-tab, and app-open flows.
- Compare traffic with and without common apps installed to see whether app-presence results are transmitted.

## 7. `X/0dMp`

- Smali evidence: `smali_classes17/X/0dMp.1.smali`
- Runtime observed: `false`
- Confidence: `medium` for local persistence/config behavior; `unknown` for sensitivity of stored values
- Report finding supported: The APK contains a substantial SharedPreferences-backed state or configuration store.

### Reconstructed Behavior

`X/0dMp` initializes a `SharedPreferences` instance, reads many strings, booleans, integers, longs, and string sets, and writes them back through an editor. One prominent key is `raw_json`, which is read and later written through helper methods. The class appears to manage serialized settings or configuration state.

The privacy concern is local persistence of potentially sensitive state, but the reviewed packet does not establish that the stored data is personal or secret.

### Data Or Capabilities Touched

- SharedPreferences local storage.
- Serialized JSON under `raw_json`.
- Multiple preference keys with string, boolean, integer, long, and set values.
- Bundle input fields read into the same state machinery.

### Evidence Anchors

- Same file: line 144 declares a `SharedPreferences` field.
- Same file: lines 610-618 initialize and store the preferences object.
- Same file: lines 2694-2702 read the `raw_json` string.
- Same file: lines 7562-8644 write many preference values through an editor.
- Same file: lines 8693-8705 write `raw_json`.
- Same file: lines 9042, 9138, and 9147 remove preference values.

### What This Proves

The APK contains a local preference/config persistence component with serialized JSON state.

### What This Does Not Prove

This does not prove the preferences contain PII, tokens, message content, identifiers, or other sensitive data.

### Runtime Follow-Up

- Inspect app data after launch, login, feed, search, upload, wallet, and logout flows.
- Identify preference file names, keys, raw JSON schema, encryption state, retention, and whether logout clears sensitive values.

## 8. `X/0PuX`

- Smali evidence: `smali_classes11/X/0PuX.2.smali`
- Runtime observed: `false`
- Confidence: `high` that the current dynamic-loading hit is a false positive
- Report finding supported: The source packet should reduce concern for the specific `ClassLoader` signal in this class.

### Reconstructed Behavior

`X/0PuX` implements `Parcelable.Creator` for `StickerNewEngineModel`. It repeatedly retrieves `StickerNewEngineModel.class.getClassLoader()` and passes that class loader to `Parcel.readParcelable`. That is normal Android parcel reconstruction behavior for typed model fields.

### Data Or Capabilities Touched

- Sticker/editing model deserialization.
- Parcelable nested model reconstruction.
- ClassLoader used as a type-resolution helper for parcel data.

### Evidence Anchors

- Same file: line 6 implements `Parcelable.Creator`.
- Same file: line 11 links the creator to `StickerNewEngineModel`.
- Same file: lines 107-119 obtain `StickerNewEngineModel`'s class loader and call `Parcel.readParcelable`.
- Same file: lines 1989-2093 construct a `StickerNewEngineModel` from parcel fields.

### What This Proves

This packet does not support a dynamic Dex-loading finding. It is better classified as a benign parcelable/model deserialization signal unless other evidence links it to untrusted parcel input.

### What This Does Not Prove

This does not rule out dynamic loading elsewhere in the APK.

### Runtime Follow-Up

- Do not prioritize this packet for privacy runtime testing unless a broader serialization or exported-component review identifies untrusted parcel entry points.

## 9. `WalletExchange`

- Smali evidence: `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali`
- Runtime observed: `false`
- Confidence: `medium` for wallet/live exchange state and telemetry labels; `low` for security concern
- Report finding supported: The command-execution marker is bounded to a locale lookup, while the class is more relevant for wallet settings and live monetization telemetry.

### Reconstructed Behavior

`WalletExchange` implements wallet exchange and auto-exchange behavior for live revenue or gift flows. It reads and writes SharedPreferences keys for auto-exchange state, builds labels such as `exchange_type`, `charge_reason`, `user_id`, and live analytics event names, and formats currency/locale strings.

The class contains a `Runtime.exec` call, but the reviewed code shows it executing `getprop persist.sys.locale` to determine locale. That is not arbitrary command execution in the evidence reviewed here.

### Data Or Capabilities Touched

- Wallet/live auto-exchange preferences.
- Gift, charge, exchange, and live revenue labels.
- User/event metadata labels in live monetization flows.
- System locale via `getprop persist.sys.locale`.

### Evidence Anchors

- Same file: lines 669-685 execute `getprop persist.sys.locale`.
- Same file: lines 856-884 write `live_revenue_auto_exchange` to SharedPreferences.
- Same file: lines 938-966 write `live_auto_exchange` to SharedPreferences.
- Same file: lines 2894-2910 read `live_revenue_auto_exchange`.
- Same file: lines 3817-3833 read `live_auto_exchange`.
- Same file: lines 4480-4649 build live exchange/gift event labels including `user_id` and `livesdk_lynx_auto_send_gift_success`.
- Same file: lines 5668-5689 reference `livesdk_auto_balance_exchange_status`, `status`, and `charge_reason`.

### What This Proves

The APK contains live wallet auto-exchange state handling and analytics labels. The command-execution hit in this class is a fixed system-property lookup for locale.

### What This Does Not Prove

This does not prove arbitrary code execution, vulnerable command injection, or unsafe handling of wallet data. It also does not prove live wallet event payloads are transmitted with sensitive values.

### Runtime Follow-Up

- Exercise wallet, gift, creator revenue, and auto-exchange settings where legally and ethically permitted.
- Inspect traffic for wallet/gift event fields, user identifiers, retention, consent, and regional privacy behavior.

## 10. `TEAudioRecord`

- Smali evidence: `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali`
- Runtime observed: `false`
- Confidence: `high` for video SDK microphone capture capability; `unknown` for user-flow activation and transmission
- Report finding supported: The APK contains a video SDK audio recording abstraction with privacy-cert wrappers.

### Reconstructed Behavior

`TEAudioRecord` is an audio recording helper in the video editing/capture SDK. It initializes `AudioRecord`, chooses system audio source, channel, format, sample rate, and buffer size, reads audio into buffers, and supports start, stop, release, and callback setup. The class also retrieves `VEAudioCaptureSettings.getAudioPrivacyCertMap()` and passes `Cert` objects into start/stop/release flows, suggesting privacy/governance wrapping around recording operations.

### Data Or Capabilities Touched

- Microphone audio capture through `AudioRecord`.
- PCM byte and direct buffer reads.
- Video SDK audio callbacks and native audio data callback hooks.
- ByteDance BPEA privacy certificates around audio lifecycle operations.

### Evidence Anchors

- Same file: line 24 declares the `AudioRecord` field.
- Same file: lines 324-423 initialize `AudioRecord`.
- Same file: lines 924-957 retrieve audio privacy certs and release on failure.
- Same file: lines 1746-1827 read from `AudioRecord` into a `ByteBuffer`.
- Same file: lines 1998-2075 read from `AudioRecord` into a byte array.
- Same file: lines 2281-2412 release using a privacy cert wrapper.
- Same file: lines 2556-2668 start recording using a privacy cert wrapper.
- Same file: lines 2915-3041 stop recording using a privacy cert wrapper.

### What This Proves

The APK contains video SDK code capable of microphone audio recording, and that code is wired into privacy-certificate/governance wrappers.

### What This Does Not Prove

This does not prove background microphone recording, covert recording, or network transmission of audio.

### Runtime Follow-Up

- Exercise recording, upload, live, effects, voiceover, and editing flows.
- Verify permission prompts, mic privacy indicators, start/stop timing, and whether audio-derived data leaves the device.

## Methodology

1. Androguard parsed the APK metadata, manifest-derived surfaces, and selected bytecode API references.
2. apktool output was scanned for privacy-relevant smali keywords.
3. The reconstruction inventory selected a small set of high-signal source slices from a very large decompiled corpus.
4. Source finding packets added line-cited smali context and optional JADX reading context where available.
5. Findings were labeled by evidence type to avoid overstating static analysis as runtime proof.

## Limitations

- Static analysis can miss behavior hidden behind obfuscation, native code, encrypted strings, feature flags, or server-controlled paths.
- Static analysis can also overstate risk when a referenced API is unreachable, dead code, guarded by consent checks, or only used by third-party SDK internals.
- No dynamic analysis, network interception, account login, or device-flow testing is included in this milestone.

## Next Steps

- Manually reconstruct the selected source slices into readable pseudocode with file and line citations.
- Add dynamic validation for the highest-impact findings.
- Compare findings across additional APKs, such as Snapchat and Instagram, using the same evidence model.
