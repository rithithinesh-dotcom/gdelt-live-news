import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="TrendWatch",
    page_icon="📰",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/rithithinesh-dotcom/gdelt-live-news/main/gdelt_live_news.csv"

st.markdown("""
<style>
    .stApp {
        background-color: #F2F7FB;
        color: #8DB4D6;
    }

    header[data-testid="stHeader"] {
        background-color: #F2F7FB;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .main-title {
        font-size: 52px;
        font-weight: 800;
        color: #8DB4D6;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }

    .subtitle {
        color: #8DB4D6;
        font-size: 18px;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    .section-title {
        color: #8DB4D6;
        font-size: 25px;
        font-weight: 700;
        margin-top: 20px;
    }

    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #D6E6F2;
        border-radius: 16px;
        padding: 18px;
        min-height: 130px;
    }

    .metric-label {
        color: #8DB4D6;
        font-size: 15px;
        font-weight: 600;
    }

    .metric-value {
        color: #8DB4D6;
        font-size: 34px;
        font-weight: 800;
        margin-top: 8px;
    }

    .metric-note {
        color: #8DB4D6;
        font-size: 13px;
        margin-top: 8px;
    }

    .trend-card {
        background-color: #FFFFFF;
        border: 1px solid #D6E6F2;
        border-radius: 16px;
        padding: 20px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #D6E6F2;
        border-radius: 12px;
        overflow: hidden;
    }

    .stTextInput input {
        background-color: #FFFFFF;
        border: 1px solid #8DB4D6;
        color: #8DB4D6;
        border-radius: 10px;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border-color: #8DB4D6;
        color: #8DB4D6;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(DATA_URL)

    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce")
    df["tone"] = pd.to_numeric(df["tone"], errors="coerce")

    return df


def get_sentiment(tone):
    if pd.isna(tone):
        return "Neutral"
    elif tone > 1:
        return "Positive"
    elif tone < -1:
        return "Negative"
    return "Neutral"


def extract_topic(title):
    if pd.isna(title):
        return "Other"

    title = title.lower()

    topic_words = {
        "Artificial Intelligence": ["ai", "artificial intelligence", "chatgpt", "openai", "robot"],
        "Technology": ["technology", "tech", "software", "cyber", "digital"],
        "Business & Economy": ["business", "market", "economy", "stock", "finance"],
        "Health": ["health", "hospital", "medical", "disease", "doctor"],
        "Sports": ["sport", "cricket", "football", "match", "player"],
        "Entertainment": ["movie", "film", "music", "celebrity", "actor"]
    }

    for topic, words in topic_words.items():
        if any(re.search(r"\b" + re.escape(word) + r"\b", title) for word in words):
            return topic

    return "General News"


df = load_data()
df["sentiment"] = df["tone"].apply(get_sentiment)
df["topic"] = df["title"].apply(extract_topic)

st.markdown('<div class="main-title">TrendWatch</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Live News Trend and Sentiment Analytics Dashboard</div>',
    unsafe_allow_html=True
)

search = st.text_input("🔎 Search news headlines")

country_options = ["All Countries"] + sorted(df["source_country"].dropna().unique().tolist())
selected_country = st.selectbox("Filter by country", country_options)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False)
    ]

if selected_country != "All Countries":
    filtered_df = filtered_df[
        filtered_df["source_country"] == selected_country
    ]

total_articles = len(filtered_df)
top_topic = (
    filtered_df["topic"].value_counts().index[0]
    if not filtered_df.empty else "No data"
)
avg_tone = filtered_df["tone"].mean()

if pd.isna(avg_tone):
    overall_sentiment = "Neutral"
elif avg_tone > 1:
    overall_sentiment = "Positive"
elif avg_tone < -1:
    overall_sentiment = "Negative"
else:
    overall_sentiment = "Neutral"

news_sources = filtered_df["domain"].nunique()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Articles Analysed</div>
        <div class="metric-value">{total_articles}</div>
        <div class="metric-note">Live articles in your dataset</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Top Trending Topic</div>
        <div class="metric-value">{top_topic}</div>
        <div class="metric-note">Most mentioned category</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Overall Sentiment</div>
        <div class="metric-value">{overall_sentiment}</div>
        <div class="metric-note">Average tone: {avg_tone:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">News Sources</div>
        <div class="metric-value">{news_sources}</div>
        <div class="metric-note">Different news domains</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">News Trend Overview</div>', unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.markdown('<div class="trend-card">', unsafe_allow_html=True)
    st.subheader("Articles Collected Over Time")

    trend_df = (
        filtered_df.dropna(subset=["published_date"])
        .groupby(filtered_df["published_date"].dt.date)
        .size()
    )

    st.line_chart(trend_df, color="#8DB4D6")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="trend-card">', unsafe_allow_html=True)
    st.subheader("Trending Topics")

    topic_counts = filtered_df["topic"].value_counts().head(6)

    if not topic_counts.empty:
        st.bar_chart(topic_counts, color="#8DB4D6")
    else:
        st.info("No topic data available.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Sentiment Analysis</div>', unsafe_allow_html=True)

sentiment_counts = (
    filtered_df["sentiment"]
    .value_counts()
    .reindex(["Positive", "Neutral", "Negative"], fill_value=0)
)

s1, s2 = st.columns(2)

with s1:
    st.markdown('<div class="trend-card">', unsafe_allow_html=True)
    st.subheader("Sentiment Distribution")
    st.bar_chart(sentiment_counts, color="#8DB4D6")
    st.markdown('</div>', unsafe_allow_html=True)

with s2:
    st.markdown('<div class="trend-card">', unsafe_allow_html=True)
    st.subheader("Top News Countries")
    country_counts = filtered_df["source_country"].value_counts().head(8)
    st.bar_chart(country_counts, color="#8DB4D6")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Latest News Headlines</div>', unsafe_allow_html=True)

latest_news = filtered_df.sort_values(
    "collected_at",
    ascending=False
)[
    ["title", "topic", "sentiment", "source_country",
     "published_date", "tone", "url"]
]

st.dataframe(
    latest_news,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Filtered News Dataset",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="trendwatch_filtered_news.csv",
    mime="text/csv"
)
