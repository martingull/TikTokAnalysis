# Source Reconstruction Status

This artifact shows the handoff from generated source packets to reviewed source evidence.

## Summary

| Metric | Count |
| --- | --- |
| Generated packets | 10 |
| Reviewed packets | 10 |
| Not reviewed | 0 |
| Packets with JADX context | 2 |
| Reviewed likely false positives | 1 |

## Packet Status

| Priority | Packet | Class | Categories | JADX | Review status |
| --- | --- | --- | --- | --- | --- |
| 1 | `smali_classes17/com/google/android/gms/ads/identifier/AdvertisingIdClient.smali` | `Lcom/google/android/gms/ads/identifier/AdvertisingIdClient` | identifiers, network_telemetry | yes | reviewed, static-only |
| 2 | `smali_classes17/com/bytedance/helios/statichook/config/ApiHookConfig.smali` | `Lcom/bytedance/helios/statichook/config/ApiHookConfig` | camera_microphone, contacts_accounts, identifiers, installed_apps, location, network_telemetry | yes | reviewed, static-only |
| 3 | `smali_classes40/com/byted/cast/capture/audio/AudioRecorder$AudioThread.smali` | `Lcom/byted/cast/capture/audio/AudioRecorder$AudioThread` | camera_microphone | no | reviewed, static-only |
| 4 | `smali_classes17/X/0eGv.1.smali` | `LX/0eGv` | camera_microphone, contacts_accounts, dynamic_loading, identifiers, installed_apps, local_storage, location, network_telemetry | no | reviewed, static-only |
| 5 | `smali_classes16/X/0awA.2.smali` | `LX/0awA` | installed_apps | no | reviewed, static-only |
| 6 | `smali_classes17/X/0dMp.1.smali` | `LX/0dMp` | local_storage | no | reviewed, static-only |
| 7 | `smali_classes17/com/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener.smali` | `Lcom/bytedance/apm/agent/instrumentation/okhttp3/OkHttpEventListener` | network_telemetry | no | reviewed, static-only |
| 8 | `smali_classes11/X/0PuX.2.smali` | `LX/0PuX` | dynamic_loading | no | reviewed, likely false-positive static signal |
| 9 | `smali_classes18/com/bytedance/android/live/wallet/WalletExchange.smali` | `Lcom/bytedance/android/live/wallet/WalletExchange` | command_execution, local_storage | no | reviewed, static-only |
| 10 | `smali_classes19/com/ss/android/vesdk/audio/TEAudioRecord.smali` | `Lcom/ss/android/vesdk/audio/TEAudioRecord` | camera_microphone | no | reviewed, static-only |

## Interpretation

- `source_findings.md` is generated triage and should not be treated as reviewed evidence by itself.
- `reviewed_source_notes.md` is the human/Codex-reviewed interpretation layer.
- Publishable source claims should be based on reviewed notes and line-cited smali evidence.
- JADX is a reading aid; apktool smali remains the evidence layer for claims.
