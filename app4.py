import streamlit as st
import random
import time

# 1. ページの設定
st.set_page_config(page_title="最強経営シミュレーター", layout="centered")

# 2. データの初期化
if 'money' not in st.session_state:
    st.session_state.money = 5000
    st.session_state.staff = 0
    st.session_state.share = 5
    st.session_state.month = 1
    st.session_state.last_time = time.time() # 前回の月更新時間
    st.session_state.is_listed = False
    st.session_state.logs = ["ゲーム開始！20分ごとに月が替わります。"]

# 定数設定
MONTH_DURATION = 1200  # 1ヶ月 = 20分 (1200秒)

# 3. 時間経過による月更新チェック
current_time = time.time()
elapsed = current_time - st.session_state.last_time
remaining = max(0, int(MONTH_DURATION - elapsed))

# 月更新のロジックを関数化
def next_month():
    s = st.session_state.staff
    # --- 収益計算 ---
    base_income = 0
    if 1 <= s <= 10: base_income = 100
    elif 11 <= s <= 50: base_income = 1000
    elif 51 <= s <= 100: base_income = 10000
    elif s > 100: base_income = s * 100
    
    income = int(base_income * (1 + st.session_state.share / 100))
    
    # --- 経費計算 ---
    salary_cost = s * 50  # 人件費: 1人50円
    office_cost = 500     # 諸経費(固定費)
    tax = int(income * 0.3) if income > 0 else 0
    
    total_cost = salary_cost + office_cost + tax
    st.session_state.money += (income - total_cost)
    st.session_state.month += 1
    st.session_state.last_time = time.time()
    
    st.session_state.logs.insert(0, f"【{st.session_state.month-1}月末決算】収益:{income}円 / 経費:{total_cost}円(人件費:{salary_cost}含む)")

# 20分経過していたら自動更新
if elapsed >= MONTH_DURATION:
    next_month()
    st.rerun()

# 4. 画面表示
st.title(f"🏢 会社経営シミュレーター ({st.session_state.month}ヶ月目)")
st.caption(f"次の月まであと: {remaining // 60}分 {remaining % 60}秒")
st.progress(1.0 - (remaining / MONTH_DURATION))

col1, col2, col3 = st.columns(3)
col1.metric("総資産", f"{st.session_state.money:,}円")
col2.metric("市場シェア", f"{st.session_state.share}%")
col3.metric("従業員数", f"{st.session_state.staff}名")

# 5. アクションボタン
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
            st.rerun()
with c3:
    if st.button("商品開発 (5,000円)"):
        if st.session_state.money >= 5000:
            st.session_state.money -= 5000
            st.session_state.share += random.randint(1, 10)
            st.rerun()

if st.button("⏩ 手動で月を進める（テスト用）"):
    next_month()
    st.rerun()

# 6. 履歴
st.subheader("経営履歴")
for log in st.session_state.logs[:5]:
    st.text(log)

# 画面を定期的に更新（10秒おきに再描画してタイマーを進める）
time.sleep(1)
st.rerun()
