# 大容診所看診小工具 - 專案進度與技術手冊 (PROGRESS)

## 🚀 核心工具儀表板 (Dashboard)
| 工具名稱 | 最後更新 | 核心功能 | 連結 |
| :--- | :--- | :--- | :--- |
| **SGLT2i 健保給付評估** | 2026/05/08 | 整合 2025/03 擴大給付 (HF/CKD/DM) | `tools/nhi/sglt2i_calculator.html` |
| **代謝/痛風風險評估** | 2026/05/08 | 2024 指引判定、藥物選擇與健保規範 | `tools/gout/gout_calculator.html` |
| **CVD 風險計算器** | 2026/05/08 | TwCCCC (2023) & ASCVD 模型 | `tools/cvd/cvd_calculator.html` |
| **健保降血脂給付評估** | 2026/05/08 | 2.6.1 規範、SOAP Note 一鍵複製 | `tools/nhi/statin_reimbursement.html` |
| **腎功能 eGFR 計算器** | 2026/05/08 | CKD-EPI (2021) 與 MDRD 雙公式 | `tools/renal/egfr_calculator.html` |
| **10年慢性病風險評估** | 2026/05/09 | 國健署 10 年風險模型 (預留單機版介接) 與處置建議 | `tools/hpa/hpa_risk_calculator.html` |
| **HPA 成人健檢摘要** | 2026/05/09 | 2025 新制 (30歲起、增項尿酸) 與風險預測模型 | `tools/hpa/adult_health_checkup_summary.md` |
| **血脂自動換算** | 2026/05/09 | Friedewald 公式四項參數換算 (修正手動計算) | `tools/lipid/lipid_calculator.html` |

## 🧠 醫學邏輯與健保規範摘要 (Medical Logic)
### 1. SGLT2 抑制劑 (2025/03 擴大給付)
*   **HF:** LVEF ≤ 49% 且有症狀。
*   **CKD:** eGFR 25-60 且 UACR 200-5000 (需加入照護計畫)。
*   **DM:** 需先用過 Metformin，不可併用健保給付之 GLP-1 RA (胰妥讚、易週糖)。

### 2. 高尿酸血症與痛風 (2024 指引)
*   **ULT 啟動:** 痛風石、關節受損、頻繁發作、或 CKD 3+ (sUA > 7.0)。
*   **藥物選擇:** Febuxostat (CKD 第一線)、Allopurinol (基因篩檢)、Benzbromarone (結石禁忌)。

### 3. 心血管風險與血脂 (2024 指引)
*   **模型:** TwCCCC (本土) 與 ASCVD (PCE)。
*   **降血脂:** 健保 2.6.1 規範 (2021)。

## 📜 開發歷史紀錄 (Development History)
### 2026-05-09 (血脂工具修正與規範強化)
- **新功能:** 實作「10年慢性病風險評估」前端工具。整合 35-70 歲國人本土風險模型參數，並提供紅、黃、綠燈分級處置建議，預留國健署官方「單機版 SDK」串接介面。
- **Bug Fix:** 修正「血脂自動換算」工具。移除即時監聽邏輯，改為「開始計算」按鈕觸發，提升計算穩定性。
- **Dashboard 更新:** 同步更新 `index.html` 工具卡片日期。
- **規範強化:** 於 `GEMINI.md` 增加準則，要求未來工具異動需同步更新首頁日期。

### 2026-05-08 (重大更新：自動化與擴充)
- **基礎建設:** 安裝 Git 並自動化 GitHub 同步 (Repository: `clinictools`)。
- **功能開發:** 完成「SGLT2i 健保評估」與「痛風風險評估」兩大工具。
- **文件整合:** 廢除 `SUMMARY.md` 與 `SESSION_LOG.md`，統一使用 `PROGRESS.md`。

### 2026-05-07 以前 (初期開發)
- 完成 CVD、eGFR、血脂換算基礎工具。
- 實作 SOAP Note 一鍵複製功能於降血脂工具。
- 整合 `index.html` 診所首頁。

## 📅 未來擴充計畫 (Future Tasks)
- [ ] 介接 **HPA 慢性病風險評估** 官方單機版 SDK (等待申請核可)。
- [ ] 增加 **15 年中風風險** 計算 (TwCCCC Stroke Model)。
- [ ] 增加 **心房顫動 (Af)** 之 CHADS2/CHA2DS2-VASc 評分。
- [ ] 串接更多健保藥物 (如高血壓、抗血小板藥物) 的給付門檻。

---
*整理日期：2026/05/09 | 系統版本：1.1.1 Alpha*
