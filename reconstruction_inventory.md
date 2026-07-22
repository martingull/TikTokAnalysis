# Reconstruction Inventory

This artifact ranks privacy-relevant smali files for source reconstruction. It is static evidence only.

## Corpus Summary

- Decompiled directory: `tiktok_decompiled`
- Candidate smali files from keyword discovery: 4922
- Files with privacy-relevant findings: 4922

## Category Totals

| Category | Matches |
| --- | ---: |
| `camera_microphone` | 3794 |
| `command_execution` | 18 |
| `contacts_accounts` | 164 |
| `dynamic_loading` | 4205 |
| `identifiers` | 632 |
| `installed_apps` | 17 |
| `local_storage` | 9265 |
| `location` | 271 |
| `network_telemetry` | 12703 |

## Keyword Totals

| Keyword | Matches |
| --- | ---: |
| `ACCESS_COARSE_LOCATION` | 67 |
| `ACCESS_FINE_LOCATION` | 10 |
| `AccountManager` | 113 |
| `AdvertisingId` | 217 |
| `Appsflyer` | 85 |
| `AudioRecord` | 3514 |
| `Camera;->open` | 3 |
| `ClassLoader` | 3248 |
| `ContactsContract` | 15 |
| `DexClassLoader` | 38 |
| `Firebase` | 456 |
| `HttpURLConnection` | 1993 |
| `LocationManager` | 99 |
| `MediaRecorder;->start` | 5 |
| `Method;->invoke` | 906 |
| `PathClassLoader` | 8 |
| `ProcessBuilder;->start` | 4 |
| `READ_CONTACTS` | 15 |
| `READ_EXTERNAL_STORAGE` | 46 |
| `RECORD_AUDIO` | 172 |
| `Runtime;->exec` | 14 |
| `SQLiteDatabase` | 1933 |
| `SharedPreferences` | 7190 |
| `System.loadLibrary` | 5 |
| `WRITE_EXTERNAL_STORAGE` | 85 |
| `ad_id` | 290 |
| `analytics` | 2552 |
| `android.permission.CAMERA` | 100 |
| `android_id` | 75 |
| `getAccounts` | 21 |
| `getAdvertisingIdInfo` | 11 |
| `getDeviceId` | 325 |
| `getInstalledPackages` | 3 |
| `getLastKnownLocation` | 11 |
| `getLatitude` | 43 |
| `getLongitude` | 41 |
| `getMacAddress` | 2 |
| `getSimSerialNumber` | 1 |
| `getSubscriberId` | 1 |
| `okhttp` | 1309 |
| `openOrCreateDatabase` | 11 |
| `queryIntentActivities` | 14 |
| `retrofit` | 6018 |

## Source Slices To Reconstruct First

### 1. `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali`

- Class: `Lcom/google/android/gms/ads/identifier/AdvertisingIdClient`
- Weighted score: 535
- Total matches: 54
- Categories: `identifiers`, `network_telemetry`
- Reconstruction note: `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali` maps to `Lcom/google/android/gms/ads/identifier/AdvertisingIdClient` and contains static references in these categories: identifiers, network_telemetry. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 1 | `identifiers` | `AdvertisingId` | `` | `.class public Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;` |
| 38 | `identifiers` | `AdvertisingId` | `.method public constructor <init>(ZLandroid/content/Context;Z)V` | `iput-object v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LIZLLL:Ljava/lang/Object;` |
| 53 | `identifiers` | `AdvertisingId` | `.method public constructor <init>(ZLandroid/content/Context;Z)V` | `iput-object p2, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJFF:Landroid/content/Context;` |
| 57 | `identifiers` | `AdvertisingId` | `.method public constructor <init>(ZLandroid/content/Context;Z)V` | `iput-boolean v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LIZJ:Z` |
| 61 | `identifiers` | `AdvertisingId` | `.method public constructor <init>(ZLandroid/content/Context;Z)V` | `iput-wide v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJII:J` |
| 63 | `identifiers` | `AdvertisingId` | `.method public constructor <init>(ZLandroid/content/Context;Z)V` | `iput-boolean p3, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJI:Z` |
| 229 | `identifiers` | `AdvertisingId` | `.method public static LIZLLL(LX/0dMc;)LX/0dWt;` | `const-string v0, "com.google.android.gms.ads.identifier.internal.IAdvertisingIdService"` |
| 334 | `identifiers` | `AdvertisingId` | `.method public static LJFF(Lcom/google/android/gms/ads/identifier/AdvertisingIdClient$Info;ZFJLjava/lang/String;Ljava/lang/Throwable;)V` | `.method public static LJFF(Lcom/google/android/gms/ads/identifier/AdvertisingIdClient$Info;ZFJLjava/lang/String;Ljava/lang/Throwable;)V` |
| 375 | `identifiers` | `AdvertisingId` | `.method public static LJFF(Lcom/google/android/gms/ads/identifier/AdvertisingIdClient$Info;ZFJLjava/lang/String;Ljava/lang/Throwable;)V` | `iget-boolean v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient$Info;->LIZIZ:Z` |
| 388 | `identifiers` | `AdvertisingId` | `.method public static LJFF(Lcom/google/android/gms/ads/identifier/AdvertisingIdClient$Info;ZFJLjava/lang/String;Ljava/lang/Throwable;)V` | `invoke-static {p0, v1}, LX/0eGv;->LLJJIJIIJIL(Lcom/google/android/gms/ads/identifier/AdvertisingIdClient$Info;Ljava/lang/String;)Ljava/lang/String;` |

### 2. `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`

- Class: `Lcom/bytedance/helios/statichook/config/ApiHookConfig`
- Weighted score: 623
- Total matches: 78
- Categories: `camera_microphone`, `contacts_accounts`, `identifiers`, `installed_apps`, `location`, `network_telemetry`
- Reconstruction note: `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali` maps to `Lcom/bytedance/helios/statichook/config/ApiHookConfig` and contains static references in these categories: camera_microphone, contacts_accounts, identifiers, installed_apps, location, network_telemetry. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 50 | `identifiers` | `getDeviceId` | `.method public static constructor <clinit>()V` | `const-string v0, "This class is used as a dictionary maintains.\nDictionary layout:\n    \|---- key: API ID, an integer value\n    \|---- value: {API ID, API name hash code,                   API related resource id(may be empty),                  API related resource name(maybe empty),                  permissions(maybe empty),                  permission type(anyOf/allOf, maybe empty),                  data types,                  monitor class hash code,                  invoke type (before or/and around)}\nIn runtime, TikTok will monitor these sensitive API usage according to this dictionary to make sure there is no misuse. For example *getDeviceId/getSSID...etc* is not allowed in TikTok. And the ActionInvokers are used to intercept the usage of these API"` |
| 193 | `network_telemetry` | `okhttp` | `.method public static LIZ()V` | `const-string v7, "okhttp3.OkHttpClient$Builder.build"` |
| 229 | `network_telemetry` | `okhttp` | `.method public static LIZ()V` | `const-string v7, "okhttp3.Call.execute"` |
| 263 | `network_telemetry` | `okhttp` | `.method public static LIZ()V` | `const-string v7, "okhttp3.Call.enqueue"` |
| 297 | `network_telemetry` | `retrofit` | `.method public static LIZ()V` | `const-string v7, "com.bytedance.retrofit2.Retrofit$Builder.build"` |
| 401 | `network_telemetry` | `retrofit` | `.method public static LIZ()V` | `const-string v7, "com.bytedance.retrofit2.SsHttpCall.execute"` |
| 435 | `network_telemetry` | `retrofit` | `.method public static LIZ()V` | `const-string v7, "com.bytedance.retrofit2.SsHttpCall.enqueue"` |
| 607 | `network_telemetry` | `Firebase` | `.method public static LIZ()V` | `const-string v7, "com.google.firebase.analytics.FirebaseAnalytics.setUserId"` |
| 607 | `network_telemetry` | `analytics` | `.method public static LIZ()V` | `const-string v7, "com.google.firebase.analytics.FirebaseAnalytics.setUserId"` |
| 639 | `network_telemetry` | `Firebase` | `.method public static LIZ()V` | `const-string v7, "com.google.firebase.analytics.FirebaseAnalytics.setUserProperty"` |

### 3. `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`

- Class: `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread`
- Weighted score: 2610
- Total matches: 290
- Categories: `camera_microphone`
- Reconstruction note: `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali` maps to `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread` and contains static references in these categories: camera_microphone. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 1 | `camera_microphone` | `AudioRecord` | `` | `.class public Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;` |
| 8 | `camera_microphone` | `AudioRecord` | `` | `value = Lcom/byted/cast/capture/audio/AudioRecorder;` |
| 18 | `camera_microphone` | `AudioRecord` | `` | `.field public final synthetic this$0:Lcom/byted/cast/capture/audio/AudioRecorder;` |
| 22 | `camera_microphone` | `AudioRecord` | `.method public constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;)V` | `.method public constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;)V` |
| 27 | `camera_microphone` | `AudioRecord` | `.method public constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;)V` | `iput-object p1, p0, Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;->this$0:Lcom/byted/cast/capture/audio/AudioRecorder;` |
| 39 | `camera_microphone` | `AudioRecord` | `.method public synthetic constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;Lcom/byted/cast/capture/audio/AudioRecorder$1;)V` | `.method public synthetic constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;Lcom/byted/cast/capture/audio/AudioRecorder$1;)V` |
| 44 | `camera_microphone` | `AudioRecord` | `.method public synthetic constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;Lcom/byted/cast/capture/audio/AudioRecorder$1;)V` | `invoke-direct {p0, p1}, Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;-><init>(Lcom/byted/cast/capture/audio/AudioRecorder;)V` |
| 59 | `camera_microphone` | `AudioRecord` | `.method private bpea_origin_run()V` | `invoke-static {p0}, Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;->com_byted_cast_capture_audio_AudioRecorder$AudioThread_com_ss_android_ugc_aweme_lancet_RunnableGuardLancet_run(Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;)V` |
| 66 | `camera_microphone` | `AudioRecord` | `.method public static com_byted_cast_capture_audio_AudioRecorder$AudioThread_com_ss_android_ugc_aweme_lancet_RunnableGuardLancet_run(Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;)V` | `.method public static com_byted_cast_capture_audio_AudioRecorder$AudioThread_com_ss_android_ugc_aweme_lancet_RunnableGuardLancet_run(Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;)V` |
| 82 | `camera_microphone` | `AudioRecord` | `.method public static com_byted_cast_capture_audio_AudioRecorder$AudioThread_com_ss_android_ugc_aweme_lancet_RunnableGuardLancet_run(Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;)V` | `invoke-virtual {p0}, Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;->com_byted_cast_capture_audio_AudioRecorder$AudioThread__run$___twin___()V` |

### 4. `smali_classes17/X/0eGv.1.smali`

- Class: `LX/0eGv`
- Weighted score: 1200
- Total matches: 149
- Categories: `camera_microphone`, `contacts_accounts`, `dynamic_loading`, `identifiers`, `installed_apps`, `local_storage`, `location`, `network_telemetry`
- Reconstruction note: `smali_classes17/X/0eGv.1.smali` maps to `LX/0eGv` and contains static references in these categories: camera_microphone, contacts_accounts, dynamic_loading, identifiers, installed_apps, local_storage, location, network_telemetry. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 7 | `contacts_accounts` | `AccountManager` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` |
| 59 | `contacts_accounts` | `AccountManager` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `const-string v14, "android/accounts/AccountManager"` |
| 63 | `contacts_accounts` | `getAccounts` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `const-string v15, "getAccounts"` |
| 112 | `contacts_accounts` | `AccountManager` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `const-string v6, "android/accounts/AccountManager"` |
| 116 | `contacts_accounts` | `getAccounts` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `const-string v7, "getAccounts"` |
| 145 | `contacts_accounts` | `getAccounts` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `invoke-virtual {v10}, Landroid/accounts/AccountManager;->getAccounts()[Landroid/accounts/Account;` |
| 145 | `contacts_accounts` | `AccountManager` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `invoke-virtual {v10}, Landroid/accounts/AccountManager;->getAccounts()[Landroid/accounts/Account;` |
| 153 | `contacts_accounts` | `AccountManager` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `const-string v6, "android/accounts/AccountManager"` |
| 157 | `contacts_accounts` | `getAccounts` | `.method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `const-string v7, "getAccounts"` |
| 177 | `contacts_accounts` | `AccountManager` | `.method public static LIZIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` | `.method public static LIZIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;` |

### 5. `smali_classes16/X/0awA.2.smali`

- Class: `LX/0awA`
- Weighted score: 16
- Total matches: 2
- Categories: `installed_apps`
- Reconstruction note: `smali_classes16/X/0awA.2.smali` maps to `LX/0awA` and contains static references in these categories: installed_apps. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 239 | `installed_apps` | `queryIntentActivities` | `.method public final LIZ(Landroid/content/Context;Ljava/lang/String;)Ljava/lang/String;` | `const-string v0, "pm.queryIntentActivities(activityIntent, 0)"` |
| 464 | `installed_apps` | `queryIntentActivities` | `.method public final LIZ(Landroid/content/Context;Ljava/lang/String;)Ljava/lang/String;` | `const-string v0, "pm.queryIntentActivities\u2026VED_FILTER,\n            )"` |

### 6. `smali_classes17/X/0dMp.1.smali`

- Class: `LX/0dMp`
- Weighted score: 567
- Total matches: 189
- Categories: `local_storage`
- Reconstruction note: `smali_classes17/X/0dMp.1.smali` maps to `LX/0dMp` and contains static references in these categories: local_storage. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 144 | `local_storage` | `SharedPreferences` | `` | `.field public final LLJ:Landroid/content/SharedPreferences;` |
| 610 | `local_storage` | `SharedPreferences` | `.method public constructor <init>(Landroid/content/Context;)V` | `invoke-static {v2, v1, v0}, LX/09yB;->LIZIZ(Landroid/content/Context;ILjava/lang/String;)Landroid/content/SharedPreferences;` |
| 618 | `local_storage` | `SharedPreferences` | `.method public constructor <init>(Landroid/content/Context;)V` | `iput-object v0, p0, LX/0dMp;->LLJ:Landroid/content/SharedPreferences;` |
| 1782 | `local_storage` | `SharedPreferences` | `.method public final LIZIZ()Ljava/util/List;` | `iget-object v1, p0, LX/0dMp;->LLJ:Landroid/content/SharedPreferences;` |
| 1819 | `local_storage` | `SharedPreferences` | `.method public final LIZIZ()Ljava/util/List;` | `invoke-interface {v1, v0, v3}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;` |
| 2694 | `local_storage` | `SharedPreferences` | `.method public final LJI()V` | `iget-object v1, p0, LX/0dMp;->LLJ:Landroid/content/SharedPreferences;` |
| 2702 | `local_storage` | `SharedPreferences` | `.method public final LJI()V` | `invoke-interface {v1, v0, v8}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;` |
| 2747 | `local_storage` | `SharedPreferences` | `.method public final LJI()V` | `iget-object v1, p0, LX/0dMp;->LLJ:Landroid/content/SharedPreferences;` |
| 2758 | `local_storage` | `SharedPreferences` | `.method public final LJI()V` | `invoke-interface {v1, v0, v7}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z` |
| 2770 | `local_storage` | `SharedPreferences` | `.method public final LJI()V` | `iget-object v3, p0, LX/0dMp;->LLJ:Landroid/content/SharedPreferences;` |

### 7. `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali`

- Class: `Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener`
- Weighted score: 1085
- Total matches: 217
- Categories: `network_telemetry`
- Reconstruction note: `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali` maps to `Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener` and contains static references in these categories: network_telemetry. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 1 | `network_telemetry` | `okhttp` | `` | `.class public Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;` |
| 17 | `network_telemetry` | `okhttp` | `` | `.field public okHttpRecord:Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;` |
| 54 | `network_telemetry` | `okhttp` | `.method public constructor <init>(LX/0dlz;)V` | `iput-boolean v0, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->needToDeal:Z` |
| 58 | `network_telemetry` | `okhttp` | `.method public constructor <init>(LX/0dlz;)V` | `iput-object p1, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->originListener:LX/0dlz;` |
| 62 | `network_telemetry` | `okhttp` | `.method public constructor <init>(LX/0dlz;)V` | `new-instance v0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;` |
| 66 | `network_telemetry` | `okhttp` | `.method public constructor <init>(LX/0dlz;)V` | `invoke-direct {v0}, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;-><init>()V` |
| 71 | `network_telemetry` | `okhttp` | `.method public constructor <init>(LX/0dlz;)V` | `iput-object v0, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->okHttpRecord:Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;` |
| 169 | `network_telemetry` | `okhttp` | `.method private dealSpecialHeader(LX/0dkV;)V` | `iget-object v0, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->okHttpRecord:Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;` |
| 173 | `network_telemetry` | `okhttp` | `.method private dealSpecialHeader(LX/0dkV;)V` | `iget-object v0, v0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;->headerRequest:Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord$HeaderRequest;` |
| 177 | `network_telemetry` | `okhttp` | `.method private dealSpecialHeader(LX/0dkV;)V` | `iget-object v0, v0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord$HeaderRequest;->serverTimings:Ljava/util/List;` |

### 8. `smali_classes11/X/0PuX.2.smali`

- Class: `LX/0PuX`
- Weighted score: 294
- Total matches: 42
- Categories: `dynamic_loading`
- Reconstruction note: `smali_classes11/X/0PuX.2.smali` maps to `LX/0PuX` and contains static references in these categories: dynamic_loading. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 111 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v1}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;` |
| 119 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v0, v1}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;` |
| 252 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v1}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;` |
| 260 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v0, v1}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;` |
| 380 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v1}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;` |
| 388 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v0, v1}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;` |
| 474 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v1}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;` |
| 482 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v0, v1}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;` |
| 540 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v1}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;` |
| 548 | `dynamic_loading` | `ClassLoader` | `.method public final createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;` | `invoke-virtual {v0, v1}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;` |

### 9. `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali`

- Class: `Lcom/bytedance/android/live/wallet/WalletExchange`
- Weighted score: 43
- Total matches: 13
- Categories: `command_execution`, `local_storage`
- Reconstruction note: `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali` maps to `Lcom/bytedance/android/live/wallet/WalletExchange` and contains static references in these categories: command_execution, local_storage. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 685 | `command_execution` | `Runtime;->exec` | `.method public static LJIJI()Ljava/util/Locale;` | `invoke-virtual {v2, v0}, Ljava/lang/Runtime;->exec([Ljava/lang/String;)Ljava/lang/Process;` |
| 856 | `local_storage` | `SharedPreferences` | `.method public static LJJIIZ(Z)V` | `invoke-static {}, LX/0gJg;->LIZJ()Landroid/content/SharedPreferences;` |
| 864 | `local_storage` | `SharedPreferences` | `.method public static LJJIIZ(Z)V` | `invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;` |
| 876 | `local_storage` | `SharedPreferences` | `.method public static LJJIIZ(Z)V` | `invoke-interface {v1, v0, v2}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;` |
| 884 | `local_storage` | `SharedPreferences` | `.method public static LJJIIZ(Z)V` | `invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V` |
| 938 | `local_storage` | `SharedPreferences` | `.method public static LJJIIZI(Z)V` | `invoke-static {}, LX/0gJg;->LIZJ()Landroid/content/SharedPreferences;` |
| 946 | `local_storage` | `SharedPreferences` | `.method public static LJJIIZI(Z)V` | `invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;` |
| 958 | `local_storage` | `SharedPreferences` | `.method public static LJJIIZI(Z)V` | `invoke-interface {v1, v0, v2}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;` |
| 966 | `local_storage` | `SharedPreferences` | `.method public static LJJIIZI(Z)V` | `invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V` |
| 2894 | `local_storage` | `SharedPreferences` | `.method public final LJIIL()Z` | `invoke-static {}, LX/0gJg;->LIZJ()Landroid/content/SharedPreferences;` |

### 10. `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali`

- Class: `Lcom/ss/android/vesdk/audio/TEAudioRecord`
- Weighted score: 1386
- Total matches: 154
- Categories: `camera_microphone`
- Reconstruction note: `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali` maps to `Lcom/ss/android/vesdk/audio/TEAudioRecord` and contains static references in these categories: camera_microphone. Treat this as source-reconstruction evidence that the class participates in these capability areas; runtime triggering still requires dynamic validation.

| Line | Category | Keyword | Method | Code |
| ---: | --- | --- | --- | --- |
| 1 | `camera_microphone` | `AudioRecord` | `` | `.class public Lcom/ss/android/vesdk/audio/TEAudioRecord;` |
| 24 | `camera_microphone` | `AudioRecord` | `` | `.field public mAudioRecord:Landroid/media/AudioRecord;` |
| 26 | `camera_microphone` | `AudioRecord` | `` | `.field public mAudioRecordStartTime:J` |
| 28 | `camera_microphone` | `AudioRecord` | `` | `.field public mAudioRecordStopTime:J` |
| 67 | `camera_microphone` | `AudioRecord` | `.method public static constructor <clinit>()V` | `const-string v0, "TEAudioRecord"` |
| 71 | `camera_microphone` | `AudioRecord` | `.method public static constructor <clinit>()V` | `sput-object v0, Lcom/ss/android/vesdk/audio/TEAudioRecord;->TAG:Ljava/lang/String;` |
| 87 | `camera_microphone` | `AudioRecord` | `.method public static constructor <clinit>()V` | `sput-object v0, Lcom/ss/android/vesdk/audio/TEAudioRecord;->SUGGEST_SAMPLERATE_ARRAY:[I` |
| 103 | `camera_microphone` | `AudioRecord` | `.method public static constructor <clinit>()V` | `sput-object v0, Lcom/ss/android/vesdk/audio/TEAudioRecord;->SUGGEST_CHANNEL_ARRAY:[I` |
| 160 | `camera_microphone` | `AudioRecord` | `.method public constructor <init>()V` | `iput v0, p0, Lcom/ss/android/vesdk/audio/TEAudioRecord;->mSampleRate:I` |
| 167 | `camera_microphone` | `AudioRecord` | `.method public constructor <init>()V` | `iput v0, p0, Lcom/ss/android/vesdk/audio/TEAudioRecord;->mChannels:I` |
