import streamlit as st
import random
import time
from datetime import datetime, timedelta

# 1. ページの設定（必ず最初に書く）
st.set_page_config(page_title="究極・経営シミュレーター", layout="centered")

# 2. データの初期化
if 'money' not in st.session_state:
    st.session_state.money = 8000000    
    st.session_state.debt = 0           
    st.session_state.staff = 1         
    st.session_state.share = 1
    st.session_state.start_date = datetime(2024, 1, 1) 
    st.session_state.last_time = time.time()
    st.session_state.last_click_time = time.time()
    st.session_state.logs = ["2024年1月1日：株式会社を設立しました！"]
    st.session_state.is_banned = False

# 定数設定
MONTH_DURATION = 300  # 1ヶ月 = 5分
DAY_DURATION = 10     # 1日 = 10秒

# 3. 不正検知・ゲームオーバー判定
if st.session_state.is_banned:
    st.error("🚨 【不正検知】オートクリッカー使用の疑いによりデータがリセットされました。")
    if st.button("再起動"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    st.stop()

if st.session_state.money < -10000000:
    st.error("💀 【破産】不渡りを出しました。ゲームオーバー。")
    if st.button("再挑戦"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    st.stop()

def check_click_speed():
    current = time.time()
    if current - st.session_state.last_click_time < 0.1:
        st.session_state.is_banned = True
        return True
    st.session_state.last_click_time = current
    return False

# 4. 月更新・決算処理
def process_settlement():
    s = st.session_state.staff
    sales = int(s * 550000 * (1 + st.session_state.share / 100))
    interest = int(st.session_state.debt * 0.01)
    costs = int(s * 450000) + 200000 + interest
    profit = sales - costs
    if profit > 0: profit = int(profit * 0.65) # 税引後
    
    st.session_state.money += profit
    st.session_state.start_date += timedelta(days=30)
    st.session_state.last_time = time.time()
    st.session_state.logs.insert(0, f"📊 {st.session_state.start_date.strftime('%Y年%m月')} 決算報告：純利益 {profit:,}円")

elapsed = time.time() - st.session_state.last_time
if elapsed >= MONTH_DURATION:
    process_settlement()
    st.rerun()

# 5. メイン画面表示
current_game_date = st.session_state.start_date + timedelta(days=int(elapsed // DAY_DURATION))
st.title("🏙️ 究極・経営シミュレーター")

col_t1, col_t2 = st.columns(2)
col_t1.metric("📅 日付", current_game_date.strftime("%Y年%m月%d日"))
col_t2.metric("⏳ 決算まで", f"{int(MONTH_DURATION - elapsed)}秒")
st.progress(min(1.0, elapsed / MONTH_DURATION))

c1, c2, c3, c4 = st.columns(4)
c1.metric("現預金", f"{st.session_state.money:,}円")
c2.metric("借金", f"{st.session_state.debt:,}円")
c3.metric("シェア", f"{st.session_state.share}%")
c4.metric("従業員", f"{st.session_state.staff}名")

# 6. 戦略コマンド
st.subheader("🛠️ 経営戦略")
tab1, tab2, tab3 = st.tabs(["人事・広報", "銀行・財務", "M&A（買収）"])

with tab1:
    col_a, col_b = st.columns(2)
    if col_a.button("採用 (80万)"):
        if not check_click_speed() and st.session_state.money >= 800000:
            st.session_state.money -= 800000
            st.session_state.staff += 1
            st.rerun()
    if col_b.button("広告 (200万)"):
        if not check_click_speed() and st.session_state.money >= 2000000:
            st.session_state.money -= 2000000
            st.session_state.share += random.randint(2, 5)
            st.rerun()

with tab2:
    col_c, col_d = st.columns(2)
    if col_c.button("1,000万円 借入"):
        if not check_click_speed():
            st.session_state.money += 10000000
            st.session_state.debt += 10000000
            st.rerun()
    if col_d.button("1,000万円 返済"):
        if not check_click_speed() and st.session_state.money >= 10000000 and st.session_state.debt >= 10000000:
            st.session_state.money -= 10000000
            st.session_state.debt -= 10000000
            st.rerun()

with tab3:
    if st.button("他社を買収 (3,000万)"):
        if not check_click_speed() and st.session_state.money >= 30000000:
            st.session_state.money -= 30000000
            st.session_state.share += random.randint(15, 30)
            st.balloons()
            st.rerun()

# 7. 隠しコマンド
st.divider()
with st.expander("🛠️ 管理用デバッグコンソール"):
    cheat = st.text_input("コードを入力", type="password")
    if cheat == "give me money":
        if st.button("10万円入手"):
            st.session_state.money += 100000
            st.rerun()
    elif cheat == "skip":
        if st.button("翌月へスキップ"):
            process_settlement()
            st.rerun()

st.subheader("ニュースログ")
for log in st.session_state.logs[:5]:
    st.write(log)

time.sleep(1)
st.rerun()
