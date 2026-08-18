# TikTok Android APK 39.2.1 Privacy Assessment: Broad Sensitive-API Capability, Audio Capture Code, Network Instrumentation, and Large Exposed App Surface Require Runtime Validation

**Summary:** Static analysis of `TikTok_39.2.1_APKPure.apk` (`com.zhiliaoapp.musically`, version `39.2.1` / `2023902010`) found a large Android app surface: 51 declared permissions, 407 activities, 83 services, 42 broadcast receivers, 24 content providers, and 53 exported components. The APK declares sensitive permissions for camera, microphone, contacts, media storage, approximate location, notifications, Bluetooth connectivity, and advertising identifiers. Source review also found concrete audio-recording classes, broad privacy-sensitive API hook/wrapper infrastructure, Google Advertising ID client code, OkHttp network instrumentation, app-to-app resolution code, and SharedPreferences-backed local state. **No dynamic testing was performed**, so this report does **not** claim that TikTok collected, transmitted, or misused any specific data in runtime user flows. The strongest claims here are about **capabilities, static code presence, and review targets that need dynamic validation**.

---

## 1. Key Findings Ranked by Concern Level

### High concern / needs dynamic validation

#### 1. Broad sensitive permission surface

The manifest declares permissions that give the app capability to request access to sensitive device areas, including:

- Camera: `android.permission.CAMERA`
- Microphone: `android.permission.RECORD_AUDIO`
- Contacts: `android.permission.READ_CONTACTS`
- Approximate location: `android.permission.ACCESS_COARSE_LOCATION`
- Media files: `READ_MEDIA_AUDIO`, `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO`
- External storage: `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`
- Advertising identifiers: `ACCESS_ADSERVICES_AD_ID`, `com.google.android.gms.permission.AD_ID`
- Nearby Bluetooth devices: `BLUETOOTH_CONNECT`
- Notifications: `POST_NOTIFICATIONS`

**What this proves:** The APK is capable of requesting these Android-protected accesses.

**What this does not prove:** A declared permission does not prove the app actually collects contacts, audio, camera footage, location, media files, or advertising IDs during use. Android runtime prompts, feature gating, consent flows, and server-side controls were not tested.

**Why it matters:** These permissions cover categories that can reveal intimate information: people a user knows, physical surroundings, voice/audio, approximate location, media library contents, and advertising identity. For a large consumer social app, reviewers should verify that each permission is requested only when necessary, explained clearly, and limited to relevant features.

---

#### 2. Concrete microphone/audio capture code is present in multiple media components

Static source review found two high-signal audio capture implementations:

- `com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`
- `com/ss/android/vesdk/audio/TEAudioRecord.smali`

The reviewed code includes Android `AudioRecord` setup, start/read/stop/release flows, PCM buffer reads, and callbacks such as `onAudioFrameAvailable`. One cast/media path also references `MediaProjection` and `AudioPlaybackCaptureConfiguration`, indicating capability for playback/system audio capture in supported flows.

**What this proves:** The APK contains code capable of recording microphone audio and, in cast/media contexts, handling playback audio capture.

**What this does not prove:** This does not prove background recording, covert recording, recording during feed browsing, recording without Android permission prompts, or transmission of audio off-device.

**Why it matters:** Microphone and playback audio are highly sensitive. Even when legitimate — for video recording, live streaming, voiceover, effects, or casting — reviewers need to confirm that recording begins and ends at expected moments, follows Android permission UX, and does not continue outside the relevant feature.

---

#### 3. Broad privacy-sensitive API hook and wrapper infrastructure is present

The APK contains ByteDance/TikTok privacy-sensitive API monitoring or interception infrastructure:

- `ApiHookConfig`
- `X/0eGv`

Reviewed source notes describe `ApiHookConfig` as building an API dictionary and action-invoker map for sensitive APIs. It maps concrete Android and network APIs including:

- `TelephonyManager.getDeviceId`
- `LocationManager.getLastKnownLocation`
- `LocationManager.getCurrentLocation`
- location update/listener APIs
- `Camera.open`
- `AudioRecord.startRecording`, `AudioRecord.read`, stop/release calls
- `PackageManager.queryIntentActivities`
- URLConnection, OkHttp, Retrofit, and TTNet networking hooks

`X/0eGv` appears to be a broad wrapper/bridge around sensitive API calls, covering accounts, installed-app resolution, camera, audio, location, Wi-Fi, telephony, cookies, content resolver access, sensors, clipboard, and network builders.

**What this proves:** The APK contains centralized infrastructure for monitoring, wrapping, or intercepting privacy-sensitive API use.

**What this does not prove:** This does not prove misuse. The infrastructure may be a governance/compliance mechanism intended to restrict sensitive API access or produce internal audit telemetry. Runtime testing is required to determine whether hooks fire, what data they record, and whether any hook telemetry leaves the device.

**Why it matters:** Centralized sensitive-API instrumentation can be privacy-protective, privacy-invasive, or both depending on implementation. If it records only call-site metadata and enforces policy, it can reduce risk. If it captures raw values, identifiers, headers, or user data and transmits them broadly, it can increase privacy exposure.

---

#### 4. OkHttp network instrumentation can collect URL, header, timing, socket, and response metadata

`com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali` appears to collect network performance and request metadata into an `OkHttpRecord`. Reviewed notes identify fields and flows for:

- request URL
- request and response headers as JSON objects
- remote socket/host/port
- response code
- sent/received byte counts
- DNS, TCP, TLS, request, response, and server-timing metrics
- trace headers such as `x-tt-trace-host`, `x_tt_trace_id`, and `x_tt_trace_tag`
- eventual call to `MonitorTool.monitorSLA`

**What this proves:** The APK contains ByteDance APM/network instrumentation capable of observing HTTP metadata for OkHttp traffic.

**What this does not prove:** This does not prove request bodies, response bodies, credentials, auth tokens, message content, or PII are collected. It also does not prove that this metadata is transmitted externally in the reviewed paths.

**Why it matters:** URLs and headers can contain sensitive information even without request bodies. Network instrumentation should redact auth tokens and sensitive headers, avoid logging full personal URLs where possible, and clearly separate performance telemetry from user data.

---

### Medium concern / needs dynamic validation

#### 5. Advertising ID capability and Google Advertising ID client code are present

The manifest declares advertising identifier permissions:

- `android.permission.ACCESS_ADSERVICES_AD_ID`
- `com.google.android.gms.permission.AD_ID`

Static source review found:

- `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali`
- JADX source: `jadx_decompiled/sources/com/google/android/gms/ads/identifier/AdvertisingIdClient.java`

Reviewed notes say the code can retrieve a Google Advertising ID and limit-ad-tracking state and includes diagnostic telemetry to:

- `https://pagead2.googlesyndication.com/pagead/gen_204?id=gmob-apps`

The reviewed snippet reportedly sends diagnostics such as app context, limit-ad-tracking state, advertising ID length, error class, experiment ID, tag, and elapsed time. It did **not** show the raw advertising ID being sent in that diagnostic call.

**What this proves:** Advertising ID client code and advertising-ID permissions are present.

**What this does not prove:** This does not prove TikTok calls this code during normal use, sends the raw Advertising ID to TikTok or third parties, or ignores ad-tracking preferences.

**Why it matters:** Advertising IDs are designed for cross-app advertising and measurement. They are privacy-sensitive because they can support profiling or attribution unless constrained by user choice, policy, and consent.

---

#### 6. Large exported component surface requires security review

The APK has 53 exported components. The evidence brief lists the first 25, including deep-link, login/auth, share, payment, checkout, and third-party auth-related activities.

Examples include:

- `com.ss.android.ugc.aweme.deeplink.AppLinkHandlerV2`
- `com.ss.android.ugc.aweme.deeplink.DeepLinkActivityV2`
- `com.ss.android.ugc.aweme.share.SystemShareActivity`
- `com.ss.android.ugc.aweme.share.linkshare.OpenLinkShareActivity`
- `com.zhiliaoapp.musically.openauthorize.AwemeAuthorizedActivity`
- `com.bytedance.pipo.checkout.sdk.internal.CheckoutActivity`
- `com.bytedance.globalpayment.googlepayapi.PIPOPayActivity`
- `com.facebook.CustomTabActivity`
- `com.kakao.sdk.auth.AuthCodeHandlerActivity`

**What this proves:** The manifest exposes a sizable inter-app interaction surface.

**What this does not prove:** Exported components are not automatically vulnerable. This evidence does not show missing validation, privilege escalation, data leakage, or exploitable intent handling.

**Why it matters:** Exported Android components can receive intents from other apps. Deep links, auth handlers, payment screens, and share flows should validate callers, inputs, redirect targets, and sensitive extras to prevent spoofing, open redirects, unauthorized actions, or leakage through inter-process communication.

---

#### 7. Installed-app / app-to-app resolution code is present

`X/0awA` contains code that obtains `PackageManager`, resolves activities and services, calls the `X/0eGv` wrapper for `queryIntentActivities`, and inspects `IntentFilter` authorities and paths.

**What this proves:** The APK can check which installed apps or services can handle selected intents.

**What this does not prove:** This does not prove a broad installed-app inventory scan or transmission of app-presence results.

**Why it matters:** Knowing which other apps are installed or can handle certain links can reveal user interests, banking/payment apps, browsers, messaging apps, or social networks. In many legitimate flows — login, sharing, deep links, custom tabs — some app resolution is expected, but broad inventorying would require stronger privacy justification.

---

#### 8. SharedPreferences-backed local state and serialized JSON storage are present

`X/0dMp` contains a substantial SharedPreferences-backed store. Reviewed notes identify:

- a `SharedPreferences` field
- initialization and storage of the preferences object
- reads and writes of strings, booleans, integers, longs, and string sets
- a prominent `raw_json` key read and written through helper methods
- preference removals

**What this proves:** The APK contains local preference/config persistence with serialized JSON state.

**What this does not prove:** This does not prove the stored values include PII, tokens, identifiers, message content, or other sensitive data. The evidence does not establish whether values are encrypted.

**Why it matters:** Local storage can retain sensitive data across sessions. Reviewers should verify what is stored, whether sensitive values are encrypted or minimized, and whether logout or account deletion clears relevant state.

---

#### 9. Wallet/live monetization state and analytics labels are present

`WalletExchange.smali` contains wallet exchange and auto-exchange behavior for live revenue or gift flows. Reviewed notes identify:

- SharedPreferences keys such as `live_revenue_auto_exchange` and `live_auto_exchange`
- labels including `exchange_type`, `charge_reason`, `user_id`
- event names such as `livesdk_lynx_auto_send_gift_success`
- `livesdk_auto_balance_exchange_status`
- a `Runtime.exec` call limited in reviewed evidence to `getprop persist.sys.locale`

**What this proves:** The APK contains live wallet/auto-exchange state handling and analytics labels. The command-execution hit in this class is a fixed system-property lookup for locale.

**What this does not prove:** This does not prove arbitrary command execution, command injection, unsafe wallet data handling, or external transmission of wallet event payloads.

**Why it matters:** Wallet, gift, revenue, and payment-adjacent flows are privacy- and security-sensitive because they can involve money, creator earnings, account identity, and regional compliance requirements.

---

### Low concern / informational

#### 10. One dynamic-loading signal was reviewed as likely false positive

`X/0PuX` initially appeared in a dynamic-loading keyword scan because it uses a `ClassLoader`. Human review found it implements `Parcelable.Creator` for `StickerNewEngineModel` and uses `StickerNewEngineModel.class.getClassLoader()` for `Parcel.readParcelable`.

**What this proves:** This specific source packet does not support a dynamic Dex-loading concern.

**What this does not prove:** It does not rule out dynamic loading elsewhere in the APK. Separate static API references still show `DexClassLoader`, `PathClassLoader`, and reflective `Method.invoke`.

**Why it matters:** Static keyword scans often produce false positives. Reviewing and downgrading benign findings reduces noise and helps focus dynamic testing on real privacy risks.

---

#### 11. Certificate metadata is consistent and useful for sample comparison, but not a privacy finding

The APK is signed with V1, V2, and V3 signatures. One certificate was extracted:

- Subject/issuer: `C=86, ST=Shanghai, L=Shanghai, O=musical.ly Inc., OU=android, CN=musical.ly`
- Valid from: `2015-04-28T04:27:17+00:00`
- Valid until: `2040-04-21T04:27:17+00:00`
- SHA-256: `9041803e91bcb814b4b4399fb5c85a91640b755e5e8ba76813814bf4cf2ab5ba`

**What this proves:** The sample has signing metadata that can be used to compare signing lineage with other APK samples.

**What this does not prove:** Certificate metadata alone does not prove the APK came from an official app store channel or that the app behaved in any particular way.

---

## 2. Evidence Table

### App and analysis scope

| Item | Evidence |
|---|---|
| APK path | `TikTok_39.2.1_APKPure.apk` |
| Package | `com.zhiliaoapp.musically` |
| Version | `39.2.1` / `2023902010` |
| Main activity | `com.ss.android.ugc.aweme.splash.SplashActivity` |
| SDK range | min `21`, target `34` |
| Runtime testing | Not performed |
| Evidence model | Manifest declarations, static API references, exported components, source reconstruction targets, line-cited source packets |

---

### Manifest permissions — capability evidence, not proof of collection

| Privacy area | Manifest permission | Evidence grade | Concern |
|---|---|---:|---|
| Advertising identifier | `android.permission.ACCESS_ADSERVICES_AD_ID` | Declared permission | Medium |
| Advertising identifier | `com.google.android.gms.permission.AD_ID` | Declared permission | Medium |
| Approximate location | `android.permission.ACCESS_COARSE_LOCATION` | Declared permission | High / validate |
| Nearby Bluetooth devices | `android.permission.BLUETOOTH_CONNECT` | Declared permission | Medium |
| Camera | `android.permission.CAMERA` | Declared permission | High / validate |
| Notifications | `android.permission.POST_NOTIFICATIONS` | Declared permission | Low-medium |
| Contacts | `android.permission.READ_CONTACTS` | Declared permission | High / validate |
| External storage read | `android.permission.READ_EXTERNAL_STORAGE` | Declared permission | Medium-high / validate |
| Media audio | `android.permission.READ_MEDIA_AUDIO` | Declared permission | Medium-high / validate |
| Media images | `android.permission.READ_MEDIA_IMAGES` | Declared permission | Medium-high / validate |
| Media video | `android.permission.READ_MEDIA_VIDEO` | Declared permission | Medium-high / validate |
| Microphone | `android.permission.RECORD_AUDIO` | Declared permission | High / validate |
| External storage write | `android.permission.WRITE_EXTERNAL_STORAGE` | Declared permission | Medium / validate |

---

### Static API references — code-presence evidence, not proof of runtime behavior

| Category | Static references found | Examples | Evidence grade | Concern |
|---|---:|---|---|---|
| Dynamic code loading / reflection | 3 | `DexClassLoader.<init>`, `PathClassLoader.<init>`, `Method.invoke` | Static API reference | Medium, but needs review |
| SMS abuse | 0 | None supplied | Static API reference | No finding from supplied evidence |
| Privacy-sensitive API access | 2 | `Camera.open`, `LocationManager.getLastKnownLocation` | Static API reference | High / validate |
| Command execution | 2 | `ProcessBuilder.start`, `Runtime.exec` | Static API reference | Low-medium after source review of one instance |
| Permission-to-API mapping | 2 rows | `CAMERA` declared + `Camera.open`; `ACCESS_FINE_LOCATION` not declared + `LocationManager.getLastKnownLocation` | Static map | Needs control-flow validation |

Important nuance: the evidence maps `LocationManager.getLastKnownLocation` to `ACCESS_FINE_LOCATION`, but the manifest evidence provided does **not** list `ACCESS_FINE_LOCATION`; it lists `ACCESS_COARSE_LOCATION`. This should be reviewed dynamically and in source control flow before drawing conclusions about precise-location access.

---

### Exported components — manifest surface evidence, not proof of vulnerability

| Metric | Count |
|---|---:|
| Activities | 407 |
| Services | 83 |
| Broadcast receivers | 42 |
| Content providers | 24 |
| Exported components | 53 |

First 25 exported components supplied in the evidence brief:

| Exported component |
|---|
| `activity: com.aweme.account.login.OTLIntentHandlerActivity` |
| `activity: com.byted.cast.usbsource.usbdisplaysource.UsbSourceActivity` |
| `activity: com.bytedance.android.livesdk.game.broadcast.mirror.activity.UsbSourceProxyActivity` |
| `activity: com.bytedance.effectcreatormobile.creatortiktok.preview.CKENewEffectEditorActivity` |
| `activity: com.bytedance.effectcreatormobile.effectimgcreator.EffectImgCreatorActivity` |
| `activity: com.bytedance.globalpayment.googlepayapi.PIPOPayActivity` |
| `activity: com.bytedance.pipo.checkout.sdk.internal.CheckoutActivity` |
| `activity: com.bytedance.pipo.checkout.sdk.internal.PIManagementActivity` |
| `activity: com.bytedance.sdk.account.OneTapLoginActivity` |
| `activity: com.facebook.CustomTabActivity` |
| `activity: com.kakao.sdk.auth.AuthCodeHandlerActivity` |
| `activity: com.ss.android.account.share.data.write.activity.ShareDataActivity` |
| `activity: com.ss.android.sdk.activity.BootstrapActivity` |
| `activity: com.ss.android.ugc.aweme.deeplink.AppLinkHandlerV2` |
| `activity: com.ss.android.ugc.aweme.deeplink.DeepLinkActivityV2` |
| `activity: com.ss.android.ugc.aweme.main.MainActivity` |
| `activity: com.ss.android.ugc.aweme.share.SystemShareActivity` |
| `activity: com.ss.android.ugc.aweme.share.linkshare.OpenLinkShareActivity` |
| `activity: com.ss.android.ugc.aweme.share.linkshare.OpenLinkShareMainActivity` |
| `activity: com.ss.android.ugc.aweme.shortvideo.ui.VideoRecordPermissionActivity` |
| `activity: com.ss.android.ugc.gamora.recorder.sticker.aigc.AIGCGenerationDraftCompatActivity` |
| `activity: com.ss.n_project.opensdk_tt.ui.Lemon8AuthActivity` |
| `activity: com.ss.n_project.opensdk_tt.ui.WebAuthActivity` |
| `activity: com.tokopedia.loginkit.view.LoginLauncherActivity` |
| `activity: com.zhiliaoapp.musically.openauthorize.AwemeAuthorizedActivity` |

---

### Source reconstruction targets — reviewed static source evidence

| File | Class | Categories | Review value | Concern |
|---|---|---|---|---|
| `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali` | `Lcom/google/android/gms/ads/identifier/AdvertisingIdClient` | identifiers, network telemetry | Advertising ID capability and Google diagnostic telemetry context | Medium |
| `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali` | `Lcom/bytedance/helios/statichook/config/ApiHookConfig` | camera/mic, contacts, identifiers, installed apps, location, network telemetry | Sensitive API hook dictionary | High / validate |
| `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali` | `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread` | camera/microphone | Concrete audio capture path for cast/media flows | High / validate |
| `smali_classes17/X/0eGv.1.smali` | `LX/0eGv` | broad sensitive API wrapper categories | Broad sensitive-API wrapper/hook bridge | High / validate |
| `smali_classes16/X/0awA.2.smali` | `LX/0awA` | installed apps | App-to-app intent resolution behavior | Medium |
| `smali_classes17/X/0dMp.1.smali` | `LX/0dMp` | local storage | SharedPreferences/config persistence | Medium |
| `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali` | `Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener` | network telemetry | OkHttp metadata/timing instrumentation | High / validate |
| `smali_classes11/X/0PuX.2.smali` | `LX/0PuX` | dynamic loading keyword hit | Reviewed as parcelable ClassLoader false positive | Low |
| `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali` | `Lcom/bytedance/android/live/wallet/WalletExchange` | command execution, local storage | Wallet/live exchange state and bounded locale command | Medium for wallet review; low for command concern |
| `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali` | `Lcom/ss/android/vesdk/audio/TEAudioRecord` | camera/microphone | Video SDK microphone capture with privacy-cert wrappers | High / validate |

---

## 3. Plain-English Explanation of Why These Issues Matter

### Permissions are doors the app can ask Android to open

A manifest permission is not proof that data is collected. But it tells reviewers which sensitive doors the app can ask to open. Camera, microphone, contacts, media files, location, and advertising IDs are especially sensitive because they can expose a user’s environment, social graph, behavior, identity, and personal content.

For a consumer social app, many of these permissions may be feature-justified: video recording needs camera and mic; sharing may need media access; contact sync may need contacts; notifications may need notification permission. The privacy question is whether access is **timely, contextual, optional, minimized, and clearly explained**.

---

### Audio recording code is expected in a video app, but still high-impact

TikTok is a video and live-media app, so the presence of audio recording code is not surprising. The concern is not that such code exists; the concern is that microphone capture is one of the highest-impact mobile capabilities.

Dynamic testing should verify:

- whether Android permission prompts appear before recording;
- whether the microphone privacy indicator appears only during expected flows;
- whether recording stops promptly;
- whether audio frames are uploaded, processed locally, or discarded;
- whether cast/playback capture is clearly user-initiated.

---

### API hook infrastructure may be privacy governance — or telemetry — depending on what it records

The Helios/Pumbaa-style hook dictionary and wrapper layer are important because they sit near sensitive Android APIs. They may be designed to enforce internal privacy rules, log sensitive API use, block disallowed calls, or attach “privacy certificates” to risky operations.

This can be good governance if it prevents unauthorized API use. But if the hook events include raw location, account lists, identifiers, URLs, cookies, or headers, it could become an additional data collection layer. The evidence only proves the infrastructure is present, not what it emits.

---

### Network instrumentation can accidentally capture sensitive metadata

Performance monitoring often records request timing, status codes, hosts, URLs, and headers. That is common in large apps. The risk is that URLs and headers sometimes contain tokens, account identifiers, search terms, experiment IDs, or other sensitive values.

The key questions for dynamic validation are:

- Are Authorization/Cookie headers redacted?
- Are full URLs logged, or only domains/routes?
- Are user IDs or trace IDs included?
- Where are monitoring payloads sent?
- Are payloads tied to logged-in identity?

---

### Exported components are an attack surface, not automatically a vulnerability

Exported activities and other components allow other apps, browsers, or Android itself to invoke parts of the app. That is normal for deep links, share sheets, login callbacks, payment flows, and custom tabs.

The risk appears when exported components accept untrusted input without validation. Reviewers should test deep-link and intent handling for spoofed redirects, unauthorized state changes, sensitive extras, and insecure cross-app data sharing.

---

### Advertising IDs support measurement and advertising, but need consent and preference checks

The Advertising ID is intended for ad measurement and personalization. The presence of Google Advertising ID code and permissions does not prove tracking. But it does mean reviewers should validate whether the app accesses the ID, when it does so, which parties receive it, and whether user ad-tracking preferences alter behavior.

---

### Local preferences are normal, but sensitive values should not be stored casually

SharedPreferences are common for configuration and app state. The evidence does not show sensitive data in preferences. Still, serialized JSON under keys such as `raw_json` should be inspected after realistic use because preferences can persist identifiers, tokens, feature state, or account metadata if developers are not careful.

---

## 4. Technical Appendix

### APK metadata

| Field | Value |
|---|---|
| APK | `TikTok_39.2.1_APKPure.apk` |
| Package | `com.zhiliaoapp.musically` |
| Version name/code | `39.2.1` / `2023902010` |
| Main activity | `com.ss.android.ugc.aweme.splash.SplashActivity` |
| Min SDK | `21` |
| Target SDK | `34` |

---

### Signing metadata

| Field | Value |
|---|---|
| Signed | `True` |
| V1 signature | `True` |
| V2 signature | `True` |
| V3 signature | `True` |
| Certificate count | `1` |
| Subject | `C=86, ST=Shanghai, L=Shanghai, O=musical.ly Inc., OU=android, CN=musical.ly` |
| Issuer | `C=86, ST=Shanghai, L=Shanghai, O=musical.ly Inc., OU=android, CN=musical.ly` |
| Valid from | `2015-04-28T04:27:17+00:00` |
| Valid until | `2040-04-21T04:27:17+00:00` |
| SHA-256 | `9041803e91bcb814b4b4399fb5c85a91640b755e5e8ba76813814bf4cf2ab5ba` |

---

### Sensitive permissions from manifest

Source: AndroidManifest.xml via Androguard report.

```text
android.permission.ACCESS_ADSERVICES_AD_ID
android.permission.ACCESS_COARSE_LOCATION
android.permission.BLUETOOTH_CONNECT
android.permission.CAMERA
android.permission.POST_NOTIFICATIONS
android.permission.READ_CONTACTS
android.permission.READ_EXTERNAL_STORAGE
android.permission.READ_MEDIA_AUDIO
android.permission.READ_MEDIA_IMAGES
android.permission.READ_MEDIA_VIDEO
android.permission.RECORD_AUDIO
android.permission.WRITE_EXTERNAL_STORAGE
com.google.android.gms.permission.AD_ID
```

---

### Static API references from Androguard bytecode analysis

| Category | APIs |
|---|---|
| Dynamic code loading / reflection | `Ldalvik/system/DexClassLoader;-><init>`; `Ldalvik/system/PathClassLoader;-><init>`; `Ljava/lang/reflect/Method;->invoke` |
| Privacy-sensitive APIs | `Landroid/hardware/Camera;->open`; `Landroid/location/LocationManager;->getLastKnownLocation` |
| Command execution | `Ljava/lang/ProcessBuilder;->start`; `Ljava/lang/Runtime;->exec` |
| SMS abuse | No supplied references |

Permission-to-API mapping:

| Permission | Declared | Mapped reference |
|---|---:|---|
| `android.permission.CAMERA` | `True` | `Landroid/hardware/Camera;->open` |
| `android.permission.ACCESS_FINE_LOCATION` | `False` | `Landroid/location/LocationManager;->getLastKnownLocation` |

---

### Source references: `ApiHookConfig`

File:

```text
smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali
```

Class:

```text
Lcom/bytedance/helios/statichook/config/ApiHookConfig
```

JADX context:

```text
jadx_selected/ApiHookConfig.java
```

Evidence anchors supplied:

- Smali line 50: class description says it is a dictionary for monitoring sensitive API usage.
- JADX lines 68–69: register `NetworkInvoker` and `ApiCallingActionInvoker`.
- JADX line 1251: registers `PermissionPopUpActionInvoker`.
- JADX lines 1275–1283: register URLConnection, OkHttp, Retrofit, and TTNet hooks.
- JADX line 1313: registers `PackageManager.queryIntentActivities`.
- JADX lines 1406 and 1421–1424: register camera and `AudioRecord` hooks.
- JADX lines 1439–1467: register location hooks.
- JADX line 1447: registers `TelephonyManager.getDeviceId`.

Static interpretation:

- Sensitive API hook dictionary and invoker configuration.
- Runtime behavior unknown.

---

### Source references: `X/0eGv`

File:

```text
smali_classes17/X/0eGv.1.smali
```

Class:

```text
LX/0eGv
```

JADX context:

```text
jadx_decompiled/sources/X/C1082370eGv.java
```

Evidence anchors supplied:

- Lines 7–326: wrap `AccountManager.getAccounts` and `getAccountsByType`.
- Lines 7370–7539: wrap `PackageManager.queryIntentActivities`.
- Lines 7571–7861: wrap `Camera.open`.
- Lines 10283–10450: wrap `CameraManager.openCamera`.
- Lines 10817–10967: wrap `LocationManager.getLastKnownLocation`.
- Lines 11370–12265: wrap `AudioRecord.read`, `startRecording`, `stop`, and `release`.
- Lines 14826–15507: wrap Wi-Fi info access including SSID and connection info.
- Lines 18480–19869: wrap telephony network, SIM, and listener APIs.
- Lines 20750–21284: wrap WebView/CookieManager cookie access.
- Lines 36250–37219: wrap URLConnection, OkHttp, and Retrofit builders.

Static interpretation:

- Broad sensitive-API wrapper/hook bridge.
- Runtime event contents unknown.

---

### Source references: `AdvertisingIdClient`

File:

```text
smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali
```

Class:

```text
Lcom/google/android/gms/ads/identifier/AdvertisingIdClient
```

JADX context:

```text
jadx_decompiled/sources/com/google/android/gms/ads/identifier/AdvertisingIdClient.java
```

Evidence anchors supplied:

- Smali line 1: `AdvertisingIdClient` class declaration.
- Smali line 38: object field assignment in `AdvertisingIdClient`.
- JADX line 34: `public class AdvertisingIdClient`.
- JADX line 68: constructor.
- JADX lines 139–145: telemetry for `AdvertisingIdClient` and Google `gen_204` endpoint.
- JADX line 303: constructs `Info` from `getId()` and limit-ad-tracking state.

Static interpretation:

- Code capable of obtaining Google Advertising ID and limit-ad-tracking state.
- Diagnostic telemetry path present.
- Reviewed snippet did not show raw Advertising ID sent in the diagnostic call.

---

### Source references: `OkHttpEventListener`

File:

```text
smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali
```

Class:

```text
Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener
```

Evidence anchors supplied:

- Lines 17–37: define `OkHttpRecord`, request/response header JSON, timing fields, and URL.
- Lines 1123–1190: add `requestHeader` and `responseHeader` data to JSON payload.
- Lines 1211–1235: pass duration, start time, URL, remote socket, response code, and JSON payload to `MonitorTool.monitorSLA`.
- Lines 2365–2397: read request URL and request headers.
- Lines 2744–2856: extract trace/content headers and response headers.

Static interpretation:

- Network metadata/timing instrumentation for OkHttp traffic.
- Request/response bodies and token handling not established.

---

### Source references: `AudioRecorder$AudioThread`

File:

```text
smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali
```

Class:

```text
Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread
```

Evidence anchors supplied:

- Line 458: calls `AudioRecord.getMinBufferSize`.
- Lines 615, 697, 742: access `MediaProjection` and construct `AudioPlaybackCaptureConfiguration`.
- Lines 867–900: build `AudioRecord` using `AudioRecord$Builder`.
- Lines 932–978: create microphone `AudioRecord`.
- Lines 2115–2220: start audio recording through adapter/safety interfaces.
- Lines 2323, 2489, 2505: read audio through `LX/0eGv` wrapper.
- Lines 2469, 2694, 2854, 3073: pass audio frames to `onAudioFrameAvailable`.
- Lines 3135–3252 and 3480–3906: stop and release recorder resources.

Static interpretation:

- Concrete audio capture implementation in cast/media code.
- Runtime activation and transmission unknown.

---

### Source references: `TEAudioRecord`

File:

```text
smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali
```

Class:

```text
Lcom/ss/android/vesdk/audio/TEAudioRecord
```

Evidence anchors supplied:

- Line 24: declares `AudioRecord` field.
- Lines 324–423: initialize `AudioRecord`.
- Lines 924–957: retrieve audio privacy certs and release on failure.
- Lines 1746–1827: read from `AudioRecord` into `ByteBuffer`.
- Lines 1998–2075: read from `AudioRecord` into byte array.
- Lines 2281–2412: release using privacy cert wrapper.
- Lines 2556–2668: start recording using privacy cert wrapper.
- Lines 2915–3041: stop recording using privacy cert wrapper.

Static interpretation:

- Video SDK microphone capture abstraction with privacy-certificate/governance wrappers.
- Runtime activation and transmission unknown.

---

### Source references: `X/0awA`

File:

```text
smali_classes16/X/0awA.2.smali
```

Class:

```text
LX/0awA
```

Evidence anchors supplied:

- Line 170: obtains `PackageManager`.
- Line 199: calls `resolveActivity`.
- Lines 231 and 456: call `LX/0eGv.LJJIZ` for `queryIntentActivities`.
- Line 322: calls `resolveService`.
- Lines 527–547: inspect `IntentFilter` authorities and paths.

Static interpretation:

- App-to-app/deep-link/custom-tab style resolution.
- Broad installed-app inventory not proven.

---

### Source references: `X/0dMp`

File:

```text
smali_classes17/X/0dMp.1.smali
```

Class:

```text
LX/0dMp
```

Evidence anchors supplied:

- Line 144: declares `SharedPreferences` field.
- Lines 610–618: initialize and store preferences object.
- Lines 2694–2702: read `raw_json` string.
- Lines 7562–8644: write many preference values through an editor.
- Lines 8693–8705: write `raw_json`.
- Lines 9042, 9138, 9147: remove preference values.

Static interpretation:

- SharedPreferences-backed local configuration/state.
- Sensitivity and encryption state unknown.

---

### Source references: `WalletExchange`

File:

```text
smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali
```

Class:

```text
Lcom/bytedance/android/live/wallet/WalletExchange
```

Evidence anchors supplied:

- Lines 669–685: execute `getprop persist.sys.locale`.
- Lines 856–884: write `live_revenue_auto_exchange` to SharedPreferences.
- Lines 938–966: write `live_auto_exchange` to SharedPreferences.
- Lines 2894–2910: read `live_revenue_auto_exchange`.
- Lines 3817–3833: read `live_auto_exchange`.
- Lines 4480–4649: build live exchange/gift event labels including `user_id` and `livesdk_lynx_auto_send_gift_success`.
- Lines 5668–5689: reference `livesdk_auto_balance_exchange_status`, `status`, and `charge_reason`.

Static interpretation:

- Wallet/live exchange state and telemetry labels.
- Command execution marker is a fixed locale lookup in reviewed evidence.

---

### Source references: `X/0PuX`

File:

```text
smali_classes11/X/0PuX.2.smali
```

Class:

```text
LX/0PuX
```

Evidence anchors supplied:

- Line 6: implements `Parcelable.Creator`.
- Line 11: links creator to `StickerNewEngineModel`.
- Lines 107–119: obtain `StickerNewEngineModel` class loader and call `Parcel.readParcelable`.
- Lines 1989–2093: construct `StickerNewEngineModel` from parcel fields.

Static interpretation:

- This packet is better classified as benign parcelable/model reconstruction, not dynamic Dex loading.

---

## 5. Limitations

This assessment is limited to the supplied APK evidence. It should be read as a **static privacy and security assessment**, not a behavioral audit.

Key limitations:

1. **No runtime testing was performed.**
   The report does not establish what happens during launch, login, browsing, recording, upload, live, wallet, contact sync, location, ad, or sharing flows.

2. **Manifest permissions are capability evidence only.**
   A declared permission does not prove collection or access.

3. **Static API references are code-presence evidence only.**
   A method reference does not prove the code path is reachable or triggered.

4. **Source reconstruction is partial.**
   Only selected smali slices were reviewed. The APK is large and obfuscated in places.

5. **Network traffic was not captured.**
   The report does not claim any observed transmission of identifiers, audio, contacts, location, headers, wallet fields, or telemetry.

6. **Local storage contents were not inspected dynamically.**
   SharedPreferences use was identified statically, but actual preference files, values, encryption state, retention, and logout clearing were not verified.

7. **Native code, encrypted strings, feature flags, and server-controlled behavior may hide or alter behavior.**
   Static review may miss behavior or overstate unreachable code.

8. **Exported components were not fuzzed or manually exercised.**
   The report identifies an exposed component surface, not confirmed vulnerabilities.

---

## 6. Dynamic Testing Needed Next

The following tests would be required before making stronger claims about observed behavior.

### Permission and privacy UX testing

Exercise:

- first launch
- login/signup
- feed browsing
- camera open
- video recording
- upload
- live streaming
- effects/voiceover
- contact sync
- location-related flows
- share/deep-link flows
- wallet/gift/creator revenue flows where legally and ethically permitted

Validate:

- when runtime permission prompts appear;
- whether prompts are tied to clear user actions;
- whether denial is respected;
- whether Android camera/mic privacy indicators match expected capture windows.

---

### Network interception and telemetry validation

Use a controlled test device and proxy tooling such as Burp Suite or OWASP ZAP where feasible.

Look for:

- Advertising ID or replacement identifiers;
- contact-derived values;
- location values;
- media metadata;
- audio-derived data;
- wallet/gift fields;
- full URLs and request headers in APM telemetry;
- redaction of auth/cookie headers;
- hook/governance events generated by `ApiHookConfig` / `X/0eGv`.

Special focus:

- launch/login traffic;
- ad/feed traffic;
- recording/upload traffic;
- live/cast traffic;
- wallet/gift traffic;
- logout and account-switch flows.

---

### Local storage review

After exercising major flows, inspect app-private storage for:

- SharedPreferences file names and keys;
- `raw_json` contents and schema;
- tokens or session identifiers;
- Advertising ID or device identifiers;
- wallet state;
- contact/location/media-derived values;
- encryption or plaintext storage;
- retention after logout.

---

### Exported component and deep-link testing

For the 53 exported components, especially auth, payment, share, and deep-link activities:

- send crafted intents;
- test malformed/deceptive URLs;
- test redirect handling;
- test caller/package validation;
- test whether sensitive extras are accepted or leaked;
- test logged-in versus logged-out behavior.

---

### Audio capture validation

For `AudioRecorder$AudioThread` and `TEAudioRecord`-backed flows:

- verify start/stop timing;
- monitor Android privacy indicators;
- inspect logs and hook events;
- compare traffic before/during/after recording;
- determine whether audio frames are local-only or uploaded;
- test cast/playback capture flows separately from microphone capture.

---

### Sensitive API hook validation

For `ApiHookConfig` and `X/0eGv`:

- correlate sensitive API calls with logcat and network telemetry;
- identify event schemas;
- determine whether hook events include raw values, hashed values, call-site metadata, permission state, or counters only;
- test behavior under permission denial and consent changes.

---

**Bottom line:** The APK contains substantial sensitive capability and instrumentation typical of a large, media-heavy consumer social app. The highest-priority privacy questions are not whether the code exists — it does — but **when it runs, what data it handles, what leaves the device, and whether user choice and platform privacy controls are respected**.