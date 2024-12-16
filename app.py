import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from main1 import process_comments

def load_analyzed_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def create_sentiment_distribution_chart(stats):
    categories = []
    counts = []
    percentages = []
    
    for category, data in stats['category_distribution'].items():
        categories.append(category)
        counts.append(data['count'])
        percentages.append(data['percentage'])
    
    fig = go.Figure(data=[
        go.Bar(name='Count', x=categories, y=counts),
    ])
    
    fig.update_layout(
        title='Sentiment Distribution',
        xaxis_title='Sentiment Category',
        yaxis_title='Number of Comments'
    )
    
    return fig

def create_sentiment_timeline(comments):
    df = pd.DataFrame(comments)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    fig = px.line(df, x='timestamp', y='sentiment_scores.compound',
                  title='Sentiment Timeline',
                  labels={'sentiment_scores.compound': 'Compound Sentiment Score'})
    return fig

def main():
    st.title("Comment Sentiment Analysis Dashboard")
    
    # Sidebar for file upload and controls
    st.sidebar.header("Controls")
    uploaded_file = st.sidebar.file_uploader("Upload JSON file", type=['json'])
    
    if uploaded_file:
        data = json.load(uploaded_file)
    else:
        # Load default data
        data = load_analyzed_data('output1/analyzed_comments_nltk.json')
    
    if data:
        st.header("Overall Statistics")
        stats = data.get('statistics', calculate_sentiment_stats(data.get('analyzed_comments', [])))
        
        # Display key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Comments", stats['total_comments'])
        with col2:
            st.metric("Average Sentiment", f"{stats['average_compound_score']:.2f}")
        with col3:
            positive_percentage = stats['category_distribution']['positive']['percentage'] + \
                                stats['category_distribution']['strong_positive']['percentage']
            st.metric("Positive Comments", f"{positive_percentage:.1f}%")
        
        # Sentiment Distribution Chart
        st.subheader("Sentiment Distribution")
        dist_chart = create_sentiment_distribution_chart(stats)
        st.plotly_chart(dist_chart)
        
        # Sentiment Timeline
        st.subheader("Sentiment Timeline")
        timeline_chart = create_sentiment_timeline(data.get('analyzed_comments', []))
        st.plotly_chart(timeline_chart)
        
        # Comment Browser
        st.header("Comment Browser")
        sentiment_filter = st.selectbox(
            "Filter by sentiment",
            ['All', 'strong_positive', 'positive', 'neutral', 'negative', 'strong_negative']
        )
        
        comments = data.get('analyzed_comments', [])
        if sentiment_filter != 'All':
            comments = [c for c in comments if c.get('sentiment_category') == sentiment_filter]
        
        for comment in comments:
            with st.expander(f"Comment by {comment['author']} ({comment['sentiment_category']})"):
                st.write("Original Text:", comment['original_text'])
                st.write("Cleaned Text:", comment['cleaned_text'])
                st.write("Sentiment Scores:", comment['sentiment_scores'])

if __name__ == "__main__":
    main()
