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
    .stApp { background-color: #F5F7FB; }
    h1, h2, h3 { color: #15233D; }
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #15233D;
        margin-bottom: 0;
    }
    .subtitle {
        color: #667085;
        font-size: 16px;
        margin-top: 0;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 10px rgba(21,35,61,0.08);
    }
    .top-topic {
        background: linear-gradient(135deg, #15233D, #3169E8);
        color: white;
        border-radius: 16px;
        padding: 20px;
        margin: 14px 0 20px 0;
    }
    .top-topic h3 { color: white; margin: 0; }
    .top-topic p { color: #DDE8FF; margin-bottom: 0; }
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
    if tone > 1:
        return "Positive"
    elif tone < -1:
        return "Negative"
    return "Neutral"

def extract_topic(title):
    if pd.isna(title):
        return "Other"

    words = re.findall(r"\b[a-zA-Z]{4,}\b", title.lower())

    stop_words = {
        "this", "that", "with", "from", "have", "will", "news",
        "about", "after", "their", "they", "were", "been", "into",
        "more", "than", "over", "says", "said", "what", "when",
        "where", "which", "today", "latest", "could", "should"
    }

    useful_words = [word for word in words if word not in stop_words]

    if useful_words:
        return useful_words[0].title()

    return "Other"

df = load_data()
df["sentiment"] = df["tone"].apply(get_sentiment)
df["topic"] = df["title"].apply(extract_topic)

st.markdown('<p class="main-title">📰 TrendWatch</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Live News Trend & Sentiment Analytics Dashboard powered by GDELT</p>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Filter News")

    search = st.text_input("Search headlines")

    countries = sorted(df["source_country"].dropna().unique())
    selected_countries = st.multiselect(
        "Countries",
        countries,
        default=countries
    )

    languages = sorted(df["language"].dropna().unique())
    selected_languages = st.multiselect(
        "Languages",
        languages,
        default=languages
    )

    if st.button("Refresh Dashboard"):
        st.cache_data.clear()
        st.rerun()

filtered_df = df[
    (df["source_country"].isin(selected_countries)) &
    (df["language"].isin(selected_languages))
].copy()

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False)
    ]

topic_counts = filtered_df["topic"].value_counts()
top_topic = topic_counts.index[0] if not topic_counts.empty else "No data"
top_topic_count = topic_counts.iloc[0] if not topic_counts.empty else 0

sentiment_counts = filtered_df["sentiment"].value_counts()
overall_sentiment = (
    sentiment_counts.index[0] if not sentiment_counts.empty else "No data"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Articles Analyzed", f"{len(filtered_df):,}")
col2.metric("Top Trending Topic", top_topic)
col3.metric("Overall Sentiment", overall_sentiment)
col4.metric("News Sources", filtered_df["domain"].nunique())

st.markdown(
    f"""
    <div class="top-topic">
        <h3>🔥 Currently Trending: {top_topic}</h3>
        <p>{top_topic_count:,} related headlines found in the live dataset.</p>
    </div>
    """,
    unsafe_allow_html=True
)

left, right = st.columns([1.5, 1])

with left:
    st.subheader("News Trend Over Time")

    trend_df = (
        filtered_df.dropna(subset=["published_date"])
        .groupby(filtered_df["published_date"].dt.date)
        .size()
    )

    st.line_chart(trend_df)

with right:
    st.subheader("Top Trending Topics")
    st.bar_chart(topic_counts.head(8))

left2, right2 = st.columns(2)

with left2:
    st.subheader("Sentiment Analysis")
    st.bar_chart(sentiment_counts)

with right2:
    st.subheader("Top News Countries")
    st.bar_chart(filtered_df["source_country"].value_counts().head(8))

st.subheader("Latest Headline Insights")

latest_news = filtered_df.sort_values(
    "collected_at",
    ascending=False
)[
    [
        "title",
        "topic",
        "sentiment",
        "source_country",
        "language",
        "published_date",
        "tone",
        "url"
    ]
]

st.dataframe(latest_news, use_container_width=True, height=420)

st.download_button(
    "Download Filtered Dataset",
    filtered_df.to_csv(index=False).encode("utf-8"),
    "trendwatch_filtered_news.csv",
    "text/csv"
)
