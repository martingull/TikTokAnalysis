# Reviewed Source Notes

These notes are the first reviewed interpretation layer for selected Path 2 source packets. They are meant to improve the generated privacy report, but they do not establish runtime behavior unless explicitly marked as observed.

## Review Summary

| Priority | Source packet | Reviewed status | Report value |
| --- | --- | --- | --- |
| 1 | `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali` | reviewed, static-only | High value for explaining TikTok/ByteDance sensitive API monitoring hooks |
| 2 | `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali` | reviewed, static-only | Medium value for advertising identifier capability and Google telemetry context |
| 3 | `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali` | reviewed, static-only | High value for network telemetry validation planning |

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

## Remaining Packets Still Needing Manual Review

- `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`: likely media/cast audio capture logic; needs review before making privacy claims beyond static audio capability.
- `smali_classes17/X/0eGv.1.smali`: broad obfuscated hook/wrapper class; potentially important but needs targeted JADX or deeper smali reconstruction.
- `smali_classes16/X/0awA.2.smali`: installed-app query references; likely app-to-app or share/integration behavior, needs context.
- `smali_classes17/X/0dMp.1.smali`: `SharedPreferences` use; need preference key/value review before claiming sensitive local storage.
- `smali_classes11/X/0PuX.2.smali`: current `ClassLoader` signal appears to be parcelable loading, not evidence of dynamic Dex loading.
- `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali`: command-execution category needs careful review before any security claim.
- `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali`: likely video/audio SDK capture path; needs flow context.
