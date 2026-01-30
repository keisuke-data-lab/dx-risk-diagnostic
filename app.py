import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Failure Case Database
# -----------------------------------------------------------------------------
FAILURE_CASES = {
    "Mizuho_2002 (みずほ銀行)": {
        "scores": [9, 10, 10, 6],
        "desc": "【複雑性の暴走】意思決定の遅れと、3行統合によるマルチベンダーの複雑化が原因。",
        "risk_type": "Complexity Overload"
    },
    "7pay_Incident (セブンペイ)": {
        "scores": [5, 2, 4, 9],
        "desc": "【ガバナンス欠如】経営層のIT無理解。セキュリティ要件を軽視し、即死撤退に追い込まれた。",
        "risk_type": "Governance Fail"
    },
    "COCOA_App (COCOA)": {
        "scores": [8, 8, 9, 8],
        "desc": "【責任の蒸発】多重下請け構造により、テスト工程の責任者が不在化し、不具合が放置された。",
        "risk_type": "Supply Chain Fragility"
    },
    "JCB_Vendor (JCB基幹)": {
        "scores": [9, 8, 7, 5],
        "desc": "【ベンダー崩壊】要件が決まらないまま開発を強行し、過度な増員（人海戦術）で現場が瓦解。",
        "risk_type": "Death March"
    },
    "SOFTIC_009 (タグ事件)": {
        "scores": [9, 9, 3, 7],
        "desc": "【要件肥大化】ユーザーの追加要望が止まらず、仕様凍結ができないまま法的紛争に発展。",
        "risk_type": "Scope Creep"
    },
    "SOFTIC_021 (九州屋事件)": {
        "scores": [10, 3, 1, 10],
        "desc": "【ユーザー過失】ベンダーに過失はなく、発注者の業務理解不足によりシステムが適合しなかった。",
        "risk_type": "User Competence Fail (GIGO)"
    },
    "Healthy_Project (理想基準)": {
        "scores": [2, 2, 2, 2], # 現実的な健全ラインはALL1ではなく2程度
        "desc": "リスクがコントロールされた健全なプロジェクト状態。",
        "risk_type": "Baseline (Success)"
    }
}

VARIABLES = {
    "req_ambiguity": "Requirement (要件)",
    "decision_speed": "Decision (決断)",
    "multi_vendor_layer": "SupplyChain (商流)",
    "user_incompetence": "ClientCap (能力)"
}

# -----------------------------------------------------------------------------
# 2. Logic Class
# -----------------------------------------------------------------------------
class RiskDiagnostic:
    def __init__(self, inputs):
        self.inputs = np.array(inputs)

    def calculate_similarity(self):
        results = []
        for name, data in FAILURE_CASES.items():
            case_vector = np.array(data["scores"])
            
            # ユークリッド距離
            dist = np.linalg.norm(self.inputs - case_vector)
            
            # 類似度スコア (最大距離20に対して正規化)
            # 距離0で100%, 距離10で50%, 距離20で0%
            similarity = max(0, (1 - (dist / 20)) * 100)
            
            results.append({
                "case_name": name,
                "similarity": similarity,
                "description": data["desc"],
                "risk_type": data["risk_type"],
                "scores": data["scores"]
            })
        
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

# -----------------------------------------------------------------------------
# 3. Streamlit UI
# -----------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Project Omen: Risk Diagnostic", layout="wide")

    st.title("⚖️ DX Project Failure Diagnostic")
    st.markdown("""
    **「歴史は繰り返さないが、韻を踏む」**
    あなたのプロジェクトのリスク構造が、過去のどの「大失敗事例」と似ているかを診断します。
    """)
    st.markdown("---")

    col_input, col_result = st.columns([1, 2])

    with col_input:
        st.subheader("🛠 Diagnostic Inputs")
        
        def score_slider(label, key_desc):
            return st.slider(
                label, 0, 10, 5, 
                help=f"0(健全) ⇔ 10(危険): {key_desc}"
            )

        # 定義の明確化
        val_req = score_slider("1. 要件定義の未熟度", "仕様未確定のまま開発進行 / 走りながら考える")
        val_decision = score_slider("2. 意思決定の遅延度", "持ち帰り頻発 / 決裁権限者の不在")
        val_supply = score_slider("3. 多重下請け深度", "再委託・再々委託 / 実装者の顔が見えない")
        val_client = score_slider("4. 発注者能力の欠如", "丸投げ体質 / 現行業務フローが不明")
        
        user_inputs = [val_req, val_decision, val_supply, val_client]
        
        st.info("💡 **Hint:** 自分たちを良く見せようとせず、最悪の想定で入力してください。")

    # --- Calculation ---
    diagnostic = RiskDiagnostic(user_inputs)
    results = diagnostic.calculate_similarity()
    top_match = results[0]

    with col_result:
        st.subheader("📊 Diagnosis Result")
        
        # 閾値ロジック (類似度が60%未満なら「該当なし」とする安全策)
        THRESHOLD_SIMILARITY = 60.0

        if top_match["case_name"] == "Healthy_Project (理想基準)":
             st.success(f"✅ **健全な状態です** (類似度: {top_match['similarity']:.1f}%)")
             alert_level = "Safe"
        elif top_match['similarity'] < THRESHOLD_SIMILARITY:
            st.warning(f"⚠️ **判定不能（Unclassified Risk）**\n\nどの過去事例とも構造が異なりますが、リスクが高い可能性があります（類似度 {top_match['similarity']:.1f}%）。")
            alert_level = "Unknown"
        else:
            st.error(f"💀 **警告: 「{top_match['case_name']}」の再来**")
            st.markdown(f"**Structural Similarity:** `{top_match['similarity']:.1f}%`")
            st.write(f"**死因分析:** {top_match['description']}")
            alert_level = "Danger"

        # Radar Chart
        # データを閉じるために、最初の要素を最後に追加する
        categories = list(VARIABLES.values())
        categories_closed = categories + [categories[0]]
        
        user_inputs_closed = user_inputs + [user_inputs[0]]
        
        fig = go.Figure()
        
        # ユーザー入力 (線を太く、塗りを薄くして重なりを防ぐ)
        fig.add_trace(go.Scatterpolar(
            r=user_inputs_closed, theta=categories_closed, fill='toself', name='Your Project',
            line_color='#1f77b4', line_width=3, opacity=0.4
        ))
        
        # 比較対象 (破線で表示)
        if alert_level != "Unknown":
            ref_name = top_match["case_name"].split(" ")[0]
            top_match_scores_closed = top_match["scores"] + [top_match["scores"][0]]
            fig.add_trace(go.Scatterpolar(
                r=top_match_scores_closed, theta=categories_closed, fill='none', name=f"Ref: {ref_name}",
                line_color='#d62728', line_width=2, line_dash='dot'
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            title="Structural Gap Analysis",
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Rankings (データフレーム表示の改善)
        with st.expander("全事例との類似度ランキング (詳細)"):
            df_res = pd.DataFrame(results)
            df_display = df_res[["case_name", "similarity", "risk_type"]].copy()
            df_display["similarity"] = df_display["similarity"].apply(lambda x: f"{x:.1f}%")
            st.table(df_display)

if __name__ == "__main__":
    main()