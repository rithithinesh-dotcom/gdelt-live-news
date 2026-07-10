import streamlit as st
import pandas as pd
from datetime import datetime

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
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .trendwatch-title {
        color: #2D5D86;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #5F7890;
        font-size: 16px;
        margin-top: 2px;
        margin-bottom: 24px;
    }

    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #D6E6F2;
        border-radius: 14px;
        padding: 18px;
        min-height: 125px;
        box-shadow: 0 3px 10px rgba(80, 120, 150, 0.08);
    }

    .metric-label {
        color: #5F7890;
        font-size: 14px;
        font-weight: 500;
    }

    .metric-value {
        color: #2D5D86;
        font-size: 28px;
        font-weight: 700;
        margin-top: 8px;
    }

    .metric-note {
        color: #6D8EA8;
        font-size: 12px;
        margin-top: 6px;
    }

    .section-heading {
        color: #2D5D86;
        font-size: 22px;
        font-weight: 650;
        margin-top: 24px;
        margin-bottom: 10px;
    }

    .topic-card {
        background-color: #FFFFFF;
        border: 1px solid #D6E6F2;
        border-radius: 14px;
        padding: 18px;
        min-height: 320px;
    }

    .topic-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 11px 0;
        border-bottom: 1px solid #EAF2F8;
        color: #345B78;
        font-size: 15px;
    }

    .topic-pill {
        background-color: #D6E6F2;
        color: #2D5D86;
        padding: 4px 9px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .header-box {
        background-color: #8DB4D6;
        padding: 20px 24px;
        border-radius: 16px;
        margin-bottom: 20px;
    }

    .header-box h2 {
        color: #FFFFFF;
        margin: 0;
        font-size: 25px;
    }

    .header-box p {
        color: #F2F7FB;
        margin: 7px 0 0 0;
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

df = load_data()

# Header
st.markdown('<div class="trendwatch-title">TrendWatch</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Live News Trend & Sentiment Analytics Dashboard</div>',
    unsafe_allow_html=True
)

latest_update = df["collected_at"].max()
latest_update_text = (
    latest_update.strftime("%d %b %Y, %I:%M %p")
    if pd.notna(latest_update)
    else "Not available"
)

st.markdown(f"""
<div class="header-box">
    <h2>News Overview</h2>
    <p>Track live headlines, identify trending topics, and understand news sentiment.</p>
    <p><b>Last updated:</b> {latest_update_text}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Filter News")

countries = sorted(df["source_country"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries
)

search = st.sidebar.text_input("Search news headlines")

filtered_df = df[df["source_country"].isin(selected_countries)].copy()

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False)
    ]

# Sentiment category
def sentiment_label(tone):
    if pd.isna(tone):
        return "Neutral"
    if tone > 1:
        return "Positive"
    elif tone < -1:
        return "Negative"
    return "Neutral"

filtered_df["sentiment"] = filtered_df["tone"].apply(sentiment_label)

# KPI cards
total_articles = len(filtered_df)
total_sources = filtered_df["domain"].nunique()
average_tone = filtered_df["tone"].mean()

if len(filtered_df) > 0:
    top_country = filtered_df["source_country"].value_counts().index[0]
else:
    top_country = "No data"

if average_tone > 1:
    overall_sentiment = "Positive"
elif average_tone < -1:
    overall_sentiment = "Negative"
else:
    overall_sentiment = "Neutral"

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Articles Analysed</div>
        <div class="metric-value">{total_articles:,}</div>
        <div class="metric-note">Live GDELT news records</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Top News Country</div>
        <div class="metric-value">{top_country}</div>
        <div class="metric-note">Highest number of headlines</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Overall Sentiment</div>
        <div class="metric-value">{overall_sentiment}</div>
        <div class="metric-note">Average tone: {average_tone:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">News Sources</div>
        <div class="metric-value">{total_sources}</div>
        <div class="metric-note">Unique publishing domains</div>
    </div>
    """, unsafe_allow_html=True)

# Trend and topic area
left, right = st.columns([1.65, 1])

with left:
    st.markdown('<div class="section-heading">Daily News Trend</div>', unsafe_allow_html=True)

    trend_data = (
        filtered_df.dropna(subset=["published_date"])
        .groupby(filtered_df["published_date"].dt.date)
        .size()
    )

    if not trend_data.empty:
        st.area_chart(trend_data)
    else:
        st.info("No date data available for the selected filter.")

with right:
    st.markdown('<div class="section-heading">Trending Topics</div>', unsafe_allow_html=True)

    keywords = {
        "Artificial Intelligence": ["ai", "artificial intelligence", "chatgpt", "machine learning"],
        "Business & Economy": ["business", "market", "economy", "finance", "stock"],
        "Technology": ["technology", "tech", "software", "digital"],
        "Health": ["health", "medical", "hospital", "disease"],
        "Sports": ["sport", "cricket", "football", "match"],
        "Entertainment": ["movie", "film", "music", "celebrity"]
    }

    titles = filtered_df["title"].fillna("").str.lower()

    topic_counts = {}
    for topic, words in keywords.items():
        count = sum(titles.str.contains(word, regex=False).sum() for word in words)
        topic_counts[topic] = count

    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)

    topic_html = '<div class="topic-card">'
    for topic, count in sorted_topics[:6]:
        topic_html += f'''
        <div class="topic-row">
            <span>{topic}</span>
            <span class="topic-pill">{count} articles</span>
        </div>
        '''
    topic_html += "</div>"

    st.markdown(topic_html, unsafe_allow_html=True)

# Sentiment section
st.markdown('<div class="section-heading">Sentiment Analysis</div>', unsafe_allow_html=True)

sentiment_counts = filtered_df["sentiment"].value_counts()
s1, s2 = st.columns([1, 1.65])

with s1:
    st.bar_chart(sentiment_counts)

with s2:
    positive = sentiment_counts.get("Positive", 0)
    neutral = sentiment_counts.get("Neutral", 0)
    negative = sentiment_counts.get("Negative", 0)

    st.markdown(f"""
    <div class="topic-card">
        <div class="topic-row"><span>Positive Headlines</span><span class="topic-pill">{positive}</span></div>
        <div class="topic-row"><span>Neutral Headlines</span><span class="topic-pill">{neutral}</span></div>
        <div class="topic-row"><span>Negative Headlines</span><span class="topic-pill">{negative}</span></div>
        <br>
        <p style="color:#5F7890; font-size:14px;">
        Sentiment is calculated from the GDELT tone score. A score above 1 is positive,
        below -1 is negative, and values in between are neutral.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Latest headlines
st.markdown('<div class="section-heading">Latest Headline Insights</div>', unsafe_allow_html=True)

display_df = filtered_df.sort_values(
    "collected_at",
    ascending=False
)[["title", "source_country", "language", "published_date", "sentiment", "tone", "url"]]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="Download Filtered News Dataset",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="trendwatch_filtered_news.csv",
    mime="text/csv"
)
