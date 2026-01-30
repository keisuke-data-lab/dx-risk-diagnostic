# DX Project Risk Diagnostic (Project Omen)
**過去の炎上事例（判例）との類似性を判定するガバナンス・ツール**
## 🛠 Business Value / Concept
**「なぜ、人は足りないのにプロジェクトは遅れるのか？」**

本ツールは、**システムダイナミクス理論**および**ブルックスの法則**（"遅れているソフトウェアプロジェクトへの要員追加は、さらに遅らせるだけである"）に基づき、プロジェクト遅延のメカニズムを可視化する**意思決定支援システム（DSS）のプロトタイプ**です。

PMBOK等の管理手法では見落とされがちな**「コミュニケーションコストの増大」**や**「技術的負債による生産性低下」**を数理モデル化し、安易なリソース投入が引き起こす「デスマーチ（死の行進）」のリスクを定量的にシミュレーションします。

**【主な活用シーン】**
* **経営層・発注者への啓蒙:** 無理な短納期要請や仕様変更が、品質と納期に与える破壊的影響を可視化する。
* **リスク管理:** 「どのタイミングで、何人までなら追加投入しても安全か」の境界線を算出する。


[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dx-risk-diagnostic-etshqp5dvhv6pwbvzacarb.streamlit.app/)
> **👆 Click to Run App**: あなたのプロジェクトが「どの失敗パターン」に似ているかを診断します。

## 📌 Overview
**「成功する方法は様々だが、失敗する構造は常に同じである」**

本ツールは、日本のシステム開発における過去の代表的な失敗事例（Mizuho, COCOA, SOFTIC判例など）を構造化データとして定義し、診断対象プロジェクトとの**ユークリッド距離（類似度）**を算出する診断エンジンです。
PMの「勘」ではなく、過去の「死に至る病（失敗のDNA）」との距離を計測することで、プロジェクト開始前の**「損切り（Stop Loss）」**や**「体制見直し」**を支援します。

## 🔍 Diagnostic Logic
以下の4つの構造的変数を入力とし、過去の失敗ケースとのマッチングを行います。

| Variable | Meaning | Critical Failure Case |
| :--- | :--- | :--- |
| **Requirement Ambiguity** | 要件の未熟度 | **SOFTIC 009 (タグ事件)**: 仕様未定のまま進めた結果の法的紛争 |
| **Decision Latency** | 意思決定の遅延 | **Mizuho 2002**: 複雑性と決定遅延によるシステム統合不全 |
| **Supply Chain Depth** | 多重下請け深度 | **COCOA**: 責任所在の不明確化による品質崩壊 |
| **Client Immaturity** | 発注者能力の欠如 | **SOFTIC 021 (九州屋型)**: ユーザーの業務理解不足によるプロジェクト頓挫 |

| Case Name (ID) | Category (類型) | Root Cause (死因・教訓) |
| :--- | :--- | :--- |
| **Mizuho_2002**<br>(みずほ銀行) | Complexity Overload<br>(複雑性の暴走) | **意思決定不全 (Decision Latency):**<br>複数ベンダーの利害調整に失敗し、仕様が統合されないままリリースを強行。 |
| **7pay_Incident**<br>(セブンペイ) | Governance Fail<br>(ガバナンス欠如) | **経営の無理解 (Client Immaturity):**<br>セキュリティ（2段階認証）の欠如を経営層が認識せず、サービス開始直後に即死撤退。 |
| **COCOA_App**<br>(COCOA) | Supply Chain Fragility<br>(多重下請け) | **責任所在の蒸発 (Supply Chain Depth):**<br>再委託が繰り返され、テスト工程の責任者が不在化。バグが数ヶ月放置された。 |
| **JCB_Vendor**<br>(JCB基幹) | Death March<br>(ベンダー崩壊) | **要件の未決 (Req Immaturity):**<br>要件が決まらないまま開発に着手し、人海戦術（増員）で解決しようとして現場が崩壊。 |
| **SOFTIC 009**<br>(タグ事件) | Scope Creep<br>(要件肥大化) | **法的紛争 (Legal Dispute):**<br>ユーザーが追加要望を繰り返し、要件を確定させなかったことによる債務不履行争い。 |
| **SOFTIC 021**<br>(九州屋事件) | **User Competence Fail**<br>(ユーザー過失) | **GIGO (Garbage In, Garbage Out):**<br>ベンダーに過失はなかったが、ユーザーの提供情報が誤っていたためシステムが不適合。 |

### The "Kyushuuya" Paradox (SOFTIC 021)
特筆すべきは「九州屋事件」です。ベンダーに過失はなく、バグもありませんでしたが、**「ユーザー（発注者）の業務理解不足」**によりプロジェクトは失敗しました。本ツールは、この「ユーザー起因のリスク」を検知できる点が特徴です。

## 📊 Related Tool
**定量的な「赤字額」をシミュレーションしたい場合はこちら**
> **[💸 DX Project Budget Simulator](https://github.com/keisuke-data-lab/dx-project-failure-structure)**
> 技術的負債や手戻りが引き起こす「財務的損失（円）」を計算するシミュレーター

---
## 🛠 Tech Stack
* **Algorithm**: Case-Based Reasoning (k-NN approach)
* **Visualization**: Plotly (Radar Chart)
* **Framework**: Streamlit

---
**Created by Keisuke Nakamura**
