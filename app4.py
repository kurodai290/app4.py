# ターン終了（収益発生）のロジック
if st.button("☕ ターンを終了して収益を得る"):
    s = st.session_state.staff  # 現在の社員数
    base_income = 0

    # 社員数に応じた収益計算
    if 1 <= s <= 10:
        base_income = 100
    elif 11 <= s <= 50:
        base_income = 1000
    elif 51 <= s <= 100:
        base_income = 10000
    elif s > 100:
        base_income = s * 100  # 101人目からは1人100円
    
    # シェアによるボーナス倍率を適用
    income = int(base_income * (1 + st.session_state.share / 100))
    
    # 税金計算（30%）
    tax = int(income * 0.3) if income > 0 else 0
    profit = income - tax
    
    # 資産に反映
    st.session_state.money += profit
    
    # ログに記録
    st.session_state.logs.insert(0, f"期末決算：収益{income}円（内、税金{tax}円）を獲得！")
    st.rerun()
