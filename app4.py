import streamlit as st
import random
import time
from datetime import datetime, timedelta

# 1. ページの設定
st.set_page_config(page_title="国家規模経営シミュレーター", layout="centered")

# 2. データの初期化
if 'money' not in st.session_state:
    st.session_state.money = 6000000    
    st.session_state.debt = 0           
    st.session_state.staff = 1         
    st.session_state.share = 1
    st.session_state.has_building = False 
    st.session_state.ma_count = 0      # M&A成功回数
    st.session_state.start_date = datetime(2024, 1, 1) 
    st.session_state.last_time = time.time()
    st.session_state.logs = ["2024年1月1日：目指せ1兆円のM&A！伝説の経営が始まる。"]

# 定数
MONTH_DURATION = 300 
DAY_DURATION = 10
BUILDING_COST = 100000000    # 1億円
MA_COST = 1000000000000      # 1兆円

# 3. 破産判定
if st.session_state.money < -500000000000: # 5000億の赤字で倒産
    st.error("💀 【国家破綻】負債が限界を超えました。")
    if st.button("再挑戦"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    st.stop()

# 4. イベントシステム
def trigger_event():
    if random.random() < 0.50:
        event_pool = ["GOOD", "GOOD", "BAD", "BAD"]
        event_type = random.choice(event_pool)
        if event_type == "BAD":
            loss = int(st.session_state.money * 0.05) if st.session_state.money > 0 else 500000
            st.session_state.money -= loss
            st.session_state.logs.insert(0, f"🚨 【市場不況】資産が {loss:,}円 減少。")
        elif event_type == "GOOD":
            profit = 50000000 # 5000万
            st.session_state.money += profit
            st.session_state.logs.insert(0, f"✨ 【特需発生】臨時利益 {profit:,}円 獲得！")

# 5. 決算処理
def process_settlement():
    s = st.session_state.staff
    # M&A回数に応じて売上倍率を爆上げ (1回につき売上+50%)
    multiplier = 1 + (st.session_state.ma_count * 0.5)
    sales = int(s * 600000 * (1 + st.session_state.share / 100) * multiplier)
    
    interest = int(st.session_state.debt * 0.015) 
    rent_cost = 0 if st.session_state.has_building else 300000
    if st.session_state.has_building: st.session_state.share += 1
        
    costs = int(s * 450000) + rent_cost + interest 
    profit = sales - costs
    if profit > 0: profit = int(profit * 0.65)
    
    st.session_state.money += profit
    st.session_state.start_date += timedelta(days=30)
    st.session_state.last_time = time.time()
    st.session_state.logs.insert(0, f"📊 {st.session_state.start_date.strftime('%Y年%m月')} 決算：純利益 {profit:,}円")
    trigger_event()

# 自動更新
elapsed = time.time() - st.session_state.last_time
if elapsed >= MONTH_DURATION:
    process_settlement()
    st.rerun()

# 6. UI表示
st.title("🏛️ 国家規模経営シミュレーター")
if st.session_state.ma_count > 0:
    st.warning(f"💎 大規模M&A実施済み ({st.session_state.ma_count}社) : 売上倍率 x{1 + st.session_state.ma_count*0.5}")

col_t1, col_t2 = st.columns(2)
col_t1.metric("📅 日付", st.session_state.start_date.strftime("%Y年%m月%d日"))
col_t2.metric("⏳ 決算まで", f"{int(MONTH_DURATION - elapsed)}秒")

c1, c2, c3, c4 = st.columns(4)
c1.metric("現預金", f"{st.session_state.money/100000000:,.1f}億円")
c2.metric("借金", f"{st.session_state.debt/100000000:,.1f}億円")
c3.metric("シェア", f"{st.session_state.share}%")
c4.metric("従業員", f"{st.session_state.staff}名")

# 7. 戦略タブ
tab1, tab2, tab3, tab4, tab5 = st.tabs(["採用・広報", "巨大融資", "1兆円M&A", "施設投資", "⏩"])

with tab1:
    col_a, col_b = st.columns(2)
    if col_a.button("大量採用 (1,000万/10人)"):
        if st.session_state.money >= 10000000:
            st.session_state.money -= 10000000
            st.session_state.staff += 10
            st.rerun()
    if col_b.button("世界広告 (1億)"):
        if st.session_state.money >= 100000000:
            st.session_state.money -= 100000000
            st.session_state.share += random.randint(5, 15)
            st.rerun()

with tab2:
    col_c, col_d = st.columns(2)
    if col_c.button("100億円 借入"):
        st.session_state.money += 10000000000
        st.session_state.debt += 10000000000
        st.rerun()
    if col_d.button("100億円 返済"):
        if st.session_state.money >= 10000000000 and st.session_state.debt >= 10000000000:
            st.session_state.money -= 10000000000
            st.session_state.debt -= 10000000000
            st.rerun()

with tab3:
    st.header("🌐 グローバルM&A")
    st.write(f"費用: **1兆円** ({MA_COST:,}円)")
    st.write("恩恵: シェア+50% ＆ **永続的な売上倍率 +0.5倍**")
    if st.button("1兆円で競合を飲み込む"):
        if st.session_state.money >= MA_COST:
            st.session_state.money -= MA_COST
            st.session_state.share += 50
            st.session_state.ma_count += 1
            st.balloons()
            st.session_state.logs.insert(0, "🌍 【歴史的快挙】1兆円M&Aが成立しました！")
            st.rerun()
        else:
            st.warning("資金が全く足りません。")

with tab4:
    if st.button("自社ビル建設 (1億円)"):
        if not st.session_state.has_building and st.session_state.money >= BUILDING_COST:
            st.session_state.money -= BUILDING_COST
            st.session_state.has_building = True
            st.rerun()

with tab5:
    if st.button("⏩ 翌月までスキップ"):
        process_settlement()
        st.rerun()

st.divider()
st.subheader("ニュースログ")
for log in st.session_state.logs[:5]:
    st.write(log)

time.sleep(1)
st.rerun()
