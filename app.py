import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

# アプリのタイトル
st.title("📈 株価情報ビューア")

# 銘柄コード入力
code = st.text_input("銘柄コードを入力してください（例: 7203）", "7203")
period = st.selectbox("期間を選んでください", ["1mo", "3mo", "1y"])

if st.button("取得！"):
    ticker = code if ".T" in code else code + ".T"
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)

    if data.empty:
        st.error("データが見つかりませんでした")
    else:
        info = stock.get_info()
        st.subheader(info.get("longName", ticker))

        st.write(f"業種: {info.get('industry')}")
        st.write(f"PER: {info.get('trailingPE')}")
        st.write(f"時価総額: {info.get('marketCap'):,}")
        st.write(f"予想PER: {info.get('forwardPE')}")
        st.write(f"配当利回り: {info.get('dividendYield')*100:.2f} %")
        st.write(f"52週高値: {info.get('fiftyTwoWeekHigh')}")
        st.write(f"52週安値: {info.get('fiftyTwoWeekLow')}")

        # グラフ
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data["Close"], label="株価", color="blue")
        plt.title(f"{info.get('longName', '銘柄')} の株価推移", fontsize=14)
        plt.xlabel("日付", fontsize=12)
        plt.ylabel("株価（円）", fontsize=12)
        plt.grid(True)
        plt.tight_layout()

        st.pyplot(plt)
