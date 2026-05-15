import streamlit as st
import random
import time
from datetime import datetime, timedelta

# 1. ページの設定
st.set_page_config(page_title="極限経営シミュレーター", layout="centered")

# 2. データの初期化
if 'money' not in st.session_state:
    st.session_state.money = 6000000    # 資本金をさらに減額(600万)
    st.session_state.debt = 0           
    st.session_state.staff = 1         
    st.session_state.share = 1
    st.session_state.start_date = datetime(2024, 1, 1) 
    st.session_state.last_time = time.time()
    st.session_state.logs = ["2024年1月1日：過酷な市場での経営が始まりました。"]

# 定数
MONTH_DURATION = 300 
DAY_DURATION = 10

# 3. 破産判定
if st.session_state.money < -10000000:
    st.error("💀 【破産】不渡りを出しました。ゲームオーバー。")
    if st.button("再挑戦"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    st.stop()

# 4. イベント発生システム (50%の確率で発生)
def trigger_event():
    if random.random() < 0.50:  # 2ヶ月に1回ペース
        event_type = random.choice(["BAD", "BAD", "GOOD"]) # 悪いイベントの方が起きやすい
        
        if event_type == "BAD":
            event_id = random.randint(1, 3)
            if event_id == 1:
                loss = int(st.session_state.money * 0.15) if st.session_state.money > 0 else 500000
                st.session_state.money -= loss
                st.session_state.logs.insert(0, f"🚨 【不況】景気悪化により {loss:,}円 の損失。")
            elif event_id == 2:
                st.session_state.share = max(0, st.session_state.share - 8)
                st.session_state.logs.insert(0, "🔥 【不祥事】SNSで炎上し、シェアが8%低下。")
            elif event_id == 3:
                if st.session_state.staff > 1:
                    st.session_state.staff -= 1
                    st.session_state.logs.insert(0, "🏃 【離職】過労により主要社員が退職しました。")
        
        elif event_type == "GOOD":
            profit = 2000000
            st.session_state.money += profit
            st.session_state.logs.insert(0, f"✨ 【バブル】臨時ボーナス {profit:,}円 を獲得！")

# 5. 決算処理
def process_settlement():
    s = st.session_state.staff
    # 生産性を少し厳しめに設定
    sales = int(s * 450000 * (1 + st.session_state.share / 100))
    interest = int(st.session_state.debt * 0.015) # 金利を1.5%にアップ
    costs = int(s * 450000) + 300000 + interest # 固定費増額
    
    profit = sales - costs
    if profit > 0: profit = int(profit * 0.60) # 税率40%へ増税
    
    st.session_state.money += profit
    st.session_state.start_date += timedelta(days=30)
    st.session_state.last_time = time.time()
    st.session_state.logs.insert(0, f"📊 {st.session_state.start_date.strftime('%Y年%m月')} 決算：利益 {profit:,}円")
    
    # イベント判定を走らせる
    trigger_event()

# 自動更新
elapsed = time.time() - st.session_state.last_time
if elapsed >= MONTH_DURATION:
    process_settlement()
    st.rerun()

# 6. UI
current_game_date = st.session_state.start_date + timedelta(days=int(elapsed // DAY_DURATION))
st.title("⚖️ 極限経営シミュレーター")

col_t1, col_t2 = st.columns(2)
col_t1.metric("📅 日付", current_game_date.strftime("%Y年%m月%d日"))
col_t2.metric("⏳ 決算まで", f"{int(MONTH_DURATION - elapsed)}秒")
st.progress(min(1.0, elapsed / MONTH_DURATION))

c1, c2, c3, c4 = st.columns(4)
c1.metric("現預金", f"{st.session_state.money:,}円")
c2.metric("借金", f"{st.session_state.debt:,}円")
c3.metric("シェア", f"{st.session_state.share}%")
c4.metric("従業員", f"{st.session_state.staff}名")

# 7. 戦略
st.subheader("🛠️ 経営戦略")
tab1, tab2, tab3, tab4 = st.tabs(["人事・広報", "銀行・財務", "M&A", "⏩ スキップ"])

with tab1:
    col_a, col_b = st.columns(2)
    if col_a.button("採用 (100万)"): # コスト増
        if st.session_state.money >= 1000000:
            st.session_state.money -= 1000000
            st.session_state.staff += 1
            st.rerun()
    if col_b.button("広告 (300万)"): # コスト増
        if st.session_state.money >= 3000000:
            st.session_state.money -= 3000000
            st.session_state.share += random.randint(2, 6)
            st.rerun()

with tab2:
    col_c, col_d = st.columns(2)
    if col_c.button("1,000万円 借入"):
        st.session_state.money += 10000000
        st.session_state.debt += 10000000
        st.rerun()
    if col_d.button("1,000万円 返済"):
        if st.session_state.money >= 10000000 and st.session_state.debt >= 10000000:
            st.session_state.money -= 10000000
            st.session_state.debt -= 10000000
            st.rerun()

with tab3:
    cost = 40000000
    if st.button(f"他社買収 ({cost//1000000}M円)"):
        if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.share += random.randint(10, 25)
            st.balloons()
            st.rerun()

with tab4:
    st.warning("スキップしても決算とイベント判定が行われます。")
    if st.button("翌月までスキップ実行"):
        process_settlement() # ここでイベント判定も呼ばれる
        st.rerun()

st.divider()
st.subheader("経営ログ")
for log in st.session_state.logs[:5]:
    st.write(log)

time.sleep(1)
st.rerun()
