import streamlit as st
import random
import time
from datetime import datetime, timedelta

# 1. ページの設定
st.set_page_config(page_title="本格経営シミュレーター(高速版)", layout="centered")

# 2. データの初期化
if 'money' not in st.session_state:
    st.session_state.money = 10000000 
    st.session_state.staff = 1         
    st.session_state.share = 1
    st.session_state.start_date = datetime(2024, 1, 1) 
    st.session_state.last_time = time.time()
    st.session_state.last_click_time = time.time()
    st.session_state.logs = ["2024年1月1日：高速経営スタート！"]
    st.session_state.is_banned = False

# ★ 時間設定を「5分」に変更 ★
MONTH_DURATION = 300  # 1ヶ月 = 300秒 (5分)
DAY_DURATION = MONTH_DURATION / 30  # 1日 = 10秒

# 3. 不正検知 (オートクリッカー対策)
def check_click_speed():
    current = time.time()
    if current - st.session_state.last_click_time < 0.1:
        st.session_state.is_banned = True
        return True
    st.session_state.last_click_time = current
    return False

if st.session_state.is_banned:
    st.error("🚨 【不正検知】高速クリックによりデータがリセットされました。")
    if st.button("再起動"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()
    st.stop()

# 4. 時間と日付の計算
elapsed_total = time.time() - st.session_state.last_time
days_passed = int(elapsed_total // DAY_DURATION)
current_game_date = st.session_state.start_date + timedelta(days=days_passed)

# 月更新チェック（5分経過）
if elapsed_total >= MONTH_DURATION:
    s = st.session_state.staff
    # 粗利計算 (1人あたり月60万ベース)
    sales = int(s * 600000 * (1 + st.session_state.share / 100))
    # リアルな経費 (給料30万+社保+オフィス代)
    costs = int(s * 400000) + 100000 
    profit = sales - costs
    if profit > 0: profit = int(profit * 0.7) # 法人税30%引き
    
    st.session_state.money += profit
    # 日付を1ヶ月分進める
    st.session_state.start_date += timedelta(days=30)
    st.session_state.last_time = time.time()
    st.session_state.logs.insert(0, f"【決算報告】{st.session_state.start_date.strftime('%Y年%m月')} 利益:{profit:,}円")
    st.rerun()

# 5. メイン画面表示
st.title("🚀 高速経営シミュレーター")

# 日付とカウントダウンの表示
remaining = int(MONTH_DURATION - elapsed_total)
col_time1, col_time2 = st.columns(2)
col_time1.metric("📅 現在の日付", current_game_date.strftime("%Y年%m月%d日"))
col_time2.metric("⏳ 次回決算まで", f"{remaining // 60}分 {remaining % 60}秒")

st.progress(elapsed_total / MONTH_DURATION)

# ステータス
col1, col2, col3 = st.columns(3)
col1.metric("現預金", f"{st.session_state.money:,}円")
col2.metric("市場シェア", f"{st.session_state.share}%")
col3.metric("従業員数", f"{st.session_state.staff}名")

# 6. アクション
st.subheader("経営判断")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("採用 (50万)"):
        if not check_click_speed() and st.session_state.money >= 500000:
            st.session_state.money -= 500000
            st.session_state.staff += 1
            st.rerun()
with c2:
    if st.button("広告 (100万)"):
        if not check_click_speed() and st.session_state.money >= 1000000:
            st.session_state.money -= 1000000
            st.session_state.share += random.randint(1, 3)
            st.rerun()
with c3:
    # デバッグ・テスト用：すぐに月を進める
    if st.button("次月へ進む"):
        st.session_state.last_time -= MONTH_DURATION
        st.rerun()

st.divider()
st.subheader("経営ログ")
for log in st.session_state.logs[:5]:
    st.write(log)

# 1秒ごとに更新
time.sleep(1)
st.rerun()
