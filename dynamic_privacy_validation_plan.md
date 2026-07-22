# Dynamic Privacy Validation Plan: TikTok

## Scope

- APK path: `TikTok_39.2.1_APKPure.apk`
- Package: `com.zhiliaoapp.musically`
- Version: `39.2.1` / `2023902010`
- Static report input: generated Androguard evidence
- Source packet input: present

This plan translates static privacy findings into runtime checks. It should be run against a test account and a controlled device or emulator. The goal is to label static concerns as `observed`, `not observed`, or `blocked`, not to infer runtime behavior from code presence alone.

## Capture Setup

- Use a spare Android phone or emulator with a clean test account.
- Route device traffic through Burp Suite, mitmproxy, or Charles.
- Install the proxy CA certificate where permitted by the device/app configuration.
- Record app version, APK hash, device model, Android version, region, account state, and permission state.
- Keep raw captures private; publish only minimized evidence needed to support a claim.

## Baseline Flows

- Fresh install, first launch, no login.
- Login with a test account and capture account bootstrap traffic.
- Idle for 5-10 minutes after login.
- Browse feed, search, view profile, and open comments/messages if available.
- Grant and deny each sensitive permission, repeating the same flow after each change.
- Logout, force stop, relaunch, and compare persistent identifiers and post-logout traffic.

## Permission-Driven Checks

| Concern | Static evidence | Runtime flow | Traffic to inspect | Validation question |
| --- | --- | --- | --- | --- |
| Advertising identifier access | `android.permission.ACCESS_ADSERVICES_AD_ID` (advertising identifier) | Launch before login, login, browse feed, reset ad ID if possible, compare requests. | Advertising ID, app set ID, attribution IDs, ad SDK identifiers, consent fields. | Are advertising identifiers gated by platform policy and consent state? |
| Approximate location access | `android.permission.ACCESS_COARSE_LOCATION` (approximate location) | Launch app, browse feed, search, post content, and compare location granted versus denied. | Coarse location, region, city, geohash, IP-derived location labels. | Is approximate location use explained by the active feature or consent state? |
| Camera access | `android.permission.CAMERA` (camera) | Open camera, record video, upload a draft, deny camera and repeat. | Media upload metadata, camera mode flags, device/sensor metadata, unexpected background telemetry. | Is camera-related telemetry sent only after a clear camera-facing user action? |
| Contacts access | `android.permission.READ_CONTACTS` (contacts) | Open friend-finder/contact-sync flows before and after granting contacts. | Contact hashes, phone/email hashes, address-book counts, sync endpoints. | Are contacts or contact-derived identifiers transmitted only after consent? |
| External storage read access | `android.permission.READ_EXTERNAL_STORAGE` (external storage) | Open media picker, upload gallery media, deny storage/media permissions and repeat. | Local paths, filenames, media-library metadata, unexpected file inventory data. | Does traffic avoid leaking local file paths or unrelated storage metadata? |
| Image library access | `android.permission.READ_MEDIA_IMAGES` (images) | Upload an image from the gallery and compare with a camera-created image. | EXIF fields, filenames, media IDs, gallery metadata, upload side-channel metadata. | Is image metadata minimized before upload? |
| Video library access | `android.permission.READ_MEDIA_VIDEO` (videos) | Upload a video from the gallery and compare with an in-app recording. | EXIF/media metadata, filenames, codec metadata, local paths, upload identifiers. | Is video metadata minimized before upload? |
| Microphone access | `android.permission.RECORD_AUDIO` (microphone) | Record video with sound, use live/audio features, deny microphone and repeat. | Audio capture metadata, upload requests, feature flags, microphone permission state. | Is microphone-related data sent only during explicit recording or audio flows? |
| External storage write access | `android.permission.WRITE_EXTERNAL_STORAGE` (external storage writes) | Download media, save drafts, export edited video, then inspect local files and traffic. | Saved-file paths, cache identifiers, exported media metadata. | Are written files and related telemetry limited to expected user actions? |
| Google advertising identifier access | `com.google.android.gms.permission.AD_ID` (Google advertising identifier) | Launch before login, login, browse feed, reset ad ID if possible, compare requests. | Advertising ID, app set ID, attribution IDs, ad SDK identifiers, consent fields. | Are advertising identifiers gated by platform policy and consent state? |

## Source-Packet-Driven Checks

| Concern | Static evidence | Runtime flow | Traffic to inspect | Validation question |
| --- | --- | --- | --- | --- |
| Camera and microphone capture | `camera_microphone` in `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`, `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`, `smali_classes17/X/0eGv.1.smali` | Record, edit, upload, live/cast if available, deny permissions and repeat. | Capture metadata, upload metadata, audio/video feature flags, sensor state. | Is capture-related telemetry limited to explicit capture flows? |
| Command execution markers | `command_execution` in `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali` | Exercise media editing, diagnostics, live/cast, wallet/payment, and export flows. | Remote config or parameters that appear to influence local command behavior. | Is command execution reachable, and can any server/client input influence commands? |
| Contacts and accounts | `contacts_accounts` in `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`, `smali_classes17/X/0eGv.1.smali` | Find friends, contact sync, invite flows, account-linking flows. | Contact hashes, phone/email hashes, account identifiers, sync counts. | Is contact/account data sent only after clear consent? |
| Dynamic loading | `dynamic_loading` in `smali_classes17/X/0eGv.1.smali`, `smali_classes11/X/0PuX.2.smali` | Launch, login, open media effects, ads, live, payment, and plugin-like features. | Downloaded dex/jar/so files, plugin manifests, remote config enabling modules. | Is executable or plugin-like content fetched, verified, and scoped? |
| Device and advertising identifiers | `identifiers` in `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali`, `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`, `smali_classes17/X/0eGv.1.smali` | Cold launch, login, browse feed, open ads, reset advertising ID and repeat. | Advertising ID, Android ID, install ID, device ID, session IDs, hashed identifiers. | Which identifiers are transmitted, and are they resettable or user-controllable? |
| Installed-app or intent query behavior | `installed_apps` in `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`, `smali_classes17/X/0eGv.1.smali`, `smali_classes16/X/0awA.2.smali` | Share, login with third parties, open links, install/remove common apps and compare. | Package names, app-presence flags, capability probes, intent-resolution results. | Does the app transmit installed-app presence beyond user-triggered integrations? |
| Local persistence | `local_storage` in `smali_classes17/X/0eGv.1.smali`, `smali_classes17/X/0dMp.1.smali`, `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali` | Login, logout, save drafts, change privacy settings, inspect app data on a test device. | Tokens or identifiers echoed from local state, cache keys, preference-derived IDs. | Are sensitive local values protected and cleared after logout where appropriate? |
| Location access | `location` in `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`, `smali_classes17/X/0eGv.1.smali` | Browse feed, search, post with location, deny location and repeat. | Latitude/longitude, geohash, city/region, accuracy, permission state. | Does location traffic match a visible location feature? |
| Network telemetry | `network_telemetry` in `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali`, `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`, `smali_classes17/X/0eGv.1.smali` | Launch, idle, browse feed, search, view profile, post content, logout. | Event names, tap/scroll telemetry, profile/content IDs, third-party endpoints. | Is telemetry proportionate to the user-visible flow and consent state? |

## Exported Component Follow-Up

The static report lists 53 exported components. For privacy validation, prioritize components that process links, sharing, login, payment, media capture, or account authorization.

| Priority | Component |
| --- | --- |
| 1 | activity: com.aweme.account.login.OTLIntentHandlerActivity |
| 2 | activity: com.byted.cast.usbsource.usbdisplaysource.UsbSourceActivity |
| 3 | activity: com.bytedance.android.livesdk.game.broadcast.mirror.activity.UsbSourceProxyActivity |
| 4 | activity: com.bytedance.effectcreatormobile.creatortiktok.preview.CKENewEffectEditorActivity |
| 5 | activity: com.bytedance.effectcreatormobile.effectimgcreator.EffectImgCreatorActivity |
| 6 | activity: com.bytedance.globalpayment.googlepayapi.PIPOPayActivity |
| 7 | activity: com.bytedance.pipo.checkout.sdk.internal.CheckoutActivity |
| 8 | activity: com.bytedance.pipo.checkout.sdk.internal.PIManagementActivity |
| 9 | activity: com.bytedance.sdk.account.OneTapLoginActivity |
| 10 | activity: com.facebook.CustomTabActivity |
| 11 | activity: com.kakao.sdk.auth.AuthCodeHandlerActivity |
| 12 | activity: com.ss.android.account.share.data.write.activity.ShareDataActivity |
| 13 | activity: com.ss.android.sdk.activity.BootstrapActivity |
| 14 | activity: com.ss.android.ugc.aweme.deeplink.AppLinkHandlerV2 |
| 15 | activity: com.ss.android.ugc.aweme.deeplink.DeepLinkActivityV2 |

Only the first 15 exported components are listed here; total exported components: 53.

## Vulnerable Or High-Concern Traffic Patterns

- Sensitive identifiers or PII in URLs, query strings, referrers, logs, or third-party requests.
- Contacts, phone/email hashes, exact location, media metadata, or installed-app data sent before consent or without a visible related feature.
- Auth tokens, upload URLs, private media URLs, or account identifiers accepted across users or after logout.
- Server responses that expose private, deleted, draft, or account-scoped resources through predictable IDs.
- Remote configuration that changes privacy-sensitive collection without a corresponding local permission or consent state.
- Executable/plugin-like downloads or command parameters that are not clearly integrity-checked.

## Result Labels

- `observed`: captured in traffic or device state during a named flow.
- `not observed`: specifically tested in a named flow and not seen.
- `blocked`: not testable because of certificate pinning, login, region gating, feature flags, or missing device capability.
- `needs source review`: static signal exists, but runtime triggerability is unknown.

## Evidence Template

| Finding | Flow | Permission state | Endpoint/domain | Data observed | Evidence file | Label | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |
