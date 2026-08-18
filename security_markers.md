# Security Marker Triage

This artifact is a deterministic static triage layer. It identifies security-relevant markers for review, but it does not claim exploitability.

## Scope

- APK path: `TikTok_39.2.1_APKPure.apk`
- Package: `com.zhiliaoapp.musically`
- Version: `39.2.1`
- Decompiled directory: `tiktok_decompiled`

## Evidence Model

- Marker: static code or manifest signal.
- Triggerability: unknown until a reachable flow and input source are reviewed.
- Vulnerability: not claimed unless manual review or dynamic testing shows control, impact, and preconditions.

## Marker Categories

| Category | Severity | Matches | Files | Review focus |
| --- | --- | --- | --- | --- |
| command_execution | high | 18 | 18 | Determine whether command arguments are fixed or attacker-controlled. |
| dynamic_code_loading | high | 98 | 57 | Identify source of loaded code, integrity checks, and writable directories. |
| native_loading | medium-high | 17104 | 873 | Map Java/JNI boundaries and decide whether native libraries need Ghidra review. |
| reflection | medium | 4174 | 1274 | Check whether reflection targets come from constants, configuration, or external input. |
| webview_bridge | high | 737 | 146 | Review bridge exposure, trusted origins, URL validation, and exported entry points. |
| tls_trust | high | 251 | 54 | Look for trust-all behavior, hostname bypasses, and custom certificate validation. |
| file_uri_content | medium | 249 | 63 | Review content/file URI exposure and caller permission checks. |
| intent_entrypoints | medium | 1936 | 889 | Correlate with exported components and deep links before making bug claims. |

## Exported Components

Exported component count: `53`

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
| activity: net.openid.appauth.RedirectUriReceiverActivity |
| provider: com.bytedance.preinstall.attribution.provider.PreinstallAttributionProvider |
| provider: com.facebook.FacebookContentProvider |
| provider: com.ss.android.account.share.data.write.provider.SecShareDataProvider |
| provider: com.ss.android.ugc.aweme.account.provider.OneTapLoginTokenProvider |
| provider: com.ss.android.ugc.aweme.livewallpaper.WallPaperDataProvider |
| receiver: androidx.work.impl.diagnostics.DiagnosticsReceiver |
| receiver: com.adm.push.ADMMessageHandler$Receiver |
| receiver: com.appsflyer.MultipleInstallBroadcastReceiver |
| receiver: com.appsflyer.SingleInstallBroadcastReceiver |
| receiver: com.google.firebase.iid.FirebaseInstanceIdReceiver |
| receiver: com.ss.android.push.window.oppo.ScreenReceiver |
| receiver: com.ss.android.ugc.aweme.common.net.NetWorkStateReceiver |
| receiver: com.ss.android.ugc.aweme.common.net.NetworkReceiver |
| receiver: com.ss.android.ugc.aweme.cubes.engage.EngageBroadcastReceiver |
| receiver: com.ss.android.ugc.trill.abtest.impl.NotificationBroadcastReceiver |
| service: androidx.work.impl.background.systemjob.SystemJobService |
| service: com.google.android.gms.auth.api.signin.RevocationBoundService |
| service: com.heytap.msp.push.service.CompatibleDataMessageCallbackService |
| service: com.heytap.msp.push.service.DataMessageCallbackService |
| service: com.ss.android.message.NotifyService |
| service: com.ss.android.ugc.aweme.livewallpaper.AmeLiveWallpaper |
| service: com.ss.android.ugc.aweme.tile.HotVideoTileService |
| service: com.ss.android.ugc.aweme.tile.PublishTileService |
| service: com.ss.android.ugc.aweme.tools.extract.video.VideoFramesUploadService |
| service: com.ss.android.ugc.aweme.tools.policysecurity.OriginalSoundUploadService |
| service: com.ss.android.ugc.tiktok.samsungfinder.SamsungSearchTikTokBrowserService |
| service: com.ss.android.ugc.trill.account.TiktokAuthService |

## Selected Marker Files

| File | Class | Score | Matches | Categories |
| --- | --- | --- | --- | --- |
| smali_classes17/X/0ceJ.smali | LX/0ceJ | 32 | 5 | command_execution, reflection |
| smali_classes17/X/0cnM.smali | LX/0cnM | 27 | 4 | command_execution, reflection |
| smali_classes4/X/0ABg.1.smali | LX/0ABg | 22 | 3 | command_execution, reflection |
| smali_classes52/ttwebview/Yv.smali | Lttwebview/Yv | 88 | 8 | dynamic_code_loading |
| smali_classes23/com/google/android/gms/dynamite/DynamiteModule.smali | Lcom/google/android/gms/dynamite/DynamiteModule | 90 | 12 | dynamic_code_loading, reflection |
| smali_classes52/org/chromium/base/BundleUtils.smali | Lorg/chromium/base/BundleUtils | 65 | 7 | dynamic_code_loading, reflection |
| smali_classes16/X/0bVx.1.smali | LX/0bVx | 780 | 78 | webview_bridge |
| smali_classes16/X/0bVy.1.smali | LX/0bVy | 710 | 71 | webview_bridge |
| smali_classes16/X/0axr.3.smali | LX/0axr | 330 | 33 | webview_bridge |
| smali_classes40/X/116W.smali | LX/116W | 150 | 15 | tls_trust |
| smali_classes17/X/0diK.2.smali | LX/0diK | 160 | 20 | reflection, tls_trust |
| smali_classes17/X/0dla.3.smali | LX/0dla | 90 | 9 | tls_trust |
| smali_classes9/com/bytedance/ies/nle/editor_jni/NLEEditorJniJNI.smali | Lcom/bytedance/ies/nle/editor_jni/NLEEditorJniJNI | 23640 | 2955 | native_loading |
| smali_classes54/com/bytedance/ies/effectcreatorpro/swig/EffectCreatorProJniJNI.smali | Lcom/bytedance/ies/effectcreatorpro/swig/EffectCreatorProJniJNI | 15768 | 1971 | native_loading |
| smali_classes54/com/bytedance/ies/effectcreator/swig/EffectCreatorJniJNI.smali | Lcom/bytedance/ies/effectcreator/swig/EffectCreatorJniJNI | 14984 | 1873 | native_loading |
| smali_classes17/androidx/core/content/FileProvider.smali | Landroidx/core/content/FileProvider | 511 | 73 | file_uri_content |
| smali_classes17/com/ss/android/common/util/MultiProcessSharedProvider.smali | Lcom/ss/android/common/util/MultiProcessSharedProvider | 103 | 15 | file_uri_content, reflection |
| smali_classes17/com/ss/android/ugc/aweme/account/provider/OneTapLoginTokenProvider.smali | Lcom/ss/android/ugc/aweme/account/provider/OneTapLoginTokenProvider | 63 | 9 | file_uri_content |
| smali_classes23/Y/ARunnableS53S0000000_22.smali | LY/ARunnableS53S0000000_22 | 2695 | 539 | reflection |
| smali_classes8/X/0IUh.1.smali | LX/0IUh | 580 | 116 | reflection |
| smali_classes4/com/appsflyer/internal/AFa1uSDK.smali | Lcom/appsflyer/internal/AFa1uSDK | 540 | 108 | reflection |
| smali_classes8/com/ss/android/ugc/aweme/feed/landscape/LandscapeFeedFragment.smali | Lcom/ss/android/ugc/aweme/feed/landscape/LandscapeFeedFragment | 66 | 22 | intent_entrypoints |
| smali_classes8/Y/AObserverS111S0200000_7.smali | LY/AObserverS111S0200000_7 | 48 | 16 | intent_entrypoints |
| smali_classes24/com/ss/android/ugc/profile/business/profile/ui/v2/I18nMyProfileFragment.smali | Lcom/ss/android/ugc/profile/business/profile/ui/v2/I18nMyProfileFragment | 48 | 16 | intent_entrypoints |
| smali_classes9/com/bytedance/ies/nle/editor_jni/NLEMediaJniJNI.smali | Lcom/bytedance/ies/nle/editor_jni/NLEMediaJniJNI | 6368 | 796 | native_loading |
| smali_classes52/TT_J/TT_N.smali | LTT_J/TT_N | 5024 | 628 | native_loading |
| smali_classes25/com/ss/ugc/android/davinciresource/jni/DavinciResourceJniJNI.smali | Lcom/ss/ugc/android/davinciresource/jni/DavinciResourceJniJNI | 4592 | 574 | native_loading |
| smali_classes25/com/bytedance/ies/effecteditor/swig/EffectEditorJniJNI.smali | Lcom/bytedance/ies/effecteditor/swig/EffectEditorJniJNI | 3320 | 415 | native_loading |
| smali_classes9/com/bytedance/ies/nle/editor_jni/NLEMediaPublicJniJNI.smali | Lcom/bytedance/ies/nle/editor_jni/NLEMediaPublicJniJNI | 3112 | 389 | native_loading |
| smali_classes15/com/bytedance/ies/smartmovie/jni/SmartMovieJniJNI.smali | Lcom/bytedance/ies/smartmovie/jni/SmartMovieJniJNI | 3032 | 379 | native_loading |

## Review Packets

### `smali_classes17/X/0ceJ.smali`

- Class: `LX/0ceJ`
- Categories: `command_execution`, `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 62, `reflection`, `Class.forName`, `.method public static LIZ()Ljava/lang/String;`: `invoke-static {v1}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 110, `reflection`, `Class.forName`, `.method public static LIZ()Ljava/lang/String;`: `invoke-static {v1}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 1082, `reflection`, `Class.forName`, `.method public static LIZIZ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 1131, `reflection`, `Method.invoke`, `.method public static LIZIZ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v1, v4, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;`
- Line 1220, `command_execution`, `Runtime.exec`, `.method public static LIZIZ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v2, v0}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;`

### `smali_classes17/X/0cnM.smali`

- Class: `LX/0cnM`
- Categories: `command_execution`, `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 293, `reflection`, `Class.forName`, `.method public static LIZ()LX/0cnU;`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 1195, `reflection`, `Class.forName`, `.method public static LIZJ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 1256, `reflection`, `Method.invoke`, `.method public static LIZJ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v2, v5, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;`
- Line 1352, `command_execution`, `Runtime.exec`, `.method public static LIZJ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v3, v0}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;`

### `smali_classes4/X/0ABg.1.smali`

- Class: `LX/0ABg`
- Categories: `command_execution`, `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `reflection`, `Class.forName`, `.method public static LIZ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 97, `reflection`, `Method.invoke`, `.method public static LIZ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v1, v4, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;`
- Line 186, `command_execution`, `Runtime.exec`, `.method public static LIZ(Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v2, v0}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;`

### `smali_classes52/ttwebview/Yv.smali`

- Class: `Lttwebview/Yv`
- Categories: `dynamic_code_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 37, `dynamic_code_loading`, `ClassLoader.loadClass`, `.method public final findClass(Ljava/lang/String;)Ljava/lang/Class;`: `invoke-virtual {v0, p1}, Ljava/lang/ClassLoader;->loadClass(Ljava/lang/String;)Ljava/lang/Class;`
- Line 55, `dynamic_code_loading`, `ClassLoader.loadClass`, `.method public final findClass(Ljava/lang/String;)Ljava/lang/Class;`: `invoke-virtual {v0, p1}, Ljava/lang/ClassLoader;->loadClass(Ljava/lang/String;)Ljava/lang/Class;`
- Line 84, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public final findLibrary(Ljava/lang/String;)Ljava/lang/String;`: `instance-of v0, v1, Ldalvik/system/BaseDexClassLoader;`
- Line 88, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public final findLibrary(Ljava/lang/String;)Ljava/lang/String;`: `check-cast v1, Ldalvik/system/BaseDexClassLoader;`
- Line 90, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public final findLibrary(Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v1, p1}, Ldalvik/system/BaseDexClassLoader;->findLibrary(Ljava/lang/String;)Ljava/lang/String;`
- Line 106, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public final findLibrary(Ljava/lang/String;)Ljava/lang/String;`: `instance-of v0, v1, Ldalvik/system/BaseDexClassLoader;`
- Line 110, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public final findLibrary(Ljava/lang/String;)Ljava/lang/String;`: `check-cast v1, Ldalvik/system/BaseDexClassLoader;`
- Line 112, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public final findLibrary(Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v1, p1}, Ldalvik/system/BaseDexClassLoader;->findLibrary(Ljava/lang/String;)Ljava/lang/String;`

### `smali_classes23/com/google/android/gms/dynamite/DynamiteModule.smali`

- Class: `Lcom/google/android/gms/dynamite/DynamiteModule`
- Categories: `dynamic_code_loading`, `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 254, `dynamic_code_loading`, `ClassLoader.loadClass`, `.method public static LIZ(Landroid/content/Context;Ljava/lang/String;)I`: `invoke-virtual {v2, v0}, Ljava/lang/ClassLoader;->loadClass(Ljava/lang/String;)Ljava/lang/Class;`
- Line 289, `reflection`, `Field.get`, `.method public static LIZ(Landroid/content/Context;Ljava/lang/String;)I`: `invoke-virtual {v3, v1}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;`
- Line 309, `reflection`, `Field.get`, `.method public static LIZ(Landroid/content/Context;Ljava/lang/String;)I`: `invoke-virtual {v3, v1}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;`
- Line 2141, `dynamic_code_loading`, `ClassLoader.loadClass`, `.method public static LIZLLL(Landroid/content/Context;Ljava/lang/String;Z)I`: `invoke-virtual {v2, v0}, Ljava/lang/ClassLoader;->loadClass(Ljava/lang/String;)Ljava/lang/Class;`
- Line 2178, `reflection`, `Field.get`, `.method public static LIZLLL(Landroid/content/Context;Ljava/lang/String;Z)I`: `invoke-virtual {v6, v1}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;`
- Line 2304, `reflection`, `Field.set`, `.method public static LIZLLL(Landroid/content/Context;Ljava/lang/String;Z)I`: `invoke-virtual {v6, v1, v0}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V`
- Line 2373, `reflection`, `Field.set`, `.method public static LIZLLL(Landroid/content/Context;Ljava/lang/String;Z)I`: `invoke-virtual {v6, v1, v5}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V`
- Line 2478, `reflection`, `Field.set`, `.method public static LIZLLL(Landroid/content/Context;Ljava/lang/String;Z)I`: `invoke-virtual {v6, v1, v0}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V`

### `smali_classes52/org/chromium/base/BundleUtils.smali`

- Class: `Lorg/chromium/base/BundleUtils`
- Categories: `dynamic_code_loading`, `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 190, `reflection`, `Field.set`, `.method public static a(Landroid/content/Context;Ljava/lang/String;)Landroid/content/Context;`: `invoke-virtual {v0, v2, v3}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V`
- Line 375, `reflection`, `Field.get`, `.method public static b(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v0, v2}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;`
- Line 445, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public static getNativeLibraryPath(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;`: `check-cast v0, Ldalvik/system/BaseDexClassLoader;`
- Line 447, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public static getNativeLibraryPath(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v0, p0}, Ldalvik/system/BaseDexClassLoader;->findLibrary(Ljava/lang/String;)Ljava/lang/String;`
- Line 461, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public static getNativeLibraryPath(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;`: `instance-of v0, v1, Ldalvik/system/BaseDexClassLoader;`
- Line 465, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public static getNativeLibraryPath(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;`: `check-cast v1, Ldalvik/system/BaseDexClassLoader;`
- Line 467, `dynamic_code_loading`, `BaseDexClassLoader`, `.method public static getNativeLibraryPath(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;`: `invoke-virtual {v1, p0}, Ldalvik/system/BaseDexClassLoader;->findLibrary(Ljava/lang/String;)Ljava/lang/String;`

### `smali_classes16/X/0bVx.1.smali`

- Class: `LX/0bVx`
- Categories: `webview_bridge`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 2, `webview_bridge`, `WebViewClient`, `unknown method`: `.super Landroid/webkit/WebViewClient;`
- Line 15, `webview_bridge`, `WebViewClient`, `unknown method`: `.field public LJLIL:Landroid/webkit/WebViewClient;`
- Line 24, `webview_bridge`, `WebViewClient`, `.method public constructor <init>()V`: `invoke-direct {p0}, Landroid/webkit/WebViewClient;-><init>()V`
- Line 123, `webview_bridge`, `WebViewClient`, `.method public doUpdateVisitedHistory(Landroid/webkit/WebView;Ljava/lang/String;Z)V`: `iget-object v0, p0, LX/0bVx;->LJLIL:Landroid/webkit/WebViewClient;`
- Line 131, `webview_bridge`, `WebViewClient`, `.method public doUpdateVisitedHistory(Landroid/webkit/WebView;Ljava/lang/String;Z)V`: `invoke-virtual {v0, p1, p2, p3}, Landroid/webkit/WebViewClient;->doUpdateVisitedHistory(Landroid/webkit/WebView;Ljava/lang/String;Z)V`
- Line 145, `webview_bridge`, `WebViewClient`, `.method public doUpdateVisitedHistory(Landroid/webkit/WebView;Ljava/lang/String;Z)V`: `invoke-super {p0, p1, p2, p3}, Landroid/webkit/WebViewClient;->doUpdateVisitedHistory(Landroid/webkit/WebView;Ljava/lang/String;Z)V`
- Line 200, `webview_bridge`, `WebViewClient`, `.method public onFormResubmission(Landroid/webkit/WebView;Landroid/os/Message;Landroid/os/Message;)V`: `iget-object v0, p0, LX/0bVx;->LJLIL:Landroid/webkit/WebViewClient;`
- Line 208, `webview_bridge`, `WebViewClient`, `.method public onFormResubmission(Landroid/webkit/WebView;Landroid/os/Message;Landroid/os/Message;)V`: `invoke-virtual {v0, p1, p2, p3}, Landroid/webkit/WebViewClient;->onFormResubmission(Landroid/webkit/WebView;Landroid/os/Message;Landroid/os/Message;)V`

### `smali_classes16/X/0bVy.1.smali`

- Class: `LX/0bVy`
- Categories: `webview_bridge`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 2, `webview_bridge`, `WebViewClient`, `unknown method`: `.super Landroid/webkit/WebViewClient;`
- Line 27, `webview_bridge`, `WebViewClient`, `unknown method`: `"Landroid/webkit/WebViewClient;",`
- Line 37, `webview_bridge`, `WebViewClient`, `unknown method`: `.field public static final LJLJJL:Landroid/webkit/WebViewClient;`
- Line 45, `webview_bridge`, `WebViewClient`, `unknown method`: `.field public LJLIL:Landroid/webkit/WebViewClient;`
- Line 105, `webview_bridge`, `WebViewClient`, `.method public static constructor <clinit>()V`: `new-instance v0, Landroid/webkit/WebViewClient;`
- Line 109, `webview_bridge`, `WebViewClient`, `.method public static constructor <clinit>()V`: `invoke-direct {v0}, Landroid/webkit/WebViewClient;-><init>()V`
- Line 114, `webview_bridge`, `WebViewClient`, `.method public static constructor <clinit>()V`: `sput-object v0, LX/0bVy;->LJLJJL:Landroid/webkit/WebViewClient;`
- Line 131, `webview_bridge`, `WebViewClient`, `.method public constructor <init>()V`: `invoke-direct {p0}, Landroid/webkit/WebViewClient;-><init>()V`

### `smali_classes16/X/0axr.3.smali`

- Class: `LX/0axr`
- Categories: `webview_bridge`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 2, `webview_bridge`, `WebViewClient`, `unknown method`: `.super Landroid/webkit/WebViewClient;`
- Line 24, `webview_bridge`, `WebViewClient`, `.method public constructor <init>()V`: `invoke-direct {p0}, Landroid/webkit/WebViewClient;-><init>()V`
- Line 118, `webview_bridge`, `WebViewClient`, `.method public final onLoadResource(Landroid/webkit/WebView;Ljava/lang/String;)V`: `invoke-super {p0, p1, p2}, Landroid/webkit/WebViewClient;->onLoadResource(Landroid/webkit/WebView;Ljava/lang/String;)V`
- Line 156, `webview_bridge`, `WebViewClient`, `.method public final onLoadResource(Landroid/webkit/WebView;Ljava/lang/String;)V`: `check-cast v0, Landroid/webkit/WebViewClient;`
- Line 161, `webview_bridge`, `WebViewClient`, `.method public final onLoadResource(Landroid/webkit/WebView;Ljava/lang/String;)V`: `invoke-virtual {v0, p1, p2}, Landroid/webkit/WebViewClient;->onLoadResource(Landroid/webkit/WebView;Ljava/lang/String;)V`
- Line 207, `webview_bridge`, `WebViewClient`, `.method public final onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V`: `invoke-super {p0, p1, p2}, Landroid/webkit/WebViewClient;->onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V`
- Line 245, `webview_bridge`, `WebViewClient`, `.method public final onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V`: `check-cast v0, Landroid/webkit/WebViewClient;`
- Line 250, `webview_bridge`, `WebViewClient`, `.method public final onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V`: `invoke-virtual {v0, p1, p2}, Landroid/webkit/WebViewClient;->onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V`

### `smali_classes40/X/116W.smali`

- Class: `LX/116W`
- Categories: `tls_trust`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 30, `tls_trust`, `HostnameVerifier`, `unknown method`: `.field public final LJII:Ljavax/net/ssl/HostnameVerifier;`
- Line 40, `tls_trust`, `TrustManager`, `unknown method`: `.field public final LJIIL:[Ljavax/net/ssl/TrustManager;`
- Line 124, `tls_trust`, `TrustManager`, `.method public static constructor <clinit>()V`: `new-array v2, v0, [Ljavax/net/ssl/TrustManager;`
- Line 147, `tls_trust`, `TrustManager`, `.method public static constructor <clinit>()V`: `invoke-virtual {v3, v0, v2, v0}, Ljavax/net/ssl/SSLContext;->init([Ljavax/net/ssl/KeyManager;[Ljavax/net/ssl/TrustManager;Ljava/security/SecureRandom;)V`
- Line 179, `tls_trust`, `HostnameVerifier`, `.method public constructor <init>(LX/111U;Ljava/lang/String;Ljavax/net/ssl/SSLEngine;[Ljavax/net/ssl/TrustManager;Ljavax/net/ssl/HostnameVerifier;)V`: `.method public constructor <init>(LX/111U;Ljava/lang/String;Ljavax/net/ssl/SSLEngine;[Ljavax/net/ssl/TrustManager;Ljavax/net/ssl/HostnameVerifier;)V`
- Line 179, `tls_trust`, `TrustManager`, `.method public constructor <init>(LX/111U;Ljava/lang/String;Ljavax/net/ssl/SSLEngine;[Ljavax/net/ssl/TrustManager;Ljavax/net/ssl/HostnameVerifier;)V`: `.method public constructor <init>(LX/111U;Ljava/lang/String;Ljavax/net/ssl/SSLEngine;[Ljavax/net/ssl/TrustManager;Ljavax/net/ssl/HostnameVerifier;)V`
- Line 242, `tls_trust`, `HostnameVerifier`, `.method public constructor <init>(LX/111U;Ljava/lang/String;Ljavax/net/ssl/SSLEngine;[Ljavax/net/ssl/TrustManager;Ljavax/net/ssl/HostnameVerifier;)V`: `iput-object p5, p0, LX/116W;->LJII:Ljavax/net/ssl/HostnameVerifier;`
- Line 253, `tls_trust`, `TrustManager`, `.method public constructor <init>(LX/111U;Ljava/lang/String;Ljavax/net/ssl/SSLEngine;[Ljavax/net/ssl/TrustManager;Ljavax/net/ssl/HostnameVerifier;)V`: `iput-object p4, p0, LX/116W;->LJIIL:[Ljavax/net/ssl/TrustManager;`

### `smali_classes17/X/0diK.2.smali`

- Class: `LX/0diK`
- Categories: `reflection`, `tls_trust`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 114, `reflection`, `Class.forName`, `.method public constructor <init>(Ljava/lang/Class;LX/09wR;LX/09wR;LX/09wR;LX/09wR;)V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 309, `reflection`, `Method.invoke`, `.method public static LJIILLIIL(Ljava/lang/Class;Ljava/lang/String;Ljava/lang/Object;)Z`: `invoke-virtual {v1, p2, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;`
- Line 375, `reflection`, `Method.invoke`, `.method public static LJIILLIIL(Ljava/lang/Class;Ljava/lang/String;Ljava/lang/Object;)Z`: `invoke-virtual {v1, p2, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;`
- Line 434, `tls_trust`, `X509TrustManager`, `.method public final LIZJ(Ljavax/net/ssl/X509TrustManager;)LX/0d0e;`: `.method public final LIZJ(Ljavax/net/ssl/X509TrustManager;)LX/0d0e;`
- Line 454, `reflection`, `Class.forName`, `.method public final LIZJ(Ljavax/net/ssl/X509TrustManager;)LX/0d0e;`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 469, `tls_trust`, `X509TrustManager`, `.method public final LIZJ(Ljavax/net/ssl/X509TrustManager;)LX/0d0e;`: `const-class v0, Ljavax/net/ssl/X509TrustManager;`
- Line 496, `reflection`, `Constructor.newInstance`, `.method public final LIZJ(Ljavax/net/ssl/X509TrustManager;)LX/0d0e;`: `invoke-virtual {v1, v0}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;`
- Line 578, `tls_trust`, `X509TrustManager`, `.method public final LIZJ(Ljavax/net/ssl/X509TrustManager;)LX/0d0e;`: `invoke-super {p0, p1}, LX/0diM;->LIZJ(Ljavax/net/ssl/X509TrustManager;)LX/0d0e;`

### `smali_classes17/X/0dla.3.smali`

- Class: `LX/0dla`
- Categories: `tls_trust`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 89, `tls_trust`, `HostnameVerifier`, `unknown method`: `.field public final LJLLI:Ljavax/net/ssl/HostnameVerifier;`
- Line 550, `tls_trust`, `TrustManager`, `.method public constructor <init>(LX/0dlb;)V`: `invoke-virtual {v0}, Ljavax/net/ssl/TrustManagerFactory;->getTrustManagers()[Ljavax/net/ssl/TrustManager;`
- Line 569, `tls_trust`, `X509TrustManager`, `.method public constructor <init>(LX/0dlb;)V`: `instance-of v0, v4, Ljavax/net/ssl/X509TrustManager;`
- Line 577, `tls_trust`, `X509TrustManager`, `.method public constructor <init>(LX/0dlb;)V`: `check-cast v4, Ljavax/net/ssl/X509TrustManager;`
- Line 611, `tls_trust`, `TrustManager`, `.method public constructor <init>(LX/0dlb;)V`: `new-array v0, v8, [Ljavax/net/ssl/TrustManager;`
- Line 619, `tls_trust`, `TrustManager`, `.method public constructor <init>(LX/0dlb;)V`: `invoke-virtual {v1, v6, v0, v6}, Ljavax/net/ssl/SSLContext;->init([Ljavax/net/ssl/KeyManager;[Ljavax/net/ssl/TrustManager;Ljava/security/SecureRandom;)V`
- Line 772, `tls_trust`, `X509TrustManager`, `.method public constructor <init>(LX/0dlb;)V`: `invoke-virtual {v2, v4}, LX/0diM;->LIZJ(Ljavax/net/ssl/X509TrustManager;)LX/0d0e;`
- Line 803, `tls_trust`, `HostnameVerifier`, `.method public constructor <init>(LX/0dlb;)V`: `iget-object v0, p1, LX/0dlb;->hostnameVerifier:Ljavax/net/ssl/HostnameVerifier;`

### `smali_classes9/com/bytedance/ies/nle/editor_jni/NLEEditorJniJNI.smali`

- Class: `Lcom/bytedance/ies/nle/editor_jni/NLEEditorJniJNI`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `native_loading`, `native method`, `.method public static final native INLEMonitor_change_ownership(Lcom/bytedance/ies/nle/editor_jni/INLEMonitor;JZ)V`: `.method public static final native INLEMonitor_change_ownership(Lcom/bytedance/ies/nle/editor_jni/INLEMonitor;JZ)V`
- Line 51, `native_loading`, `native method`, `.method public static final native INLEMonitor_director_connect(Lcom/bytedance/ies/nle/editor_jni/INLEMonitor;JZZ)V`: `.method public static final native INLEMonitor_director_connect(Lcom/bytedance/ies/nle/editor_jni/INLEMonitor;JZZ)V`
- Line 54, `native_loading`, `native method`, `.method public static final native INLEMonitor_onEvent(JLcom/bytedance/ies/nle/editor_jni/INLEMonitor;Ljava/lang/String;ILjava/lang/String;J)V`: `.method public static final native INLEMonitor_onEvent(JLcom/bytedance/ies/nle/editor_jni/INLEMonitor;Ljava/lang/String;ILjava/lang/String;J)V`
- Line 57, `native_loading`, `native method`, `.method public static final native INLEMonitor_onEventSwigExplicitINLEMonitor(JLcom/bytedance/ies/nle/editor_jni/INLEMonitor;Ljava/lang/String;ILjava/lang/String;J)V`: `.method public static final native INLEMonitor_onEventSwigExplicitINLEMonitor(JLcom/bytedance/ies/nle/editor_jni/INLEMonitor;Ljava/lang/String;ILjava/lang/String;J)V`
- Line 60, `native_loading`, `native method`, `.method public static final native MapStrNLENodeSPtrConst_Iterator_getKey(JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;)Ljava/lang/String;`: `.method public static final native MapStrNLENodeSPtrConst_Iterator_getKey(JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;)Ljava/lang/String;`
- Line 63, `native_loading`, `native method`, `.method public static final native MapStrNLENodeSPtrConst_Iterator_getNextUnchecked(JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;)J`: `.method public static final native MapStrNLENodeSPtrConst_Iterator_getNextUnchecked(JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;)J`
- Line 66, `native_loading`, `native method`, `.method public static final native MapStrNLENodeSPtrConst_Iterator_getValue(JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;)J`: `.method public static final native MapStrNLENodeSPtrConst_Iterator_getValue(JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;)J`
- Line 69, `native_loading`, `native method`, `.method public static final native MapStrNLENodeSPtrConst_Iterator_isNot(JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;)Z`: `.method public static final native MapStrNLENodeSPtrConst_Iterator_isNot(JLcom/bytedance/ies/nle/editor_jni/MapStrNLENodeSPtrConst$Iterator;JLcom/bytedance/ies/nle/editor_jni/Ma...`

### `smali_classes54/com/bytedance/ies/effectcreatorpro/swig/EffectCreatorProJniJNI.smali`

- Class: `Lcom/bytedance/ies/effectcreatorpro/swig/EffectCreatorProJniJNI`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioClipEndTime_get(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;)D`: `.method public static final native ActionExtraData_audioClipEndTime_get(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;)D`
- Line 51, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioClipEndTime_set(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;D)V`: `.method public static final native ActionExtraData_audioClipEndTime_set(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;D)V`
- Line 54, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioClipStartTime_get(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;)D`: `.method public static final native ActionExtraData_audioClipStartTime_get(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;)D`
- Line 57, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioClipStartTime_set(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;D)V`: `.method public static final native ActionExtraData_audioClipStartTime_set(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;D)V`
- Line 60, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioVolume_get(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;)D`: `.method public static final native ActionExtraData_audioVolume_get(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;)D`
- Line 63, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioVolume_set(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;D)V`: `.method public static final native ActionExtraData_audioVolume_set(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;D)V`
- Line 66, `native_loading`, `native method`, `.method public static final native ActionExtraData_timeInterval_get(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;)D`: `.method public static final native ActionExtraData_timeInterval_get(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;)D`
- Line 69, `native_loading`, `native method`, `.method public static final native ActionExtraData_timeInterval_set(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;D)V`: `.method public static final native ActionExtraData_timeInterval_set(JLcom/bytedance/ies/effectcreatorpro/swig/ActionExtraData;D)V`

### `smali_classes54/com/bytedance/ies/effectcreator/swig/EffectCreatorJniJNI.smali`

- Class: `Lcom/bytedance/ies/effectcreator/swig/EffectCreatorJniJNI`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioClipEndTime_get(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;)D`: `.method public static final native ActionExtraData_audioClipEndTime_get(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;)D`
- Line 51, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioClipEndTime_set(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;D)V`: `.method public static final native ActionExtraData_audioClipEndTime_set(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;D)V`
- Line 54, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioClipStartTime_get(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;)D`: `.method public static final native ActionExtraData_audioClipStartTime_get(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;)D`
- Line 57, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioClipStartTime_set(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;D)V`: `.method public static final native ActionExtraData_audioClipStartTime_set(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;D)V`
- Line 60, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioVolume_get(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;)D`: `.method public static final native ActionExtraData_audioVolume_get(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;)D`
- Line 63, `native_loading`, `native method`, `.method public static final native ActionExtraData_audioVolume_set(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;D)V`: `.method public static final native ActionExtraData_audioVolume_set(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;D)V`
- Line 66, `native_loading`, `native method`, `.method public static final native ActionExtraData_timeInterval_get(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;)D`: `.method public static final native ActionExtraData_timeInterval_get(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;)D`
- Line 69, `native_loading`, `native method`, `.method public static final native ActionExtraData_timeInterval_set(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;D)V`: `.method public static final native ActionExtraData_timeInterval_set(JLcom/bytedance/ies/effectcreator/swig/ActionExtraData;D)V`

### `smali_classes17/androidx/core/content/FileProvider.smali`

- Class: `Landroidx/core/content/FileProvider`
- Categories: `file_uri_content`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 1, `file_uri_content`, `FileProvider`, `unknown method`: `.class public Landroidx/core/content/FileProvider;`
- Line 2, `file_uri_content`, `ContentProvider`, `unknown method`: `.super Landroid/content/ContentProvider;`
- Line 53, `file_uri_content`, `FileProvider`, `.method public static constructor <clinit>()V`: `sput-object v0, Landroidx/core/content/FileProvider;->COLUMNS:[Ljava/lang/String;`
- Line 70, `file_uri_content`, `FileProvider`, `.method public static constructor <clinit>()V`: `sput-object v1, Landroidx/core/content/FileProvider;->DEVICE_ROOT:Ljava/io/File;`
- Line 83, `file_uri_content`, `FileProvider`, `.method public static constructor <clinit>()V`: `sput-object v0, Landroidx/core/content/FileProvider;->sCache:Ljava/util/HashMap;`
- Line 95, `file_uri_content`, `ContentProvider`, `.method public constructor <init>()V`: `invoke-direct {p0}, Landroid/content/ContentProvider;-><init>()V`
- Line 108, `file_uri_content`, `ContentProvider`, `.method public constructor <init>(I)V`: `invoke-direct {p0}, Landroid/content/ContentProvider;-><init>()V`
- Line 113, `file_uri_content`, `FileProvider`, `.method public constructor <init>(I)V`: `iput p1, p0, Landroidx/core/content/FileProvider;->mResourceId:I`

### `smali_classes17/com/ss/android/common/util/MultiProcessSharedProvider.smali`

- Class: `Lcom/ss/android/common/util/MultiProcessSharedProvider`
- Categories: `file_uri_content`, `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 2, `file_uri_content`, `ContentProvider`, `unknown method`: `.super Landroid/content/ContentProvider;`
- Line 37, `file_uri_content`, `ContentProvider`, `.method public constructor <init>()V`: `invoke-direct {p0}, Landroid/content/ContentProvider;-><init>()V`
- Line 597, `file_uri_content`, `ContentProvider`, `.method public final declared-synchronized LIZIZ()Landroid/content/SharedPreferences;`: `invoke-virtual {p0}, Landroid/content/ContentProvider;->getContext()Landroid/content/Context;`
- Line 842, `file_uri_content`, `ContentProvider`, `.method public final LJFF(Landroid/net/Uri;)V`: `invoke-virtual {p0}, Landroid/content/ContentProvider;->getContext()Landroid/content/Context;`
- Line 897, `file_uri_content`, `ContentProvider`, `.method public final attachInfo(Landroid/content/Context;Landroid/content/pm/ProviderInfo;)V`: `invoke-super {p0, p1, p2}, Landroid/content/ContentProvider;->attachInfo(Landroid/content/Context;Landroid/content/pm/ProviderInfo;)V`
- Line 1022, `file_uri_content`, `ContentProvider`, `.method public final delete(Landroid/net/Uri;Ljava/lang/String;[Ljava/lang/String;)I`: `invoke-virtual {p0}, Landroid/content/ContentProvider;->getContext()Landroid/content/Context;`
- Line 1470, `file_uri_content`, `ContentProvider`, `.method public final insert(Landroid/net/Uri;Landroid/content/ContentValues;)Landroid/net/Uri;`: `invoke-virtual {p0}, Landroid/content/ContentProvider;->getContext()Landroid/content/Context;`
- Line 1525, `file_uri_content`, `ContentProvider`, `.method public final insert(Landroid/net/Uri;Landroid/content/ContentValues;)Landroid/net/Uri;`: `invoke-virtual {p0}, Landroid/content/ContentProvider;->getContext()Landroid/content/Context;`

### `smali_classes17/com/ss/android/ugc/aweme/account/provider/OneTapLoginTokenProvider.smali`

- Class: `Lcom/ss/android/ugc/aweme/account/provider/OneTapLoginTokenProvider`
- Categories: `file_uri_content`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 2, `file_uri_content`, `ContentProvider`, `unknown method`: `.super Landroid/content/ContentProvider;`
- Line 32, `file_uri_content`, `ContentProvider`, `.method public constructor <init>()V`: `invoke-direct {p0}, Landroid/content/ContentProvider;-><init>()V`
- Line 384, `file_uri_content`, `ContentProvider`, `.method public final LIZIZ()V`: `invoke-virtual {p0}, Landroid/content/ContentProvider;->getContext()Landroid/content/Context;`
- Line 783, `file_uri_content`, `ContentProvider`, `.method public final delete(Landroid/net/Uri;Ljava/lang/String;[Ljava/lang/String;)I`: `invoke-virtual {p0}, Landroid/content/ContentProvider;->getCallingPackage()Ljava/lang/String;`
- Line 798, `file_uri_content`, `ContentProvider`, `.method public final delete(Landroid/net/Uri;Ljava/lang/String;[Ljava/lang/String;)I`: `invoke-virtual {p0}, Landroid/content/ContentProvider;->getContext()Landroid/content/Context;`
- Line 1241, `file_uri_content`, `ContentProvider`, `.method public final insert(Landroid/net/Uri;Landroid/content/ContentValues;)Landroid/net/Uri;`: `invoke-virtual {v4}, Landroid/content/ContentProvider;->getCallingPackage()Ljava/lang/String;`
- Line 1253, `file_uri_content`, `ContentProvider`, `.method public final insert(Landroid/net/Uri;Landroid/content/ContentValues;)Landroid/net/Uri;`: `invoke-virtual {v4}, Landroid/content/ContentProvider;->getContext()Landroid/content/Context;`
- Line 2472, `file_uri_content`, `ContentProvider`, `.method public final query(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;)Landroid/database/Cursor;`: `invoke-virtual {v4}, Landroid/content/ContentProvider;->getCallingPackage()Ljava/lang/String;`

### `smali_classes23/Y/ARunnableS53S0000000_22.smali`

- Class: `LY/ARunnableS53S0000000_22`
- Categories: `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 67, `reflection`, `Class.forName`, `.method public static LIZ$0()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 84, `reflection`, `Class.forName`, `.method public static LIZ$0()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 101, `reflection`, `Class.forName`, `.method public static LIZ$0()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 118, `reflection`, `Class.forName`, `.method public static LIZ$0()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 135, `reflection`, `Class.forName`, `.method public static LIZ$0()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 152, `reflection`, `Class.forName`, `.method public static LIZ$0()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 169, `reflection`, `Class.forName`, `.method public static LIZ$0()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 186, `reflection`, `Class.forName`, `.method public static LIZ$0()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`

### `smali_classes8/X/0IUh.1.smali`

- Class: `LX/0IUh`
- Categories: `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 7096, `reflection`, `Class.forName`, `.method public static LIZ()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 7105, `reflection`, `Class.forName`, `.method public static LIZ()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 7114, `reflection`, `Class.forName`, `.method public static LIZ()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 7123, `reflection`, `Class.forName`, `.method public static LIZ()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 7132, `reflection`, `Class.forName`, `.method public static LIZ()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 7141, `reflection`, `Class.forName`, `.method public static LIZ()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 7150, `reflection`, `Class.forName`, `.method public static LIZ()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 7159, `reflection`, `Class.forName`, `.method public static LIZ()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`

### `smali_classes4/com/appsflyer/internal/AFa1uSDK.smali`

- Class: `Lcom/appsflyer/internal/AFa1uSDK`
- Categories: `reflection`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 359, `reflection`, `Class.forName`, `.method public static constructor <clinit>()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 440, `reflection`, `Class.forName`, `.method public static constructor <clinit>()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 778, `reflection`, `Class.forName`, `.method public static constructor <clinit>()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 841, `reflection`, `Class.forName`, `.method public static constructor <clinit>()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 855, `reflection`, `Constructor.newInstance`, `.method public static constructor <clinit>()V`: `invoke-virtual {v0, v5}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;`
- Line 923, `reflection`, `Class.forName`, `.method public static constructor <clinit>()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`
- Line 937, `reflection`, `Constructor.newInstance`, `.method public static constructor <clinit>()V`: `invoke-virtual {v0, v6}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;`
- Line 1009, `reflection`, `Class.forName`, `.method public static constructor <clinit>()V`: `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`

### `smali_classes8/com/ss/android/ugc/aweme/feed/landscape/LandscapeFeedFragment.smali`

- Class: `Lcom/ss/android/ugc/aweme/feed/landscape/LandscapeFeedFragment`
- Categories: `intent_entrypoints`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 696, `intent_entrypoints`, `Activity.getIntent`, `.method public final onAttach(Landroid/app/Activity;)V`: `invoke-virtual {p1}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 738, `intent_entrypoints`, `Activity.getIntent`, `.method public final onAttach(Landroid/app/Activity;)V`: `invoke-virtual {p1}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 808, `intent_entrypoints`, `Activity.getIntent`, `.method public final onAttach(Landroid/app/Activity;)V`: `invoke-virtual {p1}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 833, `intent_entrypoints`, `Activity.getIntent`, `.method public final onAttach(Landroid/app/Activity;)V`: `invoke-virtual {p1}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 858, `intent_entrypoints`, `Activity.getIntent`, `.method public final onAttach(Landroid/app/Activity;)V`: `invoke-virtual {p1}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 900, `intent_entrypoints`, `Activity.getIntent`, `.method public final onAttach(Landroid/app/Activity;)V`: `invoke-virtual {p1}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 933, `intent_entrypoints`, `Activity.getIntent`, `.method public final onAttach(Landroid/app/Activity;)V`: `invoke-virtual {p1}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 966, `intent_entrypoints`, `Activity.getIntent`, `.method public final onAttach(Landroid/app/Activity;)V`: `invoke-virtual {p1}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`

### `smali_classes8/Y/AObserverS111S0200000_7.smali`

- Class: `LY/AObserverS111S0200000_7`
- Categories: `intent_entrypoints`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 1245, `intent_entrypoints`, `Activity.getIntent`, `.method public static final onChanged$11(LY/AObserverS111S0200000_7;Ljava/lang/Object;)V`: `invoke-virtual {v8}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 1311, `intent_entrypoints`, `Activity.getIntent`, `.method public static final onChanged$11(LY/AObserverS111S0200000_7;Ljava/lang/Object;)V`: `invoke-virtual {v8}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 1449, `intent_entrypoints`, `Activity.getIntent`, `.method public static final onChanged$11(LY/AObserverS111S0200000_7;Ljava/lang/Object;)V`: `invoke-virtual {v8}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 1710, `intent_entrypoints`, `Activity.getIntent`, `.method public static final onChanged$11(LY/AObserverS111S0200000_7;Ljava/lang/Object;)V`: `invoke-virtual {v8}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 1759, `intent_entrypoints`, `Activity.getIntent`, `.method public static final onChanged$11(LY/AObserverS111S0200000_7;Ljava/lang/Object;)V`: `invoke-virtual {v8}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 1775, `intent_entrypoints`, `Activity.getIntent`, `.method public static final onChanged$11(LY/AObserverS111S0200000_7;Ljava/lang/Object;)V`: `invoke-virtual {v8}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 1795, `intent_entrypoints`, `Activity.getIntent`, `.method public static final onChanged$11(LY/AObserverS111S0200000_7;Ljava/lang/Object;)V`: `invoke-virtual {v8}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 1815, `intent_entrypoints`, `Activity.getIntent`, `.method public static final onChanged$11(LY/AObserverS111S0200000_7;Ljava/lang/Object;)V`: `invoke-virtual {v8}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`

### `smali_classes24/com/ss/android/ugc/profile/business/profile/ui/v2/I18nMyProfileFragment.smali`

- Class: `Lcom/ss/android/ugc/profile/business/profile/ui/v2/I18nMyProfileFragment`
- Categories: `intent_entrypoints`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 5668, `intent_entrypoints`, `Activity.getIntent`, `.method public final initData()V`: `invoke-virtual {v0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 5754, `intent_entrypoints`, `Activity.getIntent`, `.method public final initData()V`: `invoke-virtual {v0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 5988, `intent_entrypoints`, `onActivityResult`, `.method public final onActivityResult(IILandroid/content/Intent;)V`: `.method public final onActivityResult(IILandroid/content/Intent;)V`
- Line 6003, `intent_entrypoints`, `onActivityResult`, `.method public final onActivityResult(IILandroid/content/Intent;)V`: `invoke-super {p0, p1, p2, p3}, Landroidx/fragment/app/Fragment;->onActivityResult(IILandroid/content/Intent;)V`
- Line 9440, `intent_entrypoints`, `Activity.getIntent`, `.method public final onResume()V`: `invoke-virtual {v0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 9639, `intent_entrypoints`, `Activity.getIntent`, `.method public final onResume()V`: `invoke-virtual {v0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 9730, `intent_entrypoints`, `Activity.getIntent`, `.method public final onResume()V`: `invoke-virtual {v0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`
- Line 9764, `intent_entrypoints`, `Activity.getIntent`, `.method public final onResume()V`: `invoke-virtual {v0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;`

### `smali_classes9/com/bytedance/ies/nle/editor_jni/NLEMediaJniJNI.smali`

- Class: `Lcom/bytedance/ies/nle/editor_jni/NLEMediaJniJNI`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `native_loading`, `native method`, `.method public static final native INLEAsyncRenderPlayStatusListener_change_ownership(Lcom/bytedance/ies/nle/editor_jni/INLEAsyncRenderPlayStatusListener;JZ)V`: `.method public static final native INLEAsyncRenderPlayStatusListener_change_ownership(Lcom/bytedance/ies/nle/editor_jni/INLEAsyncRenderPlayStatusListener;JZ)V`
- Line 51, `native_loading`, `native method`, `.method public static final native INLEAsyncRenderPlayStatusListener_director_connect(Lcom/bytedance/ies/nle/editor_jni/INLEAsyncRenderPlayStatusListener;JZZ)V`: `.method public static final native INLEAsyncRenderPlayStatusListener_director_connect(Lcom/bytedance/ies/nle/editor_jni/INLEAsyncRenderPlayStatusListener;JZZ)V`
- Line 54, `native_loading`, `native method`, `.method public static final native INLEAsyncRenderPlayStatusListener_onPauseInner(JLcom/bytedance/ies/nle/editor_jni/INLEAsyncRenderPlayStatusListener;)V`: `.method public static final native INLEAsyncRenderPlayStatusListener_onPauseInner(JLcom/bytedance/ies/nle/editor_jni/INLEAsyncRenderPlayStatusListener;)V`
- Line 57, `native_loading`, `native method`, `.method public static final native INLEAsyncRenderPlayStatusListener_onPlayInner(JLcom/bytedance/ies/nle/editor_jni/INLEAsyncRenderPlayStatusListener;)V`: `.method public static final native INLEAsyncRenderPlayStatusListener_onPlayInner(JLcom/bytedance/ies/nle/editor_jni/INLEAsyncRenderPlayStatusListener;)V`
- Line 60, `native_loading`, `native method`, `.method public static final native INLEMattingListener_change_ownership(Lcom/bytedance/ies/nle/editor_jni/INLEMattingListener;JZ)V`: `.method public static final native INLEMattingListener_change_ownership(Lcom/bytedance/ies/nle/editor_jni/INLEMattingListener;JZ)V`
- Line 63, `native_loading`, `native method`, `.method public static final native INLEMattingListener_director_connect(Lcom/bytedance/ies/nle/editor_jni/INLEMattingListener;JZZ)V`: `.method public static final native INLEMattingListener_director_connect(Lcom/bytedance/ies/nle/editor_jni/INLEMattingListener;JZZ)V`
- Line 66, `native_loading`, `native method`, `.method public static final native INLEMattingListener_onMattingAddedCallback(JLcom/bytedance/ies/nle/editor_jni/INLEMattingListener;Ljava/lang/String;)V`: `.method public static final native INLEMattingListener_onMattingAddedCallback(JLcom/bytedance/ies/nle/editor_jni/INLEMattingListener;Ljava/lang/String;)V`
- Line 69, `native_loading`, `native method`, `.method public static final native INLEMattingListener_onMattingClipDoneCallback(JLcom/bytedance/ies/nle/editor_jni/INLEMattingListener;Ljava/lang/String;FF)V`: `.method public static final native INLEMattingListener_onMattingClipDoneCallback(JLcom/bytedance/ies/nle/editor_jni/INLEMattingListener;Ljava/lang/String;FF)V`

### `smali_classes52/TT_J/TT_N.smali`

- Class: `LTT_J/TT_N`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 7, `native_loading`, `native method`, `.method public static native M$$25N5$(J)V`: `.method public static native M$$25N5$(J)V`
- Line 10, `native_loading`, `native method`, `.method public static native M$2oj6EQ(JLjava/lang/Object;JIFFIFFFIIII)V`: `.method public static native M$2oj6EQ(JLjava/lang/Object;JIFFIFFFIIII)V`
- Line 13, `native_loading`, `native method`, `.method public static native M$HKWu8q(JLjava/lang/Object;Ljava/lang/String;ZZLjava/lang/Object;)V`: `.method public static native M$HKWu8q(JLjava/lang/Object;Ljava/lang/String;ZZLjava/lang/Object;)V`
- Line 16, `native_loading`, `native method`, `.method public static native M$O7xE3y(Ljava/lang/Object;Ljava/lang/Object;)V`: `.method public static native M$O7xE3y(Ljava/lang/Object;Ljava/lang/Object;)V`
- Line 19, `native_loading`, `native method`, `.method public static native M$b45Vvn(JIIZZII[Ljava/lang/String;)V`: `.method public static native M$b45Vvn(JIIZZII[Ljava/lang/String;)V`
- Line 22, `native_loading`, `native method`, `.method public static native M$eaBDjM(J)Ljava/lang/Object;`: `.method public static native M$eaBDjM(J)Ljava/lang/Object;`
- Line 25, `native_loading`, `native method`, `.method public static native M$oMD214(Ljava/lang/String;JIIII)J`: `.method public static native M$oMD214(Ljava/lang/String;JIIII)J`
- Line 28, `native_loading`, `native method`, `.method public static native M$ugXLRy(J[B)Z`: `.method public static native M$ugXLRy(J[B)Z`

### `smali_classes25/com/ss/ugc/android/davinciresource/jni/DavinciResourceJniJNI.smali`

- Class: `Lcom/ss/ugc/android/davinciresource/jni/DavinciResourceJniJNI`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `native_loading`, `native method`, `.method public static final native AlgorithmResourceFinder_resourceFinder(JLjava/lang/String;Ljava/lang/String;)Ljava/lang/String;`: `.method public static final native AlgorithmResourceFinder_resourceFinder(JLjava/lang/String;Ljava/lang/String;)Ljava/lang/String;`
- Line 51, `native_loading`, `native method`, `.method public static final native AlgorithmResourceGlobalSettings_getAlgorithmModelMappingRuleValid()Z`: `.method public static final native AlgorithmResourceGlobalSettings_getAlgorithmModelMappingRuleValid()Z`
- Line 54, `native_loading`, `native method`, `.method public static final native AlgorithmResourceGlobalSettings_getResourceFinder()J`: `.method public static final native AlgorithmResourceGlobalSettings_getResourceFinder()J`
- Line 57, `native_loading`, `native method`, `.method public static final native AlgorithmResourceGlobalSettings_setAlgorithmModelMappingRuleValid(Z)V`: `.method public static final native AlgorithmResourceGlobalSettings_setAlgorithmModelMappingRuleValid(Z)V`
- Line 60, `native_loading`, `native method`, `.method public static final native AlgorithmResourceGlobalSettings_setBuildInModelFinder(JLcom/ss/ugc/android/davinciresource/jni/IBuildInModelFinder;)V`: `.method public static final native AlgorithmResourceGlobalSettings_setBuildInModelFinder(JLcom/ss/ugc/android/davinciresource/jni/IBuildInModelFinder;)V`
- Line 63, `native_loading`, `native method`, `.method public static final native AlgorithmResourceGlobalSettings_setRequirementsPeeker(JLcom/ss/ugc/android/davinciresource/jni/IRequirementsPeeker;)V`: `.method public static final native AlgorithmResourceGlobalSettings_setRequirementsPeeker(JLcom/ss/ugc/android/davinciresource/jni/IRequirementsPeeker;)V`
- Line 66, `native_loading`, `native method`, `.method public static final native AlgorithmResourceHandler_Builder_accessKey(JLcom/ss/ugc/android/davinciresource/jni/AlgorithmResourceHandler$Builder;Ljava/lang/String;)J`: `.method public static final native AlgorithmResourceHandler_Builder_accessKey(JLcom/ss/ugc/android/davinciresource/jni/AlgorithmResourceHandler$Builder;Ljava/lang/String;)J`
- Line 69, `native_loading`, `native method`, `.method public static final native AlgorithmResourceHandler_Builder_appID(JLcom/ss/ugc/android/davinciresource/jni/AlgorithmResourceHandler$Builder;Ljava/lang/String;)J`: `.method public static final native AlgorithmResourceHandler_Builder_appID(JLcom/ss/ugc/android/davinciresource/jni/AlgorithmResourceHandler$Builder;Ljava/lang/String;)J`

### `smali_classes25/com/bytedance/ies/effecteditor/swig/EffectEditorJniJNI.smali`

- Class: `Lcom/bytedance/ies/effecteditor/swig/EffectEditorJniJNI`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `native_loading`, `native method`, `.method public static final native EEEffectHandle_Instance()J`: `.method public static final native EEEffectHandle_Instance()J`
- Line 51, `native_loading`, `native method`, `.method public static final native EEEffectHandle_addEffectHandlesChangeObserver(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;JLcom/bytedance/ies/effecteditor/swig/EffectHandlesChangedObserver;)V`: `.method public static final native EEEffectHandle_addEffectHandlesChangeObserver(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;JLcom/bytedance/ies/effecteditor/swig/Effec...`
- Line 54, `native_loading`, `native method`, `.method public static final native EEEffectHandle_getAMEEditEffectHandleGetterPtr(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;)J`: `.method public static final native EEEffectHandle_getAMEEditEffectHandleGetterPtr(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;)J`
- Line 57, `native_loading`, `native method`, `.method public static final native EEEffectHandle_notifyEffectHandlesChanged(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;)V`: `.method public static final native EEEffectHandle_notifyEffectHandlesChanged(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;)V`
- Line 60, `native_loading`, `native method`, `.method public static final native EEEffectHandle_removeEffectHandlesChangeObserver(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;JLcom/bytedance/ies/effecteditor/swig/EffectHandlesChangedObserver;)V`: `.method public static final native EEEffectHandle_removeEffectHandlesChangeObserver(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;JLcom/bytedance/ies/effecteditor/swig/Ef...`
- Line 63, `native_loading`, `native method`, `.method public static final native EEEffectHandle_setMETEffectHandleGetterPtr(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;JLcom/bytedance/ies/effecteditor/swig/EffectHandleGetter;)V`: `.method public static final native EEEffectHandle_setMETEffectHandleGetterPtr(JLcom/bytedance/ies/effecteditor/swig/EEEffectHandle;JLcom/bytedance/ies/effecteditor/swig/EffectHa...`
- Line 66, `native_loading`, `native method`, `.method public static final native EEStdStringToStringMap_Iterator_getKey(JLcom/bytedance/ies/effecteditor/swig/EEStdStringToStringMap$Iterator;)Ljava/lang/String;`: `.method public static final native EEStdStringToStringMap_Iterator_getKey(JLcom/bytedance/ies/effecteditor/swig/EEStdStringToStringMap$Iterator;)Ljava/lang/String;`
- Line 69, `native_loading`, `native method`, `.method public static final native EEStdStringToStringMap_Iterator_getNextUnchecked(JLcom/bytedance/ies/effecteditor/swig/EEStdStringToStringMap$Iterator;)J`: `.method public static final native EEStdStringToStringMap_Iterator_getNextUnchecked(JLcom/bytedance/ies/effecteditor/swig/EEStdStringToStringMap$Iterator;)J`

### `smali_classes9/com/bytedance/ies/nle/editor_jni/NLEMediaPublicJniJNI.smali`

- Class: `Lcom/bytedance/ies/nle/editor_jni/NLEMediaPublicJniJNI`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `native_loading`, `native method`, `.method public static final native DLWCallback_change_ownership(Lcom/bytedance/ies/nle/editor_jni/DLWCallback;JZ)V`: `.method public static final native DLWCallback_change_ownership(Lcom/bytedance/ies/nle/editor_jni/DLWCallback;JZ)V`
- Line 51, `native_loading`, `native method`, `.method public static final native DLWCallback_compileDone(JLcom/bytedance/ies/nle/editor_jni/DLWCallback;)V`: `.method public static final native DLWCallback_compileDone(JLcom/bytedance/ies/nle/editor_jni/DLWCallback;)V`
- Line 54, `native_loading`, `native method`, `.method public static final native DLWCallback_compileError(JLcom/bytedance/ies/nle/editor_jni/DLWCallback;I)V`: `.method public static final native DLWCallback_compileError(JLcom/bytedance/ies/nle/editor_jni/DLWCallback;I)V`
- Line 57, `native_loading`, `native method`, `.method public static final native DLWCallback_director_connect(Lcom/bytedance/ies/nle/editor_jni/DLWCallback;JZZ)V`: `.method public static final native DLWCallback_director_connect(Lcom/bytedance/ies/nle/editor_jni/DLWCallback;JZZ)V`
- Line 60, `native_loading`, `native method`, `.method public static final native DLWCallback_onProgress(JLcom/bytedance/ies/nle/editor_jni/DLWCallback;F)V`: `.method public static final native DLWCallback_onProgress(JLcom/bytedance/ies/nle/editor_jni/DLWCallback;F)V`
- Line 63, `native_loading`, `native method`, `.method public static final native DynamicLightWaveUtil_cancelCompile(JLcom/bytedance/ies/nle/editor_jni/DynamicLightWaveUtil;)I`: `.method public static final native DynamicLightWaveUtil_cancelCompile(JLcom/bytedance/ies/nle/editor_jni/DynamicLightWaveUtil;)I`
- Line 66, `native_loading`, `native method`, `.method public static final native DynamicLightWaveUtil_compile(JLcom/bytedance/ies/nle/editor_jni/DynamicLightWaveUtil;Ljava/lang/String;ZJLcom/bytedance/ies/nle/editor_jni/DLWCallback;)I`: `.method public static final native DynamicLightWaveUtil_compile(JLcom/bytedance/ies/nle/editor_jni/DynamicLightWaveUtil;Ljava/lang/String;ZJLcom/bytedance/ies/nle/editor_jni/DLW...`
- Line 69, `native_loading`, `native method`, `.method public static final native DynamicLightWaveUtil_destroy(JLcom/bytedance/ies/nle/editor_jni/DynamicLightWaveUtil;)I`: `.method public static final native DynamicLightWaveUtil_destroy(JLcom/bytedance/ies/nle/editor_jni/DynamicLightWaveUtil;)I`

### `smali_classes15/com/bytedance/ies/smartmovie/jni/SmartMovieJniJNI.smali`

- Class: `Lcom/bytedance/ies/smartmovie/jni/SmartMovieJniJNI`
- Categories: `native_loading`
- Triggerability: `unknown`
- Claim boundary: static marker only; not a vulnerability until input control and reachable flow are shown

Findings:
- Line 48, `native_loading`, `native method`, `.method public static final native C3_get()Ljava/lang/String;`: `.method public static final native C3_get()Ljava/lang/String;`
- Line 51, `native_loading`, `native method`, `.method public static final native C3_set(Ljava/lang/String;)V`: `.method public static final native C3_set(Ljava/lang/String;)V`
- Line 54, `native_loading`, `native method`, `.method public static final native CommonRequestCallback_change_ownership(Lcom/bytedance/ies/smartmovie/jni/CommonRequestCallback;JZ)V`: `.method public static final native CommonRequestCallback_change_ownership(Lcom/bytedance/ies/smartmovie/jni/CommonRequestCallback;JZ)V`
- Line 57, `native_loading`, `native method`, `.method public static final native CommonRequestCallback_director_connect(Lcom/bytedance/ies/smartmovie/jni/CommonRequestCallback;JZZ)V`: `.method public static final native CommonRequestCallback_director_connect(Lcom/bytedance/ies/smartmovie/jni/CommonRequestCallback;JZZ)V`
- Line 60, `native_loading`, `native method`, `.method public static final native CommonRequestCallback_onFailure(JLcom/bytedance/ies/smartmovie/jni/CommonRequestCallback;ILjava/lang/String;JLcom/bytedance/ies/smartmovie/jni/UnorderedMapStrStr;)V`: `.method public static final native CommonRequestCallback_onFailure(JLcom/bytedance/ies/smartmovie/jni/CommonRequestCallback;ILjava/lang/String;JLcom/bytedance/ies/smartmovie/jni...`
- Line 63, `native_loading`, `native method`, `.method public static final native CommonRequestCallback_onSuccess(JLcom/bytedance/ies/smartmovie/jni/CommonRequestCallback;Ljava/lang/String;)V`: `.method public static final native CommonRequestCallback_onSuccess(JLcom/bytedance/ies/smartmovie/jni/CommonRequestCallback;Ljava/lang/String;)V`
- Line 66, `native_loading`, `native method`, `.method public static final native CompressMetaCallback_change_ownership(Lcom/bytedance/ies/smartmovie/jni/CompressMetaCallback;JZ)V`: `.method public static final native CompressMetaCallback_change_ownership(Lcom/bytedance/ies/smartmovie/jni/CompressMetaCallback;JZ)V`
- Line 69, `native_loading`, `native method`, `.method public static final native CompressMetaCallback_director_connect(Lcom/bytedance/ies/smartmovie/jni/CompressMetaCallback;JZZ)V`: `.method public static final native CompressMetaCallback_director_connect(Lcom/bytedance/ies/smartmovie/jni/CompressMetaCallback;JZZ)V`

## Next Review Steps

1. Start with `command_execution`, `dynamic_code_loading`, `webview_bridge`, and `tls_trust` packets.
2. For each packet, determine whether inputs are fixed, app-controlled, remotely configured, or externally attacker-controlled.
3. Correlate risky markers with exported components and deep links before making bug-bounty-style claims.
4. Escalate native-library findings to Ghidra only when Java/smali evidence points into JNI or `.so` behavior that affects privacy or security.
5. Record reviewed conclusions separately from this generated marker output.
