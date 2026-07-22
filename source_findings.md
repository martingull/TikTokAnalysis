# Source Findings Review Packets

This artifact is the Path 2 working layer. It uses JADX as the reading layer when Java-like source is available and apktool smali as the evidence layer for line-cited review.

It is not a final report. Each packet needs manual reconstruction notes before it should support a publishable claim.

## Strategy

- Reading layer: JADX Java-like source when available
- Evidence layer: apktool smali with line-numbered context
- Scope: selected privacy/security source slices, not whole-app reconstruction

## Packets

### 1. `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali`

- Class: `Lcom/google/android/gms/ads/identifier/AdvertisingIdClient`
- JADX source: `not found`
- Categories: `identifiers`, `network_telemetry`
- Total matches: 54
- Weighted score: 535

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 1, `identifiers`, `AdvertisingId`

```smali
1: .class public Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;
2: .super Ljava/lang/Object;
3: .source "SourceFile"
4: 
5: 
6: # instance fields
7: .field public LIZ:LX/0dMc;
```

- Line 38, `identifiers`, `AdvertisingId`

```smali
32:     invoke-static {v2}, Lcom/bytedance/frameworks/apm/trace/MethodCollector;->i(I)V
33: 
34:     new-instance v0, Ljava/lang/Object;
35: 
36:     invoke-direct {v0}, Ljava/lang/Object;-><init>()V
37: 
38:     iput-object v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LIZLLL:Ljava/lang/Object;
39: 
40:     invoke-static {p2}, LX/0dVi;->LJIIIZ(Ljava/lang/Object;)V
41: 
42:     if-eqz p1, :cond_0
43: 
44:     invoke-static {p2}, LX/0pW5;->T(Landroid/content/Context;)Landroid/content/Context;
```

- Line 53, `identifiers`, `AdvertisingId`

```smali
47: 
48:     if-eqz v0, :cond_0
49: 
50:     move-object p2, v0
51: 
52:     :cond_0
53:     iput-object p2, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJFF:Landroid/content/Context;
54: 
55:     const/4 v0, 0x0
56: 
57:     iput-boolean v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LIZJ:Z
58: 
59:     const-wide/16 v0, -0x1
```

- Line 57, `identifiers`, `AdvertisingId`

```smali
51: 
52:     :cond_0
53:     iput-object p2, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJFF:Landroid/content/Context;
54: 
55:     const/4 v0, 0x0
56: 
57:     iput-boolean v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LIZJ:Z
58: 
59:     const-wide/16 v0, -0x1
60: 
61:     iput-wide v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJII:J
62: 
63:     iput-boolean p3, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJI:Z
```

- Line 61, `identifiers`, `AdvertisingId`

```smali
55:     const/4 v0, 0x0
56: 
57:     iput-boolean v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LIZJ:Z
58: 
59:     const-wide/16 v0, -0x1
60: 
61:     iput-wide v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJII:J
62: 
63:     iput-boolean p3, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJI:Z
64: 
65:     invoke-static {v2}, Lcom/bytedance/frameworks/apm/trace/MethodCollector;->o(I)V
66: 
67:     return-void
```

- Line 63, `identifiers`, `AdvertisingId`

```smali
57:     iput-boolean v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LIZJ:Z
58: 
59:     const-wide/16 v0, -0x1
60: 
61:     iput-wide v0, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJII:J
62: 
63:     iput-boolean p3, p0, Lcom/google/android/gms/ads/identifier/AdvertisingIdClient;->LJI:Z
64: 
65:     invoke-static {v2}, Lcom/bytedance/frameworks/apm/trace/MethodCollector;->o(I)V
66: 
67:     return-void
68: .end method
69: 
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 2. `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali`

- Class: `Lcom/bytedance/helios/statichook/config/ApiHookConfig`
- JADX source: `not found`
- Categories: `camera_microphone`, `contacts_accounts`, `identifiers`, `installed_apps`, `location`, `network_telemetry`
- Total matches: 78
- Weighted score: 623

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 50, `identifiers`, `getDeviceId`

```smali
44:     .line 3
45:     invoke-static {v1}, Lcom/bytedance/frameworks/apm/trace/MethodCollector;->i(I)V
46: 
47:     .line 4
48:     .line 5
49:     .line 6
50:     const-string v0, "This class is used as a dictionary maintains.\nDictionary layout:\n    |---- key: API ID, an integer value\n    |---- value: {API ID, API name hash code,                   API related resource id(may be empty),                  API related resource name(maybe empty),                  permissions(maybe empty),                  permission type(anyOf/allOf, maybe empty),                  data types,                  monitor class hash code,                  invoke type (before or/and around)}\nIn runtime, TikTok will monitor these sensitive API usage according to this dictionary to make sure there is no misuse. For example *getDeviceId/getSSID...etc* is not allowed in TikTok. And the ActionInvokers are used to intercept the usage of these API"
51: 
52:     .line 7
53:     .line 8
54:     sput-object v0, Lcom/bytedance/helios/statichook/config/ApiHookConfig;->desc:Ljava/lang/String;
55: 
56:     .line 9
```

- Line 193, `network_telemetry`, `okhttp`

```smali
187:     move-result-object v1
188: 
189:     new-instance v5, LX/0eSA;
190: 
191:     const v6, 0x61ae4
192: 
193:     const-string v7, "okhttp3.OkHttpClient$Builder.build"
194: 
195:     const-string v8, "oh"
196: 
197:     const-string v9, "OkHttp"
198: 
199:     new-array v10, v0, [Ljava/lang/String;
```

- Line 229, `network_telemetry`, `okhttp`

```smali
223:     move-result-object v1
224: 
225:     new-instance v5, LX/0eSA;
226: 
227:     const v6, 0x61ae6
228: 
229:     const-string v7, "okhttp3.Call.execute"
230: 
231:     const-string v8, "oh"
232: 
233:     const-string v9, "OkHttp"
234: 
235:     new-array v10, v0, [Ljava/lang/String;
```

- Line 263, `network_telemetry`, `okhttp`

```smali
257:     move-result-object v1
258: 
259:     new-instance v5, LX/0eSA;
260: 
261:     const v6, 0x61ae7
262: 
263:     const-string v7, "okhttp3.Call.enqueue"
264: 
265:     const-string v8, "oh"
266: 
267:     const-string v9, "OkHttp"
268: 
269:     new-array v10, v0, [Ljava/lang/String;
```

- Line 297, `network_telemetry`, `retrofit`

```smali
291:     move-result-object v1
292: 
293:     new-instance v5, LX/0eSA;
294: 
295:     const v6, 0x61b48
296: 
297:     const-string v7, "com.bytedance.retrofit2.Retrofit$Builder.build"
298: 
299:     const-string/jumbo v8, "ttn"
300: 
301:     const-string v9, "TTNet"
302: 
303:     new-array v10, v0, [Ljava/lang/String;
```

- Line 401, `network_telemetry`, `retrofit`

```smali
395:     move-result-object v1
396: 
397:     new-instance v5, LX/0eSA;
398: 
399:     const v6, 0x61b4c
400: 
401:     const-string v7, "com.bytedance.retrofit2.SsHttpCall.execute"
402: 
403:     const-string/jumbo v8, "ttn"
404: 
405:     const-string v9, "TTNet"
406: 
407:     new-array v10, v0, [Ljava/lang/String;
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 3. `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali`

- Class: `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread`
- JADX source: `not found`
- Categories: `camera_microphone`
- Total matches: 290
- Weighted score: 2610

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 1, `camera_microphone`, `AudioRecord`

```smali
1: .class public Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;
2: .super Lcom/bytedance/bpea/transmit/delegate/BPEAThread;
3: .source "SourceFile"
4: 
5: 
6: # annotations
7: .annotation system Ldalvik/annotation/EnclosingClass;
```

- Line 8, `camera_microphone`, `AudioRecord`

```smali
2: .super Lcom/bytedance/bpea/transmit/delegate/BPEAThread;
3: .source "SourceFile"
4: 
5: 
6: # annotations
7: .annotation system Ldalvik/annotation/EnclosingClass;
8:     value = Lcom/byted/cast/capture/audio/AudioRecorder;
9: .end annotation
10: 
11: .annotation system Ldalvik/annotation/InnerClass;
12:     accessFlags = 0x1
13:     name = "AudioThread"
14: .end annotation
```

- Line 18, `camera_microphone`, `AudioRecord`

```smali
12:     accessFlags = 0x1
13:     name = "AudioThread"
14: .end annotation
15: 
16: 
17: # instance fields
18: .field public final synthetic this$0:Lcom/byted/cast/capture/audio/AudioRecorder;
19: 
20: 
21: # direct methods
22: .method public constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;)V
23:     .locals 0
24: 
```

- Line 22, `camera_microphone`, `AudioRecord`

```smali
16: 
17: # instance fields
18: .field public final synthetic this$0:Lcom/byted/cast/capture/audio/AudioRecorder;
19: 
20: 
21: # direct methods
22: .method public constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;)V
23:     .locals 0
24: 
25:     .prologue
26:     .line 16777216
27:     iput-object p1, p0, Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;->this$0:Lcom/byted/cast/capture/audio/AudioRecorder;
28: 
```

- Line 27, `camera_microphone`, `AudioRecord`

```smali
21: # direct methods
22: .method public constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;)V
23:     .locals 0
24: 
25:     .prologue
26:     .line 16777216
27:     iput-object p1, p0, Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;->this$0:Lcom/byted/cast/capture/audio/AudioRecorder;
28: 
29:     .line 16777217
30:     .line 16777218
31:     invoke-direct {p0}, Lcom/bytedance/bpea/transmit/delegate/BPEAThread;-><init>()V
32: 
33:     .line 16777219
```

- Line 39, `camera_microphone`, `AudioRecord`

```smali
33:     .line 16777219
34:     .line 16777220
35:     .line 16777221
36:     return-void
37: .end method
38: 
39: .method public synthetic constructor <init>(Lcom/byted/cast/capture/audio/AudioRecorder;Lcom/byted/cast/capture/audio/AudioRecorder$1;)V
40:     .locals 0
41: 
42:     .prologue
43:     .line 33554432
44:     invoke-direct {p0, p1}, Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread;-><init>(Lcom/byted/cast/capture/audio/AudioRecorder;)V
45: 
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 4. `smali_classes17/X/0eGv.1.smali`

- Class: `LX/0eGv`
- JADX source: `not found`
- Categories: `camera_microphone`, `contacts_accounts`, `dynamic_loading`, `identifiers`, `installed_apps`, `local_storage`, `location`, `network_telemetry`
- Total matches: 149
- Weighted score: 1200

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 7, `contacts_accounts`, `AccountManager`

```smali
1: .class public final LX/0eGv;
2: .super Ljava/lang/Object;
3: .source "SourceFile"
4: 
5: 
6: # direct methods
7: .method public static LIZ(Landroid/accounts/AccountManager;Ljava/lang/String;)[Landroid/accounts/Account;
8:     .locals 19
9: 
10:     .prologue
11:     .line 33554432
12:     const/16 v2, 0x5eba
13: 
```

- Line 59, `contacts_accounts`, `AccountManager`

```smali
53:     .line 33554454
54:     const v5, 0x19064
55: 
56:     .line 33554455
57:     .line 33554456
58:     .line 33554457
59:     const-string v14, "android/accounts/AccountManager"
60: 
61:     .line 33554458
62:     .line 33554459
63:     const-string v15, "getAccounts"
64: 
65:     .line 33554460
```

- Line 63, `contacts_accounts`, `getAccounts`

```smali
57:     .line 33554456
58:     .line 33554457
59:     const-string v14, "android/accounts/AccountManager"
60: 
61:     .line 33554458
62:     .line 33554459
63:     const-string v15, "getAccounts"
64: 
65:     .line 33554460
66:     .line 33554461
67:     const-string v18, "android.accounts.Account[]"
68: 
69:     .line 33554462
```

- Line 112, `contacts_accounts`, `AccountManager`

```smali
106: 
107:     .line 33554480
108:     .line 33554481
109:     const/4 v8, 0x0
110: 
111:     .line 33554482
112:     const-string v6, "android/accounts/AccountManager"
113: 
114:     .line 33554483
115:     .line 33554484
116:     const-string v7, "getAccounts"
117: 
118:     .line 33554485
```

- Line 116, `contacts_accounts`, `getAccounts`

```smali
110: 
111:     .line 33554482
112:     const-string v6, "android/accounts/AccountManager"
113: 
114:     .line 33554483
115:     .line 33554484
116:     const-string v7, "getAccounts"
117: 
118:     .line 33554485
119:     .line 33554486
120:     const/4 v12, 0x0
121: 
122:     .line 33554487
```

- Line 145, `contacts_accounts`, `getAccounts`

```smali
139:     .line 33554496
140:     .line 33554497
141:     return-object v0
142: 
143:     .line 33554498
144:     :cond_0
145:     invoke-virtual {v10}, Landroid/accounts/AccountManager;->getAccounts()[Landroid/accounts/Account;
146: 
147:     .line 33554499
148:     .line 33554500
149:     .line 33554501
150:     move-result-object v8
151: 
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 5. `smali_classes16/X/0awA.2.smali`

- Class: `LX/0awA`
- JADX source: `not found`
- Categories: `installed_apps`
- Total matches: 2
- Weighted score: 16

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 239, `installed_apps`, `queryIntentActivities`

```smali
233:     .line 33554507
234:     .line 33554508
235:     .line 33554509
236:     move-result-object v9
237: 
238:     .line 33554510
239:     const-string v0, "pm.queryIntentActivities(activityIntent, 0)"
240: 
241:     .line 33554511
242:     .line 33554512
243:     invoke-static {v9, v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullExpressionValue(Ljava/lang/Object;Ljava/lang/String;)V
244: 
245:     .line 33554513
```

- Line 464, `installed_apps`, `queryIntentActivities`

```smali
458:     .line 33554617
459:     .line 33554618
460:     .line 33554619
461:     move-result-object v1
462: 
463:     .line 33554620
464:     const-string v0, "pm.queryIntentActivities\u2026VED_FILTER,\n            )"
465: 
466:     .line 33554621
467:     .line 33554622
468:     invoke-static {v1, v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullExpressionValue(Ljava/lang/Object;Ljava/lang/String;)V
469: 
470:     .line 33554623
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 6. `smali_classes17/X/0dMp.1.smali`

- Class: `LX/0dMp`
- JADX source: `not found`
- Categories: `local_storage`
- Total matches: 189
- Weighted score: 567

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 144, `local_storage`, `SharedPreferences`

```smali
138: .field public LLILZLL:Z
139: 
140: .field public LLIZ:Landroid/content/Context;
141: 
142: .field public final LLIZLLLIL:Lcom/bytedance/common/utility/collection/WeakHandler;
143: 
144: .field public final LLJ:Landroid/content/SharedPreferences;
145: 
146: .field public final LLJI:LX/0jAh;
147:     .annotation system Ldalvik/annotation/Signature;
148:         value = {
149:             "LX/0jAh<",
150:             "LX/0dJs;",
```

- Line 610, `local_storage`, `SharedPreferences`

```smali
604: 
605:     .line 16777292
606:     .line 16777293
607:     const/4 v1, 0x0
608: 
609:     .line 16777294
610:     invoke-static {v2, v1, v0}, LX/09yB;->LIZIZ(Landroid/content/Context;ILjava/lang/String;)Landroid/content/SharedPreferences;
611: 
612:     .line 16777295
613:     .line 16777296
614:     .line 16777297
615:     move-result-object v0
616: 
```

- Line 618, `local_storage`, `SharedPreferences`

```smali
612:     .line 16777295
613:     .line 16777296
614:     .line 16777297
615:     move-result-object v0
616: 
617:     .line 16777298
618:     iput-object v0, p0, LX/0dMp;->LLJ:Landroid/content/SharedPreferences;
619: 
620:     .line 16777299
621:     .line 16777300
622:     iput-boolean v1, p0, LX/0dMp;->LLILZLL:Z
623: 
624:     .line 16777301
```

- Line 1782, `local_storage`, `SharedPreferences`

```smali
1776:     .line 5
1777:     .line 6
1778:     sget-object v0, LX/0dLK;->LIZ:LX/0dLK;
1779: 
1780:     .line 7
1781:     .line 8
1782:     iget-object v1, p0, LX/0dMp;->LLJ:Landroid/content/SharedPreferences;
1783: 
1784:     .line 9
1785:     .line 10
1786:     invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;
1787: 
1788:     .line 11
```

- Line 1819, `local_storage`, `SharedPreferences`

```smali
1813:     .line 26
1814:     .line 27
1815:     const-string v3, ""
1816: 
1817:     .line 28
1818:     .line 29
1819:     invoke-interface {v1, v0, v3}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
1820: 
1821:     .line 30
1822:     .line 31
1823:     .line 32
1824:     move-result-object v0
1825: 
```

- Line 2694, `local_storage`, `SharedPreferences`

```smali
2688:     .line 20
2689:     :try_start_0
2690:     new-instance v2, Lorg/json/JSONObject;
2691: 
2692:     .line 21
2693:     .line 22
2694:     iget-object v1, p0, LX/0dMp;->LLJ:Landroid/content/SharedPreferences;
2695: 
2696:     .line 23
2697:     .line 24
2698:     const-string v0, "raw_json"
2699: 
2700:     .line 25
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 7. `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali`

- Class: `Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener`
- JADX source: `not found`
- Categories: `network_telemetry`
- Total matches: 217
- Weighted score: 1085

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 1, `network_telemetry`, `okhttp`

```smali
1: .class public Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;
2: .super LX/0dlz;
3: .source "SourceFile"
4: 
5: 
6: # static fields
7: .field public static sIgnoreMonitorLabel:Ljava/lang/String;
```

- Line 17, `network_telemetry`, `okhttp`

```smali
11: .field public connectStartTime:J
12: 
13: .field public dnsStartTime:J
14: 
15: .field public needToDeal:Z
16: 
17: .field public okHttpRecord:Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;
18: 
19: .field public originListener:LX/0dlz;
20: 
21: .field public requestBodyEndTime:J
22: 
23: .field public requestHeader:Lorg/json/JSONObject;
```

- Line 54, `network_telemetry`, `okhttp`

```smali
48:     .line 16777217
49:     .line 16777218
50:     .line 16777219
51:     const/4 v0, 0x1
52: 
53:     .line 16777220
54:     iput-boolean v0, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->needToDeal:Z
55: 
56:     .line 16777221
57:     .line 16777222
58:     iput-object p1, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->originListener:LX/0dlz;
59: 
60:     .line 16777223
```

- Line 58, `network_telemetry`, `okhttp`

```smali
52: 
53:     .line 16777220
54:     iput-boolean v0, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->needToDeal:Z
55: 
56:     .line 16777221
57:     .line 16777222
58:     iput-object p1, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->originListener:LX/0dlz;
59: 
60:     .line 16777223
61:     .line 16777224
62:     new-instance v0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;
63: 
64:     .line 16777225
```

- Line 62, `network_telemetry`, `okhttp`

```smali
56:     .line 16777221
57:     .line 16777222
58:     iput-object p1, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->originListener:LX/0dlz;
59: 
60:     .line 16777223
61:     .line 16777224
62:     new-instance v0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;
63: 
64:     .line 16777225
65:     .line 16777226
66:     invoke-direct {v0}, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;-><init>()V
67: 
68:     .line 16777227
```

- Line 66, `network_telemetry`, `okhttp`

```smali
60:     .line 16777223
61:     .line 16777224
62:     new-instance v0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;
63: 
64:     .line 16777225
65:     .line 16777226
66:     invoke-direct {v0}, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;-><init>()V
67: 
68:     .line 16777227
69:     .line 16777228
70:     .line 16777229
71:     iput-object v0, p0, Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener;->okHttpRecord:Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpRecord;
72: 
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 8. `smali_classes11/X/0PuX.2.smali`

- Class: `LX/0PuX`
- JADX source: `not found`
- Categories: `dynamic_loading`
- Total matches: 42
- Weighted score: 294

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 111, `dynamic_loading`, `ClassLoader`

```smali
105:     .line 16777248
106:     .line 16777249
107:     const-class v1, Lcom/ss/android/ugc/aweme/creative/model/stickers/StickerNewEngineModel;
108: 
109:     .line 16777250
110:     .line 16777251
111:     invoke-virtual {v1}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;
112: 
113:     .line 16777252
114:     .line 16777253
115:     .line 16777254
116:     move-result-object v1
117: 
```

- Line 119, `dynamic_loading`, `ClassLoader`

```smali
113:     .line 16777252
114:     .line 16777253
115:     .line 16777254
116:     move-result-object v1
117: 
118:     .line 16777255
119:     invoke-virtual {v0, v1}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;
120: 
121:     .line 16777256
122:     .line 16777257
123:     .line 16777258
124:     move-result-object v2
125: 
```

- Line 252, `dynamic_loading`, `ClassLoader`

```smali
246:     .line 16777316
247:     .line 16777317
248:     const-class v1, Lcom/ss/android/ugc/aweme/creative/model/stickers/StickerNewEngineModel;
249: 
250:     .line 16777318
251:     .line 16777319
252:     invoke-virtual {v1}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;
253: 
254:     .line 16777320
255:     .line 16777321
256:     .line 16777322
257:     move-result-object v1
258: 
```

- Line 260, `dynamic_loading`, `ClassLoader`

```smali
254:     .line 16777320
255:     .line 16777321
256:     .line 16777322
257:     move-result-object v1
258: 
259:     .line 16777323
260:     invoke-virtual {v0, v1}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;
261: 
262:     .line 16777324
263:     .line 16777325
264:     .line 16777326
265:     move-result-object v2
266: 
```

- Line 380, `dynamic_loading`, `ClassLoader`

```smali
374:     .line 16777377
375:     .line 16777378
376:     const-class v1, Lcom/ss/android/ugc/aweme/creative/model/stickers/StickerNewEngineModel;
377: 
378:     .line 16777379
379:     .line 16777380
380:     invoke-virtual {v1}, Ljava/lang/Class;->getClassLoader()Ljava/lang/ClassLoader;
381: 
382:     .line 16777381
383:     .line 16777382
384:     .line 16777383
385:     move-result-object v1
386: 
```

- Line 388, `dynamic_loading`, `ClassLoader`

```smali
382:     .line 16777381
383:     .line 16777382
384:     .line 16777383
385:     move-result-object v1
386: 
387:     .line 16777384
388:     invoke-virtual {v0, v1}, Landroid/os/Parcel;->readParcelable(Ljava/lang/ClassLoader;)Landroid/os/Parcelable;
389: 
390:     .line 16777385
391:     .line 16777386
392:     .line 16777387
393:     move-result-object v2
394: 
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 9. `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali`

- Class: `Lcom/bytedance/android/live/wallet/WalletExchange`
- JADX source: `not found`
- Categories: `command_execution`, `local_storage`
- Total matches: 13
- Weighted score: 43

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 685, `command_execution`, `Runtime;->exec`

```smali
679:     .line 20
680:     .line 21
681:     .line 22
682:     move-result-object v0
683: 
684:     .line 23
685:     invoke-virtual {v2, v0}, Ljava/lang/Runtime;->exec([Ljava/lang/String;)Ljava/lang/Process;
686: 
687:     .line 24
688:     .line 25
689:     .line 26
690:     move-result-object v3
691: 
```

- Line 856, `local_storage`, `SharedPreferences`

```smali
850:     .line 16777228
851:     invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;
852: 
853:     .line 16777229
854:     .line 16777230
855:     .line 16777231
856:     invoke-static {}, LX/0gJg;->LIZJ()Landroid/content/SharedPreferences;
857: 
858:     .line 16777232
859:     .line 16777233
860:     .line 16777234
861:     move-result-object v0
862: 
```

- Line 864, `local_storage`, `SharedPreferences`

```smali
858:     .line 16777232
859:     .line 16777233
860:     .line 16777234
861:     move-result-object v0
862: 
863:     .line 16777235
864:     invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;
865: 
866:     .line 16777236
867:     .line 16777237
868:     .line 16777238
869:     move-result-object v1
870: 
```

- Line 876, `local_storage`, `SharedPreferences`

```smali
870: 
871:     .line 16777239
872:     const-string v0, "live_revenue_auto_exchange"
873: 
874:     .line 16777240
875:     .line 16777241
876:     invoke-interface {v1, v0, v2}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
877: 
878:     .line 16777242
879:     .line 16777243
880:     .line 16777244
881:     move-result-object v0
882: 
```

- Line 884, `local_storage`, `SharedPreferences`

```smali
878:     .line 16777242
879:     .line 16777243
880:     .line 16777244
881:     move-result-object v0
882: 
883:     .line 16777245
884:     invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V
885: 
886:     .line 16777246
887:     .line 16777247
888:     .line 16777248
889:     invoke-static {v3}, Lcom/bytedance/frameworks/apm/trace/MethodCollector;->o(I)V
890: 
```

- Line 938, `local_storage`, `SharedPreferences`

```smali
932:     .line 16777228
933:     invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;
934: 
935:     .line 16777229
936:     .line 16777230
937:     .line 16777231
938:     invoke-static {}, LX/0gJg;->LIZJ()Landroid/content/SharedPreferences;
939: 
940:     .line 16777232
941:     .line 16777233
942:     .line 16777234
943:     move-result-object v0
944: 
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.

### 10. `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali`

- Class: `Lcom/ss/android/vesdk/audio/TEAudioRecord`
- JADX source: `not found`
- Categories: `camera_microphone`
- Total matches: 154
- Weighted score: 1386

#### Manual Review Template

- Reconstructed behavior:
- Data touched:
- Input source: `unknown`
- Runtime observed: `false`
- Confidence: `needs manual review`
- Report finding supported:
- Open questions:

#### Smali Evidence

- Line 1, `camera_microphone`, `AudioRecord`

```smali
1: .class public Lcom/ss/android/vesdk/audio/TEAudioRecord;
2: .super Ljava/lang/Object;
3: .source "SourceFile"
4: 
5: # interfaces
6: .implements LX/0hAt;
7: 
```

- Line 24, `camera_microphone`, `AudioRecord`

```smali
18: .field public hasInited:I
19: 
20: .field public mAudioCallback:LX/0hAi;
21: 
22: .field public mAudioCaptureSettings:Lcom/ss/android/vesdk/VEAudioCaptureSettings;
23: 
24: .field public mAudioRecord:Landroid/media/AudioRecord;
25: 
26: .field public mAudioRecordStartTime:J
27: 
28: .field public mAudioRecordStopTime:J
29: 
30: .field public mAudioSource:I
```

- Line 26, `camera_microphone`, `AudioRecord`

```smali
20: .field public mAudioCallback:LX/0hAi;
21: 
22: .field public mAudioCaptureSettings:Lcom/ss/android/vesdk/VEAudioCaptureSettings;
23: 
24: .field public mAudioRecord:Landroid/media/AudioRecord;
25: 
26: .field public mAudioRecordStartTime:J
27: 
28: .field public mAudioRecordStopTime:J
29: 
30: .field public mAudioSource:I
31: 
32: .field public mBitsPerSample:I
```

- Line 28, `camera_microphone`, `AudioRecord`

```smali
22: .field public mAudioCaptureSettings:Lcom/ss/android/vesdk/VEAudioCaptureSettings;
23: 
24: .field public mAudioRecord:Landroid/media/AudioRecord;
25: 
26: .field public mAudioRecordStartTime:J
27: 
28: .field public mAudioRecordStopTime:J
29: 
30: .field public mAudioSource:I
31: 
32: .field public mBitsPerSample:I
33: 
34: .field public mBufferSizeInBytes:I
```

- Line 67, `camera_microphone`, `AudioRecord`

```smali
61:     .line 3
62:     invoke-static {v1}, Lcom/bytedance/frameworks/apm/trace/MethodCollector;->i(I)V
63: 
64:     .line 4
65:     .line 5
66:     .line 6
67:     const-string v0, "TEAudioRecord"
68: 
69:     .line 7
70:     .line 8
71:     sput-object v0, Lcom/ss/android/vesdk/audio/TEAudioRecord;->TAG:Ljava/lang/String;
72: 
73:     .line 9
```

- Line 71, `camera_microphone`, `AudioRecord`

```smali
65:     .line 5
66:     .line 6
67:     const-string v0, "TEAudioRecord"
68: 
69:     .line 7
70:     .line 8
71:     sput-object v0, Lcom/ss/android/vesdk/audio/TEAudioRecord;->TAG:Ljava/lang/String;
72: 
73:     .line 9
74:     .line 10
75:     const/4 v0, 0x5
76: 
77:     .line 11
```

#### JADX Reading Context

No matching JADX source was found. Generate it with `task jadx` or review smali directly.
