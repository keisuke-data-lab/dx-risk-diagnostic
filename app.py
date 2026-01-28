import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Failure Case Database (判例・事例データベース)
# -----------------------------------------------------------------------------
# 0-10のスコアで各事例の特徴を定義
# [req_ambiguity, decision_speed, multi_vendor_layer, user_incompetence]
FAILURE_CASES = {
    "Mizuho_2002 (みずほ銀行)": {
        "scores": [8, 10, 9, 4],
        "desc": "【複雑性の暴走】意思決定の遅れと、3行統合によるマルチベンダーの複雑化が原因。",
        "risk_type": "Complexity Overload"
    },
    "COCOA_App (COCOA)": {
        "scores": [7, 6, 10, 5],
        "desc": "【多重下請けの弊害】責任の所在が不明確になり、テスト工程と品質管理が機能不全に陥った。",
        "risk_type": "Supply Chain Fragility"
    },
    "SOFTIC_021 (九州屋事件)": {
        "scores": [4, 5, 2, 10],
        "desc": "【発注者能力の欠如】ベンダーに過失はなく、ユーザーが正しい業務要件を出せなかったために失敗。",
        "risk_type": "User Incompetence (GIGO)"
    },
    "7pay_Incident (セブンペイ)": {
        "scores": [9, 8, 5, 7],
        "desc": "【ガバナンス欠如】リリースの焦りからセキュリティ要件（2段階認証）を軽視し、即死撤退。",
        "risk_type": "Governance Failure"
    },
    "Healthy_Project (理想的な状態)": {
        "scores": [2, 2, 2, 2],
        "desc": "リスクがコントロールされた健全なプロジェクト状態。",
        "risk_type": "Low Risk"
    }
}

VARIABLES = {
    "req_ambiguity": "Requirement Immaturity (要件定義の未熟度)",
    "decision_speed": "Decision Latency (意思決定の遅延度)",
    "multi_vendor_layer": "Supply Chain Depth (多重下請け深度)",
    "user_incompetence": "Client Immaturity (発注者当事者能力の欠如)"
}

# -----------------------------------------------------------------------------
# 2. Logic Class
# -----------------------------------------------------------------------------
class RiskDiagnostic:
    def __init__(self, inputs):
        self.inputs = np.array(inputs) # User input vector

    def calculate_similarity(self):
        results = []
        for name, data in FAILURE_CASES.items():
            case_vector = np.array(data["scores"])
            
            # ユークリッド距離を計算
            dist = np.linalg.norm(self.inputs - case_vector)
            
            # 類似度スコア (距離0なら100%, 距離最大なら0%に正規化)
            # 4次元空間の最大距離(0,0,0,0 to 10,10,10,10)は20
            similarity = max(0, (1 - (dist / 20)) * 100)
            
            results.append({
                "case_name": name,
                "similarity": similarity,
                "description": data["desc"],
                "risk_type": data["risk_type"],
                "scores": data["scores"]
            })
        
        # 類似度順にソート
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

# -----------------------------------------------------------------------------
# 3. Streamlit UI
# -----------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Project Omen: Risk Diagnostic", layout="wide")

    st.title("⚖️ DX Project Failure Diagnostic")
    st.subheader("(Project Omen) 過去の失敗構造との類似性診断")
    
    st.markdown("""
    プロジェクトの構造的特徴（4変数）を入力すると、過去の日本のシステム開発における
    **「代表的な失敗事例（判例・炎上案件）」との類似度**を判定します。
    「成功するか」ではなく**「どのパターンで失敗しそうか」**を予見するためのガバナンスツールです。
    """)
    st.markdown("---")

    col_input, col_result = st.columns([1, 2])

    with col_input:
        st.header("🛠 Diagnostic Parameters")
        st.caption("各項目を 0(健全) 〜 10(深刻) で評価してください")
        
        val_req = st.slider(
            "1. 要件定義の未熟度", 0, 10, 5,
            help="スコア高：「走りながら決める」「要件がフワッとしている」状態"
        )
        val_decision = st.slider(
            "2. 意思決定の遅延度", 0, 10, 5,
            help="スコア高：持ち帰りが多い、ステコミが開催されない、決裁者が不明"
        )
        val_supply = st.slider(
            "3. 多重下請け深度", 0, 10, 5,
            help="スコア高：再委託・再々委託が常態化し、実作業者の顔が見えない"
        )
        val_client = st.slider(
            "4. 発注者能力の欠如", 0, 10, 5,
            help="スコア高：丸投げ体質、現行業務を理解している担当者が不在"
        )
        
        user_inputs = [val_req, val_decision, val_supply, val_client]
        
        st.info("""
        **変数の定義:**
        * **Req Ambiguity**: SOFTIC 009（仕様凍結未完了）リスク
        * **Decision Latency**: Mizuho（複雑性の暴走）リスク
        * **Supply Chain**: COCOA（責任不在）リスク
        * **Client Immaturity**: SOFTIC 021（九州屋パラドックス）リスク
        """)

    # --- Calculation ---
    diagnostic = RiskDiagnostic(user_inputs)
    results = diagnostic.calculate_similarity()
    top_match = results[0]

    with col_result:
        st.header("📊 Diagnosis Result")
        
        # Top Match Alert
        if top_match["case_name"] == "Healthy_Project (理想的な状態)":
            st.success(f"✅ **診断結果: 健全な状態です** (類似度: {top_match['similarity']:.1f}%)")
        else:
            st.error(f"⚠️ **警告: 「{top_match['case_name']}」型のリスク構造に酷似しています**")
            st.metric("類似度 (Similarity Score)", f"{top_match['similarity']:.1f}%", delta="High Risk", delta_color="inverse")
            st.markdown(f"**判定根拠:** {top_match['description']}")

        # Radar Chart
        categories = list(VARIABLES.values())
        
        fig = go.Figure()
        
        # User Project
        fig.add_trace(go.Scatterpolar(
            r=user_inputs,
            theta=categories,
            fill='toself',
            name='Your Project',
            line_color='blue',
            opacity=0.8
        ))
        
        # Match Case
        fig.add_trace(go.Scatterpolar(
            r=top_match["scores"],
            theta=categories,
            fill='toself',
            name=f"Reference: {top_match['case_name']}",
            line_color='red',
            opacity=0.3,
            line_dash='dot'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10])
            ),
            showlegend=True,
            title="Structural Comparison (構造比較レーダー)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table of Distances
        st.subheader("Reference Case Analysis")
        df_res = pd.DataFrame(results)
        df_res = df_res[["case_name", "similarity", "risk_type"]].copy()
        df_res.columns = ["事例名 (Reference)", "類似度 (%)", "リスク類型"]
        st.dataframe(df_res.style.background_gradient(subset=["類似度 (%)"], cmap="Reds"), use_container_width=True)

if __name__ == "__main__":
    main()