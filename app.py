import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from datetime import datetime
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="TrendWatch",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
header1, header2 = st.columns([6,2])

with header1:

    st.markdown("""
    <div class="logo-box">
        <h1>📈 TrendWatch</h1>
        <p>Live News Trend & Sentiment Analytics</p>
    </div>
    """, unsafe_allow_html=True)

with header2:

    st.markdown(f"""
    <div class="update-box">
    <b>Last Updated</b><br>
    {datetime.now().strftime("%d %B %Y")}<br>
    {datetime.now().strftime("%I:%M %p")}
    </div>
    """, unsafe_allow_html=True)
    search = st.text_input(
    "",
    placeholder="🔍 Search news, topics or keywords..."
)
        with st.sidebar:
            st.title("📊 Dashboard")
            menu = st.radio(
                "",
                ["Dashboard","Trending Topics","News Search","Sentiment Analysis","Categories","Reports"]
            )

    st.markdown("---")

    st.info("""
### Data Source

**GDELT**

Global Database of Events,
Language & Tone
""")
    @st.cache_data
def load_data():

    if os.path.exists("data/news.csv"):
        return pd.read_csv("data/news.csv")

    return pd.DataFrame()

news = load_data()
if search:

    news = news[
        news.astype(str)
        .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
    ]
    if len(news)==0:

    st.warning("No news found.")

    st.stop()
    # ---------------- DATA PREPARATION ----------------

if "headline" in news.columns:
    news["headline"] = news["headline"].fillna("")

if "date" in news.columns:
    news["date"] = pd.to_datetime(news["date"], errors="coerce")

# Count today's mentions
today_mentions = len(news)

# Trending topic
top_topic = "AI"

if "topic" in news.columns and len(news) > 0:
    top_topic = news["topic"].mode()[0]

# Sentiment
if "sentiment" not in news.columns:

    def sentiment(text):
        score = TextBlob(str(text)).sentiment.polarity

        if score > 0.1:
            return "Positive"
        elif score < -0.1:
            return "Negative"
        else:
            return "Neutral"

    news["sentiment"] = news["headline"].apply(sentiment)

positive = (news["sentiment"] == "Positive").sum()
neutral = (news["sentiment"] == "Neutral").sum()
negative = (news["sentiment"] == "Negative").sum()
left, middle, right = st.columns([1.2,1.4,1.2])
with left:
    st.markdown(f"""
<div class="card">

<h5>TODAY'S TOP TRENDING TOPIC</h5>

<h1 style="color:#2D72D9;">
🤖 {top_topic}
</h1>

<p style="font-size:18px;">
Artificial Intelligence is dominating global discussions.
</p>

<hr>

<h5>MENTIONS TODAY</h5>

<h2 style="color:#2D72D9;">
{today_mentions:,}
</h2>

<h4 style="color:#28C76F;">
⬈ 78%
</h4>

</div>
""", unsafe_allow_html=True)
    with middle:
        st.markdown("### MENTIONS OVER TIME")

if "date" in news.columns:

    trend = (
        news.groupby(news["date"].dt.date)
        .size()
        .reset_index(name="mentions")
    )

    fig = px.line(
        trend,
        x="date",
        y="mentions",
        markers=True
    )

    fig.update_traces(
        line_color="#2D72D9",
        line_width=4
    )

    fig.update_layout(

        plot_bgcolor="white",

        paper_bgcolor="white",

        margin=dict(l=10,r=10,t=20,b=10),

        height=330
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    with right:
        st.markdown("### SENTIMENT OVERVIEW")

fig = go.Figure(
    data=[
        go.Pie(
            labels=["Positive","Neutral","Negative"],
            values=[positive,neutral,negative],
            hole=.70
        )
    ]
)

fig.update_traces(

    marker=dict(
        colors=[
            "#2D72D9",
            "#BFD7FF",
            "#DCEBFA"
        ]
    )
)

fig.update_layout(

    showlegend=False,

    height=330,

    margin=dict(
        l=10,
        r=10,
        t=20,
        b=10
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.metric("Positive",f"{positive}")

st.metric("Neutral",f"{neutral}")

st.metric("Negative",f"{negative}")
# ---------------- TRENDING CATEGORIES ----------------

st.markdown("## 🔥 Trending Categories")

category_icons = {
    "AI & Technology":"🤖",
    "Politics":"🏛️",
    "Business":"📈",
    "Health":"💙",
    "Sports":"⚽",
    "Entertainment":"🎬"
}

if "category" in news.columns:

    categories = (
        news["category"]
        .value_counts()
        .head(6)
    )

else:

    categories = pd.Series(
        [24596,18362,14827,12103,9845,8194],
        index=[
            "AI & Technology",
            "Politics",
            "Business",
            "Health",
            "Sports",
            "Entertainment"
        ]
    )

cols = st.columns(6)

for col, (cat, count) in zip(cols, categories.items()):

    icon = category_icons.get(cat, "📰")

    with col:

        st.markdown(f"""
        <div class="category-card">

        <h1>{icon}</h1>

        <h4>{cat}</h4>

        <h3>{count:,}</h3>

        <p style="color:#28C76F;">
        ▲ Trending
        </p>

        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

st.markdown("## 📰 Latest News Headlines")
display_news = news.head(8)

for _, row in display_news.iterrows():

    headline = row.get("headline","No Headline")
    source = row.get("source","Unknown")
    sentiment = row.get("sentiment","Neutral")
    url = row.get("url","#")

    if sentiment=="Positive":
        color="#28C76F"

    elif sentiment=="Negative":
        color="#EA5455"

    else:
        color="#FFB547"

    left,right = st.columns([6,1])

    with left:

        st.markdown(f"""
        <div class="news-card">

        <h4>{headline}</h4>

        <p>{source}</p>

        <span style="
        background:{color};
        color:white;
        padding:6px 12px;
        border-radius:20px;
        ">
        {sentiment}
        </span>

        </div>
        """, unsafe_allow_html=True)

    with right:

        st.link_button(
            "Read More",
            url
        )
        st.markdown("<br>",unsafe_allow_html=True)

if st.button("View All Headlines"):

    st.dataframe(news,use_container_width=True)
    st.markdown("---")

st.markdown("""
<center>

© 2026 TrendWatch

Live News Trend & Sentiment Analytics

Powered by GDELT

</center>
""",unsafe_allow_html=True)
