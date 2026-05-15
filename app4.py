import streamlit as st
import random
import time
from datetime import datetime, timedelta

# 1. ページの設定
st.set_page_config(page_title="究極・経営シミュレーター", layout="centered")

# 2. データの初期化
if 'money' not in st.session_state:
    st.session_state.money = 8000000    
    st.session_state.debt = 0           # 借金
    st.session_state.staff = 1         
    st.session_state.share = 1
    st.session_state.start_date = datetime(2024, 1, 1) 
    st.session_state.last_time = time.time()
    st.session_state.last_click_time = time.time()
    st.session_state.logs = ["2024年1月1日：野望を抱き起業。借金はまだありません。"]
    st.session_state.is_banned = False

# 時間設定
MONTH_DURATION = 300 
DAY_DURATION = 10

# 3. 判定ロジック
if st.session_state.is_banned:
    st.error("🚨 【不正検知】リセットします。")
    if st.button("再起動"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    st.stop()

if st.session_state.money < -10000000: # 借金とは別に手元資金が-1000万で倒産
    st.error("💀 【破産】支払不能に陥りました。")
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
elapsed_total = time.time() - st.session_state.last_time
if elapsed_total >= MONTH_DURATION:
    s = st.session_state.staff
    # 決算計算
    sales = int(s * 500000 * (1 + st.session_state.share / 100))
    # 利息の計算 (年利12% = 月利1%と仮定)
    interest = int(st.session_state.debt * 0.01)
    costs = int(s * 450000) + 200000 + interest
    
    profit = sales - costs
    if profit > 0: profit = int(profit * 0.65)
    
    st.session_state.money += profit
    st.session_state.start_date += timedelta(days=30)
    st.session_state.last_time = time.time()
    
    msg = f"📊 {st.session_state.start_date.strftime('%Y年%m月')} 利益:{profit:,}円"
    if interest > 0: msg += f" (利息支払:{interest:,}円)"
    st.session_state.logs.insert(0, msg)
    
    # 5%の確率で買収提案イベント
    if random.random() < 0.05:
        st.session_state.logs.insert(0, "📢 【買収提案】競合他社からM&Aの打診が来ています！")
    st.rerun()

# 5. メイン画面表示
current_game_date = st.session_state.start_date + timedelta(days=int(elapsed_total // DAY_DURATION))
st.title("🏙️ 究極・経営シミュレーター")

# ステータス
col_t1, col_t2 = st.columns(2)
col_t1.metric("📅 日付", current_game_date.strftime("%Y年%m月%d日"))
col_t2.metric("⏳ 決算まで", f"{int(MONTH_DURATION - elapsed_total)}秒")

st.progress(elapsed_total / MONTH_DURATION)

c1, c2, c3, c4 = st.columns(4)
c1.metric("現預金", f"{st.session_state.money:,}円")
c2.metric("借金", f"{st.session_state.debt:,}円", delta_color="inverse")
c3.metric("シェア", f"{st.session_state.share}%")
c4.metric("従業員", f"{st.session_state.staff}名")

# 6. 戦略コマンド
st.subheader("🛠️ 経営戦略")
tab1, tab2, tab3 = st.tabs(["人事・広報", "銀行・財務", "M&A（買収）"])

with tab1:
    col_a, col_b = st.columns(2)
    if col_a.button("人材採用 (80万)"):
        if not check_click_speed() and st.session_state.money >= 800000:
            st.session_state.money -= 800000
            st.session_state.staff += 1
            st.rerun()
    if col_b.button("積極広告 (200万)"):
        if not check_click_speed() and st.session_state.money >= 2000000:
            st.session_state.money -= 2000000
            st.session_state.share += random.randint(2, 5)
            st.rerun()

with tab2:
    col_c, col_d = st.columns(2)
    if col_c.button("1,000万円 借り入れる"):
        if not check_click_speed():
            st.session_state.money += 10000000
            st.session_state.debt += 10000000
            st.session_state.logs.insert(0, "💰 銀行から1,000万円を調達しました(年利12%)。")
            st.rerun()
    if col_d.button("1,000万円 返済する"):
        if not check_click_speed() and st.session_state.money >= 10000000 and st.session_state.debt >= 10000000:
            st.session_state.money -= 10000000
            st.session_state.debt -= 10000000
            st.session_state.logs.insert(0, "✅ 借金を1,000万円返済しました。")
            st.rerun()

with tab3:
    st.write("他社を買収してシェアを一気に拡大します。")
    m_cost = 30000000 # 3000万
    if st.button(f"競合他社を買収する ({m_cost:,}円)"):
        if not check_click_speed() and st.session_state.money >= m_cost:
            st.session_state.money -= m_cost
            plus_share = random.randint(15, 30)
            st.session_state.share += plus_share
            st.session_state.logs.insert(0, f"🤝 M&A成立！シェアが{plus_share}%拡大しました！")
            st.balloons()
            st.rerun()
        else:
            st.warning("買収資金が足りません。")

st.divider()
st.subheader("ニュースログ")
for log in st.session_state.logs[:5]:
    st.write(log)

time.sleep(1)
st.rerun()
