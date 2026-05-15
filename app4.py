# --- 隠しコマンド入力セクション ---
st.divider()
with st.expander("🛠️ 管理用デバッグコンソール"):
    cheat_code = st.text_input("アクセスコードを入力", type="password")
    
    # 新機能1：10万円手に入れる
    if cheat_code == "give me money":
        if st.button("10万円を受け取る"):
            st.session_state.money += 100000
            st.session_state.logs.insert(0, "㊙️ 臨時収入：10万円を手に入れました。")
            st.rerun()

    # 新機能2：翌月にスキップ
    elif cheat_code == "skip":
        if st.button("翌月へスキップ"):
            # 時間を強制的に進めて決算処理を走らせる
            st.session_state.last_time -= MONTH_DURATION
            st.session_state.logs.insert(0, "㊙️ 時を飛ばして翌月へ向かいます。")
            st.rerun()

    # (以前のコードも残す場合)
    elif cheat_code == "money money":
        if st.button("資金注入 (1億円)"):
            st.session_state.money += 100000000
            st.session_state.logs.insert(0, "㊙️ 1億円獲得。")
            st.rerun()
