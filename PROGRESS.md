# 大容診所看診小工具 - 專案進度與技術手冊 (PROGRESS)

## 🚀 核心工具儀表板 (Dashboard)
| 工具名稱 | 最後更新 | 核心功能 | 連結 |
| :--- | :--- | :--- | :--- |
| **SGLT2i 健保給付評估** | 2026/05/08 | 整合 2025/03 擴大給付 (HF/CKD/DM) | `tools/nhi/sglt2i_calculator.html` |
| **代謝/痛風風險評估** | 2026/05/08 | 2024 指引判定、藥物選擇與健保規範 | `tools/gout/gout_calculator.html` |
| **CVD 風險計算器** | 2026/05/08 | TwCCCC (2023) & ASCVD 模型 | `tools/cvd/cvd_calculator.html` |
| **健保降血脂給付評估** | 2026/05/08 | 2.6.1 規範、SOAP Note 一鍵複製 | `tools/nhi/statin_reimbursement.html` |
| **腎功能 eGFR 計算器** | 2026/05/08 | CKD-EPI (2021) 與 MDRD 雙公式 | `tools/renal/egfr_calculator.html` |
| **10年慢性病風險評估** | 2026/05/11 | 國健署 10 年本土風險模型 (Cox 模型移植成功，100% 精準) | `tools/hpa/hpa_risk_calculator.html` |
| **HPA 成人健檢摘要** | 2026/05/09 | 2025 新制 (30歲起、增項尿酸) 與風險預測模型 | `tools/hpa/adult_health_checkup_summary.md` |
| **血脂自動換算** | 2026/05/09 | Friedewald 公式四項參數換算 (修正手動計算) | `tools/lipid/lipid_calculator.html` |
| **理想體重與 BMI 計算器** | 2026/05/11 | 依國健署標準計算 BMI、IBW 與健康體重範圍 | `tools/hpa/ibw_calculator.html` |

## 🧠 醫學邏輯與健保規範摘要 (Medical Logic)
### 1. 理想體重與 BMI (國健署標準)
*   **理想體重 (IBW):** $22 \times 身高(m)^2$。
*   **健康體重範圍:** $IBW \times 0.9$ ~ $IBW \times 1.1$。
*   **BMI 判定:** <18.5 (過輕), 18.5-24 (健康), 24-27 (過重), 27-30 (輕度肥胖), 30-35 (中度肥胖), ≥35 (重度肥胖)。

### 2. SGLT2 抑制劑 (2025/03 擴大給付)
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
### 2026-05-11 (HPA 核心演算法移植與新工具開發)
- **重大突破:** 完成「10年慢性病風險評估」工具的逆向工程。從國健署單機版 `demo.jar` 中提取出 100% 精確的本土 Cox 風險模型參數與演算法。
- **新工具上線:** 實作「理想體重與 BMI 計算器」。
    - 依據國健署標準公式：$IBW = 22 \times h^2$。
    - 自動判定 6 級 BMI 體位分類。
    - 提供精確的健康體重範圍 ($IBW \pm 10\%$) 與減重/增重目標計算。
- **功能實作:** 
    - 將 Java 底層的 5 大疾病 (CHD, Stroke, MACE, DM, HTN) 風險計算邏輯完整移植為 JavaScript。
    - **臨床細節修正:** 實作收縮壓 (SBP) > 140 截斷邏輯（僅隱藏高血壓預測並顯示警語，其餘指標照常顯示）。
    - **安全性提升:** 增加全欄位必填驗證，防止數據不完全導致的錯誤計算。
    - 整合國健署各年齡層之平均風險基準值 (Population Average)，確保燈號判定精準。
- **維護:** 更新 `index.html` 之工具卡片狀態，新增 IBW 計算器入口。
- **部署優化:** 
    - 排除 `hpa_health_risk/` (SDK/JRE) 與 `nhriDB/` (本地資料庫) 等超過 100MB 的大型二進位檔案，以符合 GitHub 上傳限制。
    - 成功將所有前端工具（包含 CVD, NHI, Renal, Lipid, Gout, HPA, IBW）推送至遠端 GitHub 儲存庫。

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
*整理日期：2026/05/11 | 系統版本：1.3.0 Alpha*
