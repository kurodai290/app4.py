import streamlit as st
import random

# 1. ページの設定
st.set_page_config(page_title="最強経営シミュレーター", layout="centered")

# 2. データの初期化（これを書かないとエラーになります）
if 'money' not in st.session_state:
    st.session_state.money = 5000
    st.session_state.staff = 0
    st.session_state.share = 5
    st.session_state.is_listed = False
    st.session_state.logs = ["ゲーム開始！"]

# 3. 画面表示
st.title("🏢 会社経営シミュレーター")

# ステータスを横並びに表示
col1, col2, col3 = st.columns(3)
col1.metric("総資産", f"{st.session_state.money:,}円")
col2.metric("市場シェア", f"{st.session_state.share}%")
col3.metric("従業員数", f"{st.session_state.staff}名")

if st.session_state.is_listed:
    st.success("★ 上場企業 ★")

# 4. アクションボタン
st.subheader("実行アクション")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("営業活動 (+100円)"):
        st.session_state.money += 100
        st.session_state.logs.insert(0, "営業で100円稼ぎました。")

with c2:
    if st.button("社員採用 (1,000円)"):
        if st.session_state.money >= 1000:
            st.session_state.money -= 1000
            st.session_state.staff += 1
            st.session_state.logs.insert(0, "社員を1名採用しました。")
        else:
            st.error("資金不足！")

with c3:
    if st.button("商品開発 (5,000円)"):
        if st.session_state.money >= 5000:
            st.session_state.money -= 5000
            up = random.randint(1, 10)
            st.session_state.share += up
            st.session_state.logs.insert(0, f"新商品ヒット！シェアが{up}%上昇。")
        else:
            st.error("資金不足！")

st.divider()

# 5. 特殊アクション（上場）
if not st.session_state.is_listed:
    if st.button("🚀 株式上場 (条件: 5万円 & シェア30%)"):
        if st.session_state.money >= 50000 and st.session_state.share >= 30:
            st.session_state.money += 200000
            st.session_state.is_listed = True
            st.session_state.logs.insert(0, "祝・上場！200,000円の調達に成功！")
            st.balloons()
        else:
            st.warning("条件を満たしていません。")

# 6. 収益計算（ここが今回のポイント！）
if st.button("☕ ターンを終了して収益を得る"):
    s = st.session_state.staff
    base_income = 0

    # 社員数に応じた段階的収益
    if 1 <= s <= 10:
        base_income = 100
    elif 11 <= s <= 50:
        base_income = 1000
    elif 51 <= s <= 100:
        base_income = 10000
    elif s > 100:
        base_income = s * 100
    
    # シェア倍率を適用
    income = int(base_income * (1 + st.session_state.share / 100))
    # 税金（30%）
    tax = int(income * 0.3) if income > 0 else 0
    st.session_state.money += (income - tax)
    
    st.session_state.logs.insert(0, f"期末決算：収益{income}円（税引後）を獲得！")
    st.rerun()

# 7. 履歴の表示
st.subheader("経営履歴")
for log in st.session_state.logs[:5]:
    st.text(log)
