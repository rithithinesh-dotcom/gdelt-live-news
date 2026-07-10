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
       
