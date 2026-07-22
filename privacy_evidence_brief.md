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
| 2 | smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali | Lcom/bytedance/helios/statichook/config/ApiHookConfig | not supplied | camera_microphone, contacts_accounts, identifiers, installed_apps, location, network_telemetry | 50:identifiers:getDeviceId, 193:network_telemetry:okhttp, 229:network_telemetry:okhttp |
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
- JADX source: `not supplied`
- Categories: `camera_microphone`, `contacts_accounts`, `identifiers`, `installed_apps`, `location`, `network_telemetry`

Smali evidence:
- Line 50, `identifiers`, `getDeviceId`: `const-string v0, "This class is used as a dictionary maintains.\nDictionary layout:\n |---- key: API ID, an integer value\n |---- value: {API ID, API name hash code, API related resource id(may be empty), API related resource name(maybe empty), permissions(maybe empty), permis...`
- Line 193, `network_telemetry`, `okhttp`: `const-string v7, "okhttp3.OkHttpClient$Builder.build"`

#### `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`

- Class: `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread`
- JADX source: `not supplied`
- Categories: `camera_microphone`

Smali evidence:
- Line 1, `camera_microphone`, `AudioRecord`: `.class public Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;`
- Line 8, `camera_microphone`, `AudioRecord`: `value = Lcom/byted/cast/capture/audio/AudioRecorder;`


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
