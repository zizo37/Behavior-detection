import json
import re
import os
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import emoji

# Download required NLTK data (run once)
nltk.download('vader_lexicon')

def load_json_data(file_path):
    """Load data from a JSON file"""
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def clean_text(text):
    """Clean and preprocess text"""
    if not isinstance(text, str):
        return ""
    

    text = emoji.demojize(text)
    
    
    text = re.sub(r'http\S+|www.\S+', '', text)
    

    text = re.sub(r'@\w+', '', text)
    

    text = ' '.join(text.split())
    
    return text.strip()

def analyze_sentiment_nltk(text):
    """
    Analyze sentiment using NLTK's VADER
    Returns sentiment scores and classification
    """
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    
    # Determine if supportive based on compound score
    is_supportive = scores['compound'] > 0.2
    
    return {
        'is_supportive': is_supportive,
        'compound_score': scores['compound'],
        'pos_score': scores['pos'],
        'neg_score': scores['neg'],
        'neu_score': scores['neu']
    }

def process_comments(file_path):
    """Process all comments in a JSON file"""
    data = load_json_data(file_path)
    analyzed_comments = []
    
    for comment in data:
        author = comment.get('author', 'Unknown')
        text = comment.get('text', '')
        timestamp = comment.get('timestamp', 'Unknown')
        
        cleaned_text = clean_text(text)
        sentiment_analysis = analyze_sentiment_nltk(cleaned_text)
        
        analyzed_comment = {
            'author': author,
            'original_text': text,
            'cleaned_text': cleaned_text,
            'timestamp': timestamp,
            'supportive': sentiment_analysis['is_supportive'],
            'sentiment_scores': {
                'compound': sentiment_analysis['compound_score'],
                'positive': sentiment_analysis['pos_score'],
                'negative': sentiment_analysis['neg_score'],
                'neutral': sentiment_analysis['neu_score']
            }
        }
        analyzed_comments.append(analyzed_comment)
    
    return analyzed_comments

def save_cleaned_data(cleaned_comments, output_file):
    """Save cleaned comments to a new JSON file"""
    try:
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(cleaned_comments, file, indent=4, ensure_ascii=False)
        print(f"Cleaned data saved to: {output_file}")
    except Exception as e:
        print(f"Error saving cleaned data: {e}")

def main():
    files = [
        'json/comments_data_of_post_1.json',
        'json/comments_data_of_post_2.json'
    ]
    
    all_analyzed_comments = []
    for file_path in files:
        print(f"\nProcessing {file_path}:")
        analyzed_comments = process_comments(file_path)
        all_analyzed_comments.extend(analyzed_comments)
        
        # Print example of analysis
        for comment in analyzed_comments[:2]:
            print("\nOriginal:", comment['original_text'])
            print("Cleaned:", comment['cleaned_text'])
            print("Supportive:", comment['supportive'])
            print("Sentiment Scores:", comment['sentiment_scores'])
    
    output_file = 'output1/analyzed_comments_nltk2.json'
    save_cleaned_data(all_analyzed_comments, output_file)
    
    print(f"\nTotal comments processed: {len(all_analyzed_comments)}")

if __name__ == "__main__":
    main()