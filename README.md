# mymis｜Product Analytics Lab

我把產品分析裡最常被分散處理的三件事放在同一個小工具裡：A/B test、funnel，以及 event data contract。

這個 repo 沒有接第三方分析平台，也沒有用大型資料科學框架。原因很簡單：我想先把統計假設、事件品質與轉換率計算本身寫清楚，再談視覺化。

## 內容

- **Experiment**：二元轉換率比較、absolute / relative lift、雙尾 z-test
- **SRM**：sample ratio mismatch 檢查，避免流量分配異常時還硬看實驗結果
- **Funnel**：每一步相對起點、相對前一步的轉換與 drop-off
- **Event contract**：必要欄位與重複 event id 檢查

## 執行

```bash
python -m unittest discover -s tests -v
python demo.py
```

## 為什麼做這個

產品分析最容易犯的錯，不是少畫一張圖，而是資料本身不可信、實驗分流已經壞掉，卻還在解讀 lift。這個 repo 故意把「先檢查資料，再分析結果」放在同一條流程裡。

## 限制

- 目前只處理二元轉換率
- z-test 適合樣本量夠大的情境
- SRM 預設 50/50，也可以自行帶 expected share
- event contract 目前是輕量檢查，不是完整 schema registry
