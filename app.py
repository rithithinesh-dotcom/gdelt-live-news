import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="TrendWatch | Live News Analytics",
    page_icon="📈",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/rithithinesh-dotcom/gdelt-live-news/main/gdelt_live_news.csv"

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
    if tone < -1:
        return "Negative"
    return "Neutral"

def extract_keywords(titles):
    stop_words = {
        "the", "and", "for", "with", "from", "that", "this", "are", "was",
        "will", "has", "have", "into", "about", "after", "over", "news",
        "says", "new", "its", "their", "how", "why", "who", "what", "in",
        "on", "at", "to", "of", "a", "an", "is", "as", "by"
    }

    words = []
    for title in titles.dropna():
        found_words = re.findall(r"\b[a-zA-Z]{4,}\b", str(title).lower())
        words.extend([word for word in found_words if word not in stop_words])

    return pd.Series(words).value_counts().head(8)

df = load_data()
df["sentiment"] = df["tone"].apply(get_sentiment)

st.markdown("""
<style>
    .main {
        background-color: #f5f7fb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .title-text {
        font-size: 2.2rem;
        font-weight: 800;
        color: #15233d;
        margin-bottom: 0;
    }
    .subtitle-text {
        color: #667085;
        font-size: 1rem;
        margin-top: 0;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 10px rgba(23, 32, 51, 0.08);
    }
    h2, h3 {
        color: #15233d;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">📈 TrendWatch</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle-text">Live News Trend & Sentiment Analytics Dashboard</p>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Dashboard Filters")

    countries = sorted(df["source_country"].dropna().unique())
    selected_countries = st.multiselect(
        "Country",
        countries,
        default=countries
    )

    languages = sorted(df["language"].dropna().unique())
    selected_languages = st.multiselect(
        "Language",
        languages,
        default=languages
    )

    sentiment_options = ["Positive", "Neutral", "Negative"]
    selected_sentiments = st.multiselect(
        "Sentiment",
        sentiment_options,
        default=sentiment_options
    )

    search_text = st.text_input("Search news headlines")

filtered_df = df[
    (df["source_country"].isin(selected_countries)) &
    (df["language"].isin(selected_languages)) &
    (df["sentiment"].isin(selected_sentiments))
].copy()

if search_text:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_text, case=False, na=False)
    ]

top_keywords = extract_keywords(filtered_df["title"])
top_topic = top_keywords.index[0].title() if not top_keywords.empty else "No data"

positive_percentage = 0
if len(filtered_df) > 0:
    positive_percentage = round(
        (filtered_df["sentiment"] == "Positive").mean() * 100
    )

overall_sentiment = "Neutral"
if positive_percentage > 50:
    overall_sentiment = "Positive"
elif (filtered_df["sentiment"] == "Negative").mean() > 0.4:
    overall_sentiment = "Negative"

c1, c2, c3, c4 = st.columns(4)

c1.metric("Articles Analyzed", f"{len(filtered_df):,}")
c2.metric("Top Trending Topic", top_topic)
c3.metric("Overall Sentiment", overall_sentiment)
c4.metric("News Sources", filtered_df["domain"].nunique())

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("📊 News Trend Over Time")

    trend_df = filtered_df.dropna(subset=["published_date"]).copy()
    trend_df["date"] = trend_df["published_date"].dt.date
    daily_articles = trend_df.groupby("date").size()

    if not daily_articles.empty:
        st.line_chart(daily_articles)
    else:
        st.info("No date-based trend data is available yet.")

with right:
    st.subheader("🔥 Top Trending Topics")

    if not top_keywords.empty:
        trending_table = pd.DataFrame({
            "Topic": top_keywords.index.str.title(),
            "Mentions": top_keywords.values
        })
        st.dataframe(
            trending_table,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No trending topics found.")

left2, right2 = st.columns(2)

with left2:
    st.subheader("😊 Sentiment Analysis")

    sentiment_counts = filtered_df["sentiment"].value_counts()
    if not sentiment_counts.empty:
        st.bar_chart(sentiment_counts)
    else:
        st.info("No sentiment data available.")

with right2:
    st.subheader("🌍 Top News Countries")

    country_counts = filtered_df["source_country"].value_counts().head(10)
    if not country_counts.empty:
        st.bar_chart(country_counts)
    else:
        st.info("No country data available.")

st.divider()

st.subheader("📰 Latest Headline Insights")

latest_news = filtered_df.sort_values(
    "collected_at",
    ascending=False
)[["title", "source_country", "language", "published_date", "sentiment", "tone", "url"]]

st.dataframe(latest_news, use_container_width=True, hide_index=True)

st.download_button(
    "Download Filtered News Dataset",
    filtered_df.to_csv(index=False).encode("utf-8"),
    "trendwatch_filtered_news.csv",
    "text/csv"
)
