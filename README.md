# Anime1.me 下載器
## 使用方法
1. 設定 ```config.json```
   - ```download_path```：儲存位置
   - ```web_wait_time```：瀏覽器等待時間，根據網路速度調整
3. 運行 ```main.py``` / ```main.exe```
4. 複製連結 anime1.me (一集／整季)

## 特點
1. 多線程處理
2. 自定義儲存位置
3. 自動資料夾建立和管理

## 例子
```
Web url ('exit' to quit): https://anime1.me/25222

DevTools listening on ws://127.0.0.1:61201/devtools/browser/330afa07-e80f-45ad-b26f-ff908ab31b6c
Access https://anime1.me/25222
[28212:21136:0301/123846.472:ERROR:fallback_task_provider.cc(126)] Every renderer should have at least one task provided by a primary task provider. If a "Renderer" fallback task is shown, it is a bug. If you have repro steps, please file a new bug and tag it as a dependency of crbug.com/739782.
Title: 歡迎來到日本，妖精小姐。
Target folder: ./歡迎來到日本，妖精小姐。
1 ready to download.
Start processing for 歡迎來到日本，妖精小姐。_08
Video 歡迎來到日本，妖精小姐。_08 saved in ./歡迎來到日本，妖精小姐。\歡迎來到日本，妖精小姐。_08.mp4.
[18496:6920:0301/123919.004:ERROR:video_hover_overlay_agent.cc(49)] Connection to VideoHoverOverlayDriver dropped
Web url ('exit' to quit): exit
```
