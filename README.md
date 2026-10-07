# mymis｜Product Analytics Lab

[![ci](https://github.com/Miiduoa/mymis/actions/workflows/ci.yml/badge.svg)](https://github.com/Miiduoa/mymis/actions/workflows/ci.yml)

產品實驗真正麻煩的不是畫 uplift 圖，而是先回答幾個問題：分流有沒有壞、樣本量夠不夠、主要指標有沒有改善、guardrail 有沒有惡化，以及上線後使用者到底有沒有留下來。

這個 repo 把這幾件事放在同一個小型、可測試的 Python core。

## Review path

| 問題 | 位置 |
|---|---|
| A/B test、confidence interval、SRM、MDE | `src/mymis/experiment.py` |
| ship / hold / reject 規則 | `src/mymis/decision.py` |
| weekly cohort retention | `src/mymis/retention.py` |
| funnel | `src/mymis/funnel.py` |
| event contract | `src/mymis/contracts.py` |
| regression tests | `tests/test_core.py` |

## Experiment flow

```text
event quality
    ↓
sample ratio mismatch?
    ↓
primary metric + confidence interval
    ↓
guardrails
    ↓
ship / hold / reject / inconclusive
    ↓
post-launch retention
```

### Binary experiment

`compare_binary` 回傳：

- control / variant conversion rate
- absolute / relative lift
- two-sided z-test p-value
- absolute lift confidence interval

`minimum_detectable_lift` 用 equal-sized binary experiment 的常態近似，回答「這個樣本量大約能看到多大的差異」，而不是等結果出來才決定實驗夠不夠久。

### SRM first

`sample_ratio_mismatch` 先檢查實際流量是否明顯偏離預期分配。SRM 被標記時，decision 直接回 `invalid`，不再拿一個已經可疑的分流去解讀 uplift。

### Guardrails

`check_guardrails` 接受明確的 relative tolerance。

例如 crash-free rate 從 99.5% 掉到 98%，即使 conversion 上升，也可以先回 `hold`，避免把「主要指標變好」誤當成「整體產品變好」。

## Weekly retention

`weekly_retention` 從 user-level events 建 calendar-week cohort：

- cohort 取每個人的第一次 signup
- 同一 user 在同一週只算一次
- signup 前的事件忽略
- timestamp 必須包含 timezone
- `reporting_timezone` 明確決定週界線
- 可限制哪些 event 算 active

這裡刻意使用 reporting timezone，而不是先全部轉成 UTC 再切週，避免週日深夜／週一凌晨在台灣報表裡被分到錯的 cohort week。

## Funnel

`summarize_funnel` 同時保留：

- relative to start
- relative to previous step
- drop-off from previous step

Funnel 與 retention 分開，因為「這次流程走到哪裡」和「之後有沒有回來」不是同一個問題。

## Run

Python 3.11+，核心只用標準函式庫。

```bash
python -m unittest discover -s tests -v
python demo.py
```

## Scope

- 只處理 binary conversion experiment
- MDE 是近似值，不是完整 power-analysis package
- guardrail tolerance 必須依產品情境事先定義
- retention 是 calendar-week retention，不是 rolling 7-day retention
- demo 使用合成資料，不代表真實產品績效

這個作品的重點不是「會算 p-value」，而是把 **資料品質 → 實驗有效性 → 決策 → retention** 放在同一條可 review 的流程裡。
