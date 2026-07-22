# Static APK Privacy Assessment of TikTok 39.2.1: Broad Sensitive Permissions, Audio/Media Capture Code, and Privacy-API Hooking Infrastructure — Runtime Behavior Not Yet Observed

This report assesses the Android APK `TikTok_39.2.1_APKPure.apk` for package `com.zhiliaoapp.musically`, version `39.2.1` / `2023902010`, using only supplied static-analysis evidence. The APK declares a large Android surface — 51 permissions, 407 activities, 83 services, 42 broadcast receivers, 24 content providers, and 53 exported components — and contains code references relevant to advertising identifiers, camera, microphone/audio recording, location, installed-app resolution, network telemetry, SharedPreferences storage, and ByteDance/TikTok privacy-sensitive API hook infrastructure. These are capability and code-presence findings, not proof of runtime collection, transmission, or misuse. No dynamic testing, account login, network interception, or user-flow validation was performed in this milestone.

---

## 1. Key Findings Ranked by Concern Level

| Concern level | Finding | Evidence type | What the evidence supports | What it does **not** prove |
|---|---|---|---|---|
| **High concern / needs dynamic validation** | Broad sensitive permission surface | Manifest permissions | The APK requests capabilities for camera, microphone, contacts, media/storage, advertising identifiers, approximate location, Bluetooth connection, and notifications. | Does not prove these data types are collected or transmitted. |
| **High concern / needs dynamic validation** | Concrete microphone and playback-audio capture code exists | Static source reconstruction | Classes such as `AudioRecorder$AudioThread` and `TEAudioRecord` contain Android `AudioRecord` setup, start, read, stop, and release logic. | Does not prove background recording, covert recording, or upload of audio. |
| **High concern / ambiguous purpose** | ByteDance/TikTok privacy-sensitive API hook and wrapper infrastructure | Static source reconstruction | `ApiHookConfig` and `X/0eGv` map or wrap sensitive APIs including camera, audio, location, account, installed-app, telephony, Wi-Fi, cookie, and network APIs. | Does not prove surveillance or misuse; this may be compliance, permission governance, auditing, or safety infrastructure. |
| **Medium-high concern / needs redaction validation** | Network telemetry instrumentation can capture request metadata | Static source reconstruction | `OkHttpEventListener` appears able to collect URL, request/response headers, timing, socket, response code, byte counts, and trace headers for OkHttp traffic. | Does not prove request bodies, credentials, tokens, PII, or telemetry transmission were captured. |
| **Medium concern** | Advertising ID client code and ad-ID permissions are present | Manifest permission + static source | The APK declares advertising ID permissions and includes Google `AdvertisingIdClient` code capable of obtaining the Advertising ID and limit-ad-tracking state. | Does not prove TikTok invokes it in normal use, sends raw ad IDs, or ignores user preferences. |
| **Medium concern / security review needed** | 53 exported Android components | Manifest component declarations | Multiple activities are exported, including deep-link, auth, share, payment, and main-entry related components. | Does not prove an exploitable component vulnerability; intent validation and permissions were not reviewed dynamically. |
| **Medium concern** | Installed-app / external-handler resolution code exists | Static source reconstruction | Code calls or wraps `PackageManager.queryIntentActivities`, `resolveActivity`, and `resolveService`. | Does not prove broad installed-app inventorying or transmission of app-presence data. |
| **Medium concern / unknown data sensitivity** | SharedPreferences-backed local state store with serialized JSON | Static source reconstruction | `X/0dMp` reads and writes many preference values, including a `raw_json` key. | Does not prove storage of PII, tokens, messages, or unencrypted sensitive data. |
| **Low-to-medium concern** | Wallet/live exchange state and analytics labels | Static source reconstruction | `WalletExchange` handles live auto-exchange preferences and builds labels including `exchange_type`, `charge_reason`, and `user_id`. | Does not prove unsafe wallet handling or transmission of sensitive wallet data. |
| **Low concern / likely false positive** | One `ClassLoader` dynamic-loading signal is parcelable reconstruction | Reviewed source note | `X/0PuX` uses `StickerNewEngineModel.class.getClassLoader()` for `Parcel.readParcelable`, which is normal Android model deserialization. | Does not rule out dynamic loading elsewhere in the APK. |

---

## 2. Evidence Table

### 2.1 APK Identity and Signing Metadata

| Field | Evidence |
|---|---|
| APK path | `TikTok_39.2.1_APKPure.apk` |
| Package | `com.zhiliaoapp.musically` |
| Version | `39.2.1` / `2023902010` |
| Main activity | `com.ss.android.ugc.aweme.splash.SplashActivity` |
| SDK range | min `21`, target `34` |
| Signed | `True` |
| Signature schemes | V1, V2, V3 |
| Certificate subject / issuer | `C=86, ST=Shanghai, L=Shanghai, O=musical.ly Inc., OU=android, CN=musical.ly` |
| Certificate validity | 2015-04-28 to 2040-04-21 |
| Certificate SHA-256 | `9041803e91bcb814b4b4399fb5c85a91640b755e5e8ba76813814bf4cf2ab5ba` |

**Interpretation:** Signing metadata helps compare APK samples and signing lineage. It does not, by itself, prove the APK came from an official app-store channel.

---

### 2.2 Application Surface

| Surface area | Count |
|---|---:|
| Permissions | 51 |
| Activities | 407 |
| Services | 83 |
| Broadcast receivers | 42 |
| Content providers | 24 |
| Exported components | 53 |

---

### 2.3 Manifest Permissions — Capability Evidence Only

These permissions are declared in `AndroidManifest.xml`. A declared permission means the app has requested the capability; it does **not** prove collection or use.

| Permission | Privacy area |
|---|---|
| `android.permission.ACCESS_ADSERVICES_AD_ID` | Advertising identifier |
| `com.google.android.gms.permission.AD_ID` | Google advertising identifier |
| `android.permission.ACCESS_COARSE_LOCATION` | Approximate location |
| `android.permission.BLUETOOTH_CONNECT` | Nearby Bluetooth devices |
| `android.permission.CAMERA` | Camera |
| `android.permission.RECORD_AUDIO` | Microphone |
| `android.permission.READ_CONTACTS` | Contacts |
| `android.permission.READ_EXTERNAL_STORAGE` | External storage |
| `android.permission.WRITE_EXTERNAL_STORAGE` | External storage writes |
| `android.permission.READ_MEDIA_AUDIO` | Audio media library |
| `android.permission.READ_MEDIA_IMAGES` | Image media library |
| `android.permission.READ_MEDIA_VIDEO` | Video media library |
| `android.permission.POST_NOTIFICATIONS` | Notifications |

**Notable mapping:** The static API map found a reference to `LocationManager.getLastKnownLocation`, while `android.permission.ACCESS_FINE_LOCATION` was **not** declared in the supplied permission/API map. The manifest evidence supplied shows `ACCESS_COARSE_LOCATION`.

---

### 2.4 Static API References — Code-Presence Evidence Only

These are bytecode or smali references. They show code presence, not that a user flow triggers the code.

| Category | Unique references | Example APIs |
|---|---:|---|
| Dynamic code loading / reflection | 3 | `dalvik.system.DexClassLoader.<init>`, `dalvik.system.PathClassLoader.<init>`, `java.lang.reflect.Method.invoke` |
| Privacy-relevant APIs | 2 | `android.hardware.Camera.open`, `android.location.LocationManager.getLastKnownLocation` |
| Command execution | 2 | `java.lang.ProcessBuilder.start`, `java.lang.Runtime.exec` |
| SMS abuse | 0 | None supplied |

**Important nuance:** One reviewed `ClassLoader` packet, `X/0PuX`, was assessed as likely a false positive for dynamic loading because it uses a class loader for `Parcel.readParcelable`. The reviewed `Runtime.exec` example in `WalletExchange` is a bounded locale lookup: `getprop persist.sys.locale`.

---

### 2.5 Exported Components — Manifest Exposure Evidence

The APK has 53 exported components. Exported components can be invoked by other apps or system flows depending on intent filters and permissions. This requires deeper component-level review before concluding vulnerability.

Only the first 25 exported components were supplied:

| Type | Component |
|---|---|
| activity | `com.aweme.account.login.OTLIntentHandlerActivity` |
| activity | `com.byted.cast.usbsource.usbdisplaysource.UsbSourceActivity` |
| activity | `com.bytedance.android.livesdk.game.broadcast.mirror.activity.UsbSourceProxyActivity` |
| activity | `com.bytedance.effectcreatormobile.creatortiktok.preview.CKENewEffectEditorActivity` |
| activity | `com.bytedance.effectcreatormobile.effectimgcreator.EffectImgCreatorActivity` |
| activity | `com.bytedance.globalpayment.googlepayapi.PIPOPayActivity` |
| activity | `com.bytedance.pipo.checkout.sdk.internal.CheckoutActivity` |
| activity | `com.bytedance.pipo.checkout.sdk.internal.PIManagementActivity` |
| activity | `com.bytedance.sdk.account.OneTapLoginActivity` |
| activity | `com.facebook.CustomTabActivity` |
| activity | `com.kakao.sdk.auth.AuthCodeHandlerActivity` |
| activity | `com.ss.android.account.share.data.write.activity.ShareDataActivity` |
| activity | `com.ss.android.sdk.activity.BootstrapActivity` |
| activity | `com.ss.android.ugc.aweme.deeplink.AppLinkHandlerV2` |
| activity | `com.ss.android.ugc.aweme.deeplink.DeepLinkActivityV2` |
| activity | `com.ss.android.ugc.aweme.main.MainActivity` |
| activity | `com.ss.android.ugc.aweme.share.SystemShareActivity` |
| activity | `com.ss.android.ugc.aweme.share.linkshare.OpenLinkShareActivity` |
| activity | `com.ss.android.ugc.aweme.share.linkshare.OpenLinkShareMainActivity` |
| activity | `com.ss.android.ugc.aweme.shortvideo.ui.VideoRecordPermissionActivity` |
| activity | `com.ss.android.ugc.gamora.recorder.sticker.aigc.AIGCGenerationDraftCompatActivity` |
| activity | `com.ss.n_project.opensdk_tt.ui.Lemon8AuthActivity` |
| activity | `com.ss.n_project.opensdk_tt.ui.WebAuthActivity` |
| activity | `com.tokopedia.loginkit.view.LoginLauncherActivity` |
| activity | `com.zhiliaoapp.musically.openauthorize.AwemeAuthorizedActivity` |

---

### 2.6 Source Reconstruction Targets

These source slices were selected from decompiled smali because they support privacy-relevant findings. They are static reconstruction targets, not runtime observations.

| File | Class | Categories | Matches |
|---|---|---|---:|
| `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali` | `Lcom/google/android/gms/ads/identifier/AdvertisingIdClient` | identifiers, network_telemetry | 54 |
| `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali` | `Lcom/bytedance/helios/statichook/config/ApiHookConfig` | camera_microphone, contacts_accounts, identifiers, installed_apps, location, network_telemetry | 78 |
| `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali` | `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread` | camera_microphone | 290 |
| `smali_classes17/X/0eGv.1.smali` | `LX/0eGv` | camera_microphone, contacts_accounts, dynamic_loading, identifiers, installed_apps, local_storage, location, network_telemetry | 149 |
| `smali_classes16/X/0awA.2.smali` | `LX/0awA` | installed_apps | 2 |
| `smali_classes17/X/0dMp.1.smali` | `LX/0dMp` | local_storage | 189 |
| `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali` | `Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener` | network_telemetry | 217 |
| `smali_classes11/X/0PuX.2.smali` | `LX/0PuX` | dynamic_loading | 42 |
| `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali` | `Lcom/bytedance/android/live/wallet/WalletExchange` | command_execution, local_storage | 13 |
| `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali` | `Lcom/ss/android/vesdk/audio/TEAudioRecord` | camera_microphone | 154 |

---

## 3. Plain-English Explanation of Why Each Issue Matters

### 3.1 Sensitive permissions matter because they define what the app can ask Android to allow

TikTok’s APK declares permissions touching several sensitive areas: camera, microphone, contacts, media files, location, Bluetooth, advertising identifiers, and notifications. For a short-video social app, some of these permissions may be expected for recording, uploading, messaging, sharing, advertising, or personalization features. The privacy concern is not that the permissions exist in isolation, but that they create a broad capability surface. Reviewers should verify that each permission is requested only in context, explained clearly to users, and not used outside the feature that needs it.

**Concern level:** High concern as a capability surface; runtime behavior unknown.

---

### 3.2 Audio recording code matters because microphone access is highly sensitive

Two reviewed code areas contain concrete Android audio capture logic:

- `AudioRecorder$AudioThread`, in a cast/media capture package.
- `TEAudioRecord`, in a video SDK audio recording package.

These classes include `AudioRecord` initialization, recording start/stop, buffer reads, and release paths. The cast/media class also references `MediaProjection` playback capture. This is expected in apps that support recording, live, editing, effects, voiceover, casting, or media capture. It is still privacy-sensitive because audio can reveal speech, surroundings, and private activity.

The supplied evidence does **not** show that TikTok records audio outside user-initiated recording or media flows, nor that audio is transmitted. Android permission prompts, privacy indicators, and runtime traffic must be tested.

**Concern level:** High concern; needs dynamic validation.

---

### 3.3 Privacy API hooks matter because they show centralized monitoring or interception of sensitive APIs

The reviewed `ApiHookConfig` class appears to define a large dictionary of privacy-sensitive Android APIs and maps them to action invokers. The reviewed `X/0eGv` class appears to wrap many such APIs, including accounts, installed apps, camera, audio, location, Wi-Fi, telephony, cookies, and network builders.

This is an important finding, but it is not automatically negative. Large consumer apps often use internal privacy frameworks to track, gate, audit, or block sensitive API use. The evidence even suggests governance-related concepts such as permission pop-up action invokers and privacy-cert wrappers elsewhere. The privacy question is what this framework records at runtime: raw sensitive values, call-site metadata, permission state, hashed identifiers, aggregate counters, or nothing externally transmitted.

**Concern level:** High concern because of breadth; purpose and runtime behavior unknown.

---

### 3.4 Network telemetry instrumentation matters because URLs and headers can themselves contain sensitive information

The reviewed `OkHttpEventListener` appears to collect network metadata such as request URL, request headers, response headers, timing fields, socket information, response code, byte counts, and trace headers. Performance monitoring of this kind is common in large apps, but it can become privacy-sensitive if it captures full URLs, account identifiers, authentication headers, cookies, query parameters, or other user-specific data.

The supplied evidence does not show request bodies, response bodies, credentials, tokens, or PII being collected. It also does not prove telemetry is transmitted externally. The main unresolved question is whether sensitive headers and URL parameters are redacted before monitoring payloads are stored or sent.

**Concern level:** Medium-high; needs runtime redaction and traffic validation.

---

### 3.5 Advertising ID capability matters because it can support cross-app advertising measurement

The manifest declares advertising identifier permissions, and the APK includes Google `AdvertisingIdClient` code. Reviewed source notes state that the class can retrieve an Advertising ID and limit-ad-tracking state and includes a diagnostic path to a Google endpoint, `https://pagead2.googlesyndication.com/pagead/gen_204?id=gmob-apps`.

The reviewed snippet did not show the raw Advertising ID being sent in that diagnostic call; it referenced `ad_id_size`. The presence of this code may reflect bundled SDK functionality. Dynamic testing is needed to determine whether the app invokes Advertising ID access, when it does so, and whether user privacy settings affect observed behavior.

**Concern level:** Medium.

---

### 3.6 Exported components matter because they enlarge the app’s externally reachable attack surface

The APK has 53 exported components. Exported activities are common in social apps for login, sharing, deep links, open authorization, payment, and app-to-app integrations. However, each exported component needs validation: Can another app invoke it? Does it validate incoming intents and URIs? Does it require permissions? Can it receive untrusted extras, parcelables, or deep links that affect account, payment, or sharing flows?

The supplied evidence lists component names but not their intent filters, permission protections, or input validation logic. Therefore this is a review priority, not an established vulnerability.

**Concern level:** Medium; security review needed.

---

### 3.7 Installed-app resolution matters because app presence can reveal user interests or relationships

The reviewed `X/0awA` code resolves activities and services and uses a wrapper for `PackageManager.queryIntentActivities`. This can be legitimate for share sheets, login integrations, custom tabs, app links, or determining whether another app can handle a link. It becomes more privacy-sensitive if used to build a broad inventory of installed apps or transmit app-presence signals.

The reviewed context suggests external-link, custom-tab, auth, or app-to-app integration behavior rather than a demonstrated broad inventory scan. Runtime comparison on devices with different installed apps would be needed.

**Concern level:** Medium.

---

### 3.8 SharedPreferences storage matters because local app state can contain identifiers, tokens, configuration, or user data

The reviewed `X/0dMp` class reads and writes many preference values and includes a `raw_json` key. SharedPreferences are commonly used for configuration, feature flags, cached state, and simple persistence. They are not inherently unsafe, but they are not an appropriate place for unencrypted secrets or highly sensitive personal data unless protected by additional controls.

The supplied evidence does not show the contents of `raw_json` or other keys. It does not establish that the preferences store PII, credentials, tokens, message content, or other sensitive values.

**Concern level:** Medium; sensitivity unknown.

---

### 3.9 Wallet/live exchange code matters because monetization state and user labels can be sensitive

The reviewed `WalletExchange` class appears to handle wallet exchange and auto-exchange preferences in live revenue or gift flows. It builds labels such as `exchange_type`, `charge_reason`, `user_id`, and live analytics event names. That is privacy-relevant because wallet, gifting, and creator monetization flows can involve financially or behaviorally sensitive data.

A static `Runtime.exec` hit in this class was reviewed and appears limited to `getprop persist.sys.locale`, used for locale detection. The supplied evidence does not show arbitrary command execution or command injection.

**Concern level:** Low-to-medium. Wallet telemetry deserves validation; command-execution concern is low based on supplied evidence.

---

### 3.10 One dynamic-loading signal appears to be a false positive

The reviewed `X/0PuX` class implements `Parcelable.Creator` for `StickerNewEngineModel` and uses `StickerNewEngineModel.class.getClassLoader()` with `Parcel.readParcelable`. That is normal Android deserialization for typed parcelable models and does not support a dynamic Dex-loading finding for this class.

This does not eliminate dynamic loading elsewhere, because separate static references to `DexClassLoader` and `PathClassLoader` were supplied.

**Concern level:** Low for this packet.

---

## 4. Technical Appendix

### 4.1 Manifest and APK Metadata

- APK: `TikTok_39.2.1_APKPure.apk`
- Package: `com.zhiliaoapp.musically`
- Version: `39.2.1` / `2023902010`
- Main activity: `com.ss.android.ugc.aweme.splash.SplashActivity`
- SDK: min `21`, target `34`
- Declared permissions: 51
- Exported components: 53
- Activities: 407
- Services: 83
- Receivers: 42
- Providers: 24

---

### 4.2 Sensitive Manifest Permissions

Evidence grade: declared permission, high confidence.

Relevant declared permissions include:

- `android.permission.CAMERA`
- `android.permission.RECORD_AUDIO`
- `android.permission.READ_CONTACTS`
- `android.permission.ACCESS_COARSE_LOCATION`
- `android.permission.BLUETOOTH_CONNECT`
- `android.permission.READ_EXTERNAL_STORAGE`
- `android.permission.WRITE_EXTERNAL_STORAGE`
- `android.permission.READ_MEDIA_AUDIO`
- `android.permission.READ_MEDIA_IMAGES`
- `android.permission.READ_MEDIA_VIDEO`
- `android.permission.POST_NOTIFICATIONS`
- `android.permission.ACCESS_ADSERVICES_AD_ID`
- `com.google.android.gms.permission.AD_ID`

---

### 4.3 Static API References

Evidence grade: static API reference, medium confidence.

| Area | APIs |
|---|---|
| Camera | `Landroid/hardware/Camera;->open` |
| Location | `Landroid/location/LocationManager;->getLastKnownLocation` |
| Dynamic loading / reflection | `Ldalvik/system/DexClassLoader;-><init>`, `Ldalvik/system/PathClassLoader;-><init>`, `Ljava/lang/reflect/Method;->invoke` |
| Command execution | `Ljava/lang/ProcessBuilder;->start`, `Ljava/lang/Runtime;->exec` |

Permission/API mapping supplied:

| Permission | Declared in manifest | Mapped reference |
|---|---:|---|
| `android.permission.CAMERA` | True | `Landroid/hardware/Camera;->open` |
| `android.permission.ACCESS_FINE_LOCATION` | False | `Landroid/location/LocationManager;->getLastKnownLocation` |

---

### 4.4 `ApiHookConfig`: Sensitive API Hook Dictionary

Evidence:

- Smali: `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`
- JADX: `jadx_selected/ApiHookConfig.java`
- Class: `Lcom/bytedance/helios/statichook/config/ApiHookConfig`
- Runtime observed: false
- Static interpretation confidence: medium-high

Relevant anchors:

- Smali line 50: class description says it is a dictionary for monitoring sensitive API usage.
- JADX lines 68–69: registers `NetworkInvoker` and `ApiCallingActionInvoker`.
- JADX line 1251: registers `PermissionPopUpActionInvoker`.
- JADX lines 1275–1283: registers URLConnection, OkHttp, Retrofit, and TTNet hooks.
- JADX line 1313: registers `PackageManager.queryIntentActivities`.
- JADX lines 1406 and 1421–1424: registers camera and `AudioRecord` hooks.
- JADX lines 1439–1467: registers location hooks.
- JADX line 1447: registers `TelephonyManager.getDeviceId`.

Supported claim: the APK contains a ByteDance/TikTok hook configuration for privacy-sensitive API monitoring or interception.

Unsupported claim: runtime misuse, collection, or external transmission.

---

### 4.5 `X/0eGv`: Broad Sensitive-API Wrapper / Hook Bridge

Evidence:

- Smali: `smali_classes17/X/0eGv.1.smali`
- JADX: `jadx_decompiled/sources/X/C1082370eGv.java`
- Class: `LX/0eGv`
- Runtime observed: false
- Static interpretation confidence: high

Relevant anchors:

- Lines 7–326: wraps `AccountManager.getAccounts` and `getAccountsByType`.
- Lines 7370–7539: wraps `PackageManager.queryIntentActivities`.
- Lines 7571–7861: wraps `Camera.open`.
- Lines 10283–10450: wraps `CameraManager.openCamera`.
- Lines 10817–10967: wraps `LocationManager.getLastKnownLocation`.
- Lines 11370–12265: wraps `AudioRecord.read`, `startRecording`, `stop`, and `release`.
- Lines 14826–15507: wraps Wi-Fi info access, including SSID and connection info.
- Lines 18480–19869: wraps telephony network, SIM, and listener APIs.
- Lines 20750–21284: wraps WebView/CookieManager cookie access.
- Lines 36250–37219: wraps URLConnection, OkHttp, and Retrofit builders.

Supported claim: the APK includes a broad privacy-sensitive API wrapper surface.

Unsupported claim: each API is called by product features or transmits sensitive values.

---

### 4.6 `AudioRecorder$AudioThread`: Cast/Media Audio Capture

Evidence:

- Smali: `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`
- Class: `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread`
- Runtime observed: false
- Static interpretation confidence: high for audio-capture capability

Relevant anchors:

- Line 458: calls `AudioRecord.getMinBufferSize`.
- Lines 615, 697, 742: references `MediaProjection` and constructs `AudioPlaybackCaptureConfiguration`.
- Lines 867–900: builds an `AudioRecord` using `AudioRecord.Builder`.
- Lines 932–978: creates a microphone `AudioRecord`.
- Lines 2115–2220: starts audio recording through adapter/safety interfaces.
- Lines 2323, 2489, 2505: reads audio through the `LX/0eGv` wrapper.
- Lines 2469, 2694, 2854, 3073: passes audio frames to `onAudioFrameAvailable`.
- Lines 3135–3252 and 3480–3906: stops and releases recorder resources.

Supported claim: the APK contains code capable of microphone or playback audio capture in a cast/media path.

Unsupported claim: covert recording or audio upload.

---

### 4.7 `TEAudioRecord`: Video SDK Audio Recording

Evidence:

- Smali: `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali`
- Class: `Lcom/ss/android/vesdk/audio/TEAudioRecord`
- Runtime observed: false
- Static interpretation confidence: high for video SDK microphone capture capability

Relevant anchors:

- Line 24: declares the `AudioRecord` field.
- Lines 324–423: initializes `AudioRecord`.
- Lines 924–957: retrieves audio privacy certs and releases on failure.
- Lines 1746–1827: reads from `AudioRecord` into a `ByteBuffer`.
- Lines 1998–2075: reads from `AudioRecord` into a byte array.
- Lines 2281–2412: releases using a privacy cert wrapper.
- Lines 2556–2668: starts recording using a privacy cert wrapper.
- Lines 2915–3041: stops recording using a privacy cert wrapper.

Supported claim: the APK contains video SDK code capable of microphone capture and wired into privacy/governance wrappers.

Unsupported claim: background recording or transmission.

---

### 4.8 `OkHttpEventListener`: Network Metadata Instrumentation

Evidence:

- Smali: `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali`
- Class: `Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener`
- Runtime observed: false
- Static interpretation confidence: medium

Relevant anchors:

- Lines 17–37: defines `OkHttpRecord`, request/response header JSON, timing fields, and URL.
- Lines 1123–1190: adds `requestHeader` and `responseHeader` data to a JSON payload.
- Lines 1211–1235: passes duration, start time, URL, remote socket, response code, and JSON payload to `MonitorTool.monitorSLA`.
- Lines 2365–2397: reads request URL and request headers.
- Lines 2744–2856: extracts trace/content headers and response headers.

Supported claim: the APK contains network instrumentation that can collect HTTP metadata and timing information for OkHttp traffic.

Unsupported claim: body capture, credential capture, or telemetry transmission.

---

### 4.9 `AdvertisingIdClient`: Google Advertising ID Access

Evidence:

- Smali: `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali`
- JADX: `jadx_decompiled/sources/com/google/android/gms/ads/identifier/AdvertisingIdClient.java`
- Class: `Lcom/google/android/gms/ads/identifier/AdvertisingIdClient`
- Runtime observed: false
- Static interpretation confidence: medium

Relevant anchors:

- Smali line 1: class declaration for `AdvertisingIdClient`.
- Smali lines 38 and 53: references to `AdvertisingIdClient`.
- JADX line 34: `public class AdvertisingIdClient`.
- JADX line 68: constructor.
- JADX lines 139–145: telemetry helper for Google `gen_204` endpoint.
- JADX line 303: constructs an `Info` object from `getId()` and limit-ad-tracking state.

Supported claim: the APK contains code capable of obtaining the Google Advertising ID and limit-ad-tracking state.

Unsupported claim: TikTok invokes this code in normal use or sends raw advertising IDs.

---

### 4.10 `X/0awA`: Installed-App / Intent Handler Resolution

Evidence:

- Smali: `smali_classes16/X/0awA.2.smali`
- Class: `LX/0awA`
- Runtime observed: false
- Static interpretation confidence: medium

Relevant anchors:

- Line 170: obtains `PackageManager`.
- Line 199: calls `resolveActivity`.
- Lines 231 and 456: calls `LX/0eGv.LJJIZ` for `queryIntentActivities`.
- Line 322: calls `resolveService`.
- Lines 527–547: inspects `IntentFilter` authorities and paths.

Supported claim: the APK can check which installed apps or services can handle selected intents.

Unsupported claim: broad installed-app inventorying or off-device transmission.

---

### 4.11 `X/0dMp`: SharedPreferences / Local State

Evidence:

- Smali: `smali_classes17/X/0dMp.1.smali`
- Class: `LX/0dMp`
- Runtime observed: false
- Static interpretation confidence: medium

Relevant anchors:

- Line 144: declares a `SharedPreferences` field.
- Lines 610–618: initializes and stores preferences object.
- Lines 2694–2702: reads `raw_json`.
- Lines 7562–8644: writes many preference values through an editor.
- Lines 8693–8705: writes `raw_json`.
- Lines 9042, 9138, 9147: removes preference values.

Supported claim: the APK contains a local preference/config persistence component with serialized JSON state.

Unsupported claim: local storage of PII, secrets, tokens, or message content.

---

### 4.12 `WalletExchange`: Live Wallet State and Locale Command

Evidence:

- Smali: `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali`
- Class: `Lcom/bytedance/android/live/wallet/WalletExchange`
- Runtime observed: false
- Static interpretation confidence: medium for wallet/live state; low security concern for command execution

Relevant anchors:

- Lines 669–685: executes `getprop persist.sys.locale`.
- Lines 856–884: writes `live_revenue_auto_exchange` to SharedPreferences.
- Lines 938–966: writes `live_auto_exchange` to SharedPreferences.
- Lines 2894–2910: reads `live_revenue_auto_exchange`.
- Lines 3817–3833: reads `live_auto_exchange`.
- Lines 4480–4649: builds live exchange/gift event labels including `user_id` and `livesdk_lynx_auto_send_gift_success`.
- Lines 5668–5689: references `livesdk_auto_balance_exchange_status`, `status`, and `charge_reason`.

Supported claim: the APK contains live wallet auto-exchange state handling and analytics labels.

Unsupported claim: arbitrary command execution, command injection, unsafe wallet handling, or transmitted sensitive wallet payloads.

---

### 4.13 `X/0PuX`: Parcelable ClassLoader False Positive

Evidence:

- Smali: `smali_classes11/X/0PuX.2.smali`
- Class: `LX/0PuX`
- Runtime observed: false
- Static interpretation confidence: high that this packet is not dynamic Dex loading

Relevant anchors:

- Line 6: implements `Parcelable.Creator`.
- Line 11: links creator to `StickerNewEngineModel`.
- Lines 107–119: obtains `StickerNewEngineModel` class loader and calls `Parcel.readParcelable`.
- Lines 1989–2093: constructs a `StickerNewEngineModel` from parcel fields.

Supported claim: this specific source packet is normal parcelable/model deserialization, not a dynamic loading finding.

Unsupported claim: absence of dynamic loading elsewhere.

---

## 5. Limitations and Required Dynamic Testing

### 5.1 Major limitations

This assessment is static-only. It can identify declared capabilities and code presence, but it cannot establish runtime behavior.

Specifically:

- No app launch, login, browsing, upload, recording, live, wallet, contact-sync, or sharing flows were tested.
- No network traffic was intercepted.
- No request or response payloads were reviewed.
- No Android permission prompt behavior was observed.
- No local app data directory was inspected after runtime use.
- No server-side feature flags, remote configuration, consent gates, regional behavior, or account-state differences were tested.
- Static analysis can overstate risk when code is unused, dead, SDK-bundled, gated by permissions, or present only for specific features.
- Static analysis can understate risk when behavior is hidden in native code, obfuscated control flow, encrypted strings, server-controlled logic, or dynamically loaded modules.

### 5.2 Dynamic testing needed next

To move from capability/code-presence claims to behavior claims, reviewers should perform controlled runtime testing on instrumented Android devices.

Recommended next tests:

1. **Permission-flow testing**
   - Exercise launch, login, feed, camera, upload, live, effects, voiceover, contact sync, location, share, cast, and wallet flows.
   - Record when Android permission prompts appear.
   - Verify whether permissions are requested contextually and with clear user explanation.

2. **Microphone and audio validation**
   - Test video recording, editing, voiceover, live, casting, and playback-capture flows.
   - Monitor Android microphone indicators and logcat.
   - Confirm start/stop timing around `AudioRecord`.
   - Determine whether captured audio remains local or is uploaded.

3. **Network interception**
   - Use Burp Suite, OWASP ZAP, mitmproxy, or equivalent tooling where feasible.
   - Capture traffic during launch, login, feed, search, profile, posting/upload, live, wallet, logout, and reset-ad-ID flows.
   - Identify whether telemetry includes URLs, headers, trace IDs, account IDs, advertising IDs, tokens, cookies, or other sensitive fields.
   - Validate whether request and response headers are redacted in APM payloads.

4. **Advertising ID behavior**
   - Test with advertising ID available, reset, limited, or disabled where platform settings allow.
   - Observe whether the app or SDKs access ad identifiers and whether consent or limit-ad-tracking state affects traffic.

5. **Sensitive API hook telemetry**
   - Correlate calls to camera, microphone, location, contacts, accounts, installed-app resolution, Wi-Fi, telephony, and cookies with logs and network events.
   - Determine whether hook events contain raw values, hashed values, call-site metadata, permission state, or only aggregate counters.

6. **Exported component security review**
   - Enumerate all 53 exported components, not only the first 25 supplied here.
   - Review intent filters, permissions, URI schemes, input validation, and deep-link handling.
   - Fuzz exported activities with malformed extras, untrusted parcelables, and deep links where legally and ethically appropriate.

7. **Local storage inspection**
   - Inspect SharedPreferences, databases, cache files, and media directories after major flows.
   - Specifically review `raw_json` and wallet/live preference keys.
   - Check whether logout clears sensitive local state and whether sensitive values are encrypted.

8. **Installed-app resolution testing**
   - Compare behavior on devices with different app sets installed.
   - Exercise share, login, open-link, custom-tab, and app-to-app flows.
   - Determine whether app-presence results are transmitted.

---

## Bottom Line

The supplied evidence supports a careful privacy assessment of a large consumer social app with a broad sensitive-permission surface, concrete media/audio capture code, extensive privacy-sensitive API hook infrastructure, advertising ID capability, network metadata instrumentation, exported components, and local state storage. The evidence does **not** establish covert recording, surveillance, exfiltration, malicious intent, or specific runtime data transmission. The highest-priority next step is dynamic validation across real user flows, with special attention to microphone/audio use, network telemetry redaction, advertising identifiers, sensitive API hook events, exported component hardening, and local storage contents.