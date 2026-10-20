# temple-cards

「台灣廟口研究所」FB 每日貼文圖卡（由排程任務自動產生並上傳）。

- `plan.py`：依日期決定當天發「神明聖誕」（農曆神明生日）或「廟口故事」（30 題輪流，神明日順延）。`pip install lunardate` 後 `python3 plan.py [YYYY-MM-DD]`。
- `make_card.py`：產生 1080×1350 圖卡。`python3 make_card.py "標題\n第二行" "副標" 編號 輸出.png [神明聖誕]`
- `cards/YYYY-MM-DD.png`：每日圖卡，Metricool 由 raw 網址抓取。

神明生日表可直接改 `plan.py` 的 `DEITY`；廟口主題改 `TOPICS`。
