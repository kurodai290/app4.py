import streamlit as st
import random
import time

# 1. ページの設定
st.set_page_config(page_title="本格経営シミュレーター", layout="centered")

# 2. データの初期化
if 'money' not in st.session_state:
    st.session_state.money = 10000000 
    st.session_state.staff = 1         
    st.session_state.share = 1
    st.session_state.month = 1
    st.session_state.last_time = time.time()
    st.session_state.last_click_time = time.time() # クリック監視用
    st.session_state.logs = ["会社を設立しました！"]
    st.session_state.is_banned = False # バン状態

# 3. オートクリッカー検知ロジック
def check_click_speed():
    current = time.time()
    interval = current - st.session_state.last_click_time
    st.session_state.last_click_time = current
    
    # 0.1秒以下の間隔でクリックされたら不正とみなす
    if interval < 0.1:
        st.session_state.is_banned = True
        return True
    return False

# 不正検知時のリセット画面
if st.session_state.is_banned:
    st.error("🚨 【不正検知】オートクリッカーの使用が疑われました。")
    st.warning("公平なプレイを保つため、全データをリセットしました。")
    if st.button("反省して再スタートする"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
    st.stop() # ここで処理を止める

# --- (以下、前回の月更新ロジックなどはそのまま継続) ---

def next_month():
    s = st.session_state.staff
    base_unit = 500000 if s <= 10 else 800000
    total_sales = int(s * base_unit * (1 + st.session_state.share / 100))
    personnel_expenses = int(s * 300000 * 1.15)
    rent_office = int(s * 30000) + 100000
    profit = total_sales - (personnel_expenses + rent_office)
    if profit > 0: profit -= int(profit * 0.3)
    st.session_state.money += profit
    st.session_state.month += 1
    st.session_state.last_time = time.time()
    st.session_state.logs.insert(0, f"【{st.session_state.month-1}月決算】純利益:{profit:,}円")

elapsed = time.time() - st.session_state.last_time
if elapsed >= 1200:
    next_month()
    st.rerun()

# 4. 画面表示
st.title(f"🏢 経営シミュレーター ({st.session_state.month}ヶ月目)")
col1, col2, col3 = st.columns(3)
col1.metric("現預金", f"{st.session_state.money:,}円")
col2.metric("市場シェア", f"{st.session_state.share}%")
col3.metric("従業員数", f"{st.session_state.staff}名")

# 5. アクション（クリック時にスピードチェックを入れる）
st.subheader("経営判断")
c1, c2 = st.columns(2)

with c1:
    if st.button("採用を出す (50万)"):
        if check_click_speed(): st.rerun() # 検知
        if st.session_state.money >= 500000:
            st.session_state.money -= 500000
            st.session_state.staff += 1
            st.rerun()

with c2:
    if st.button("マーケティング (100万)"):
        if check_click_speed(): st.rerun() # 検知
        if st.session_state.money >= 1000000:
            st.session_state.money -= 1000000
            st.session_state.share += random.randint(1, 3)
            st.rerun()

st.divider()
st.subheader("月次報告ログ")
for log in st.session_state.logs[:5]:
    st.write(log)

time.sleep(1)
st.rerun()
