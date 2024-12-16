import json
import re
import os
import emoji

# Define adjustable weights
WEIGHTS = {
    'emoji_supportive': 0.5,
    'emoji_aggressive': 0.5,
    'punctuation': 0.5,
    'uppercase': 0.5,
}

# Keywords
SUPPORTIVE_KEYWORDS = [
    'great', 'amazing', 'love', 'fantastic', 'well done', 'awesome', 'excellent',
    'wonderful', 'outstanding', 'brilliant', 'superb', 'impressive', 'positive',
    'inspiring', 'motivating', 'incredible', 'exceptional', 'fabulous', 'marvelous',
    'beautiful', 'appreciate', 'thankful', 'grateful', 'admire', 'respect', 'cheers',
    'support', 'happy', 'joyful', 'delighted', 'proud', 'remarkable', 'encourage',
    'helpful', 'valuable', 'nice', 'kind', 'generous', 'graceful', 'uplifting',
    'phenomenal', 'enjoyed', 'commend', 'congratulations', 'glad', 'positive vibes',
    'blessing', 'charming', 'flawless', 'perfect', 'exceptional', 'yay', 'well played',
    'priceless', 'gifted', 'cool', 'legendary', 'masterpiece', 'genius', 'super', 
    'stellar', 'wow', 'bravo', 'respectful', 'gracious', 'pleasant', 'heartwarming',
    'loved', 'excellent','great job','thank you','keep it up','good work'
]

AGGRESSIVE_KEYWORDS = [
    'hate', 'terrible', 'awful', 'stupid', 'idiot', 'angry', 'furious', 'disgusting',
    'worst', 'horrible', 'pathetic', 'annoying', 'offensive', 'ridiculous', 'absurd',
    'irritating', 'arrogant', 'ignorant', 'disrespectful', 'toxic', 'bitter', 'evil',
    'nasty', 'selfish', 'coward', 'jerk', 'useless', 'suck', 'trash', 'cringe', 
    'worthless', 'fail', 'mean', 'aggressive', 'hostile', 'vicious', 'bully', 
    'vengeful', 'criticize', 'mock', 'insult', 'exploit', 'greedy', 'obnoxious', 
    'manipulative', 'vindictive', 'jealous', 'savage', 'barbaric', 'ruin', 
    'hateful', 'ignorance', 'provoking', 'irresponsible', 'chaotic', 'violent', 
    'negative', 'demeaning', 'judgmental', 'malicious', 'cruel', 'tyrant','shut up','get lost','how dare you','what the hell'
]

# Emoji dictionaries
EMOJI_SUPPORTIVE = {
    ":smile:": 0.5,
    ":tada:": 0.5,
    ":heart:": 0.5,
}
EMOJI_AGGRESSIVE = {
    ":angry:": 0.5,
    ":face_with_symbols_on_mouth:": 0.5,
}

# Punctuation or sarcastic indicators
SARCASTIC_INDICATORS = ['!', '?', '...']

def load_json_data(file_path):
    """Load data from a JSON file."""
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def clean_text(text):
    """Clean and preprocess text."""
    if not isinstance(text, str):
        return ""
    
    # Replace emojis with textual descriptions
    text = emoji.demojize(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    
    # Remove mentions (e.g., @username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Convert to lowercase for consistent keyword matching
    return text.strip().lower()

def custom_keyword_score(text):
    """
    Calculate custom scores based on keyword lists.
    Increment scores for each matched keyword and apply additional weights.
    Include breakdown of score contributions.
    """
    supportive_score = 0
    aggressive_score = 0
    contributions = {'supportive': [], 'aggressive': []}

    # Tokenize words while preserving punctuation
    words = re.findall(r'\b\w+\b', text)
    punctuation_marks = re.findall(r'[!?]', text)

    print(f"Analyzing text: {text}")  # Debug: Show the text being analyzed

    # Check for keywords
    for word in words:
        # Supportive keyword scoring
        if word.lower() in SUPPORTIVE_KEYWORDS:
            supportive_score += 1.0  # Base score
            contributions['supportive'].append(f"Keyword: {word}")
            if word.isupper():  # Add weight for uppercase
                supportive_score += WEIGHTS['uppercase']
                contributions['supportive'].append(f"Uppercase: {word}")

        # Aggressive keyword scoring
        if word.lower() in AGGRESSIVE_KEYWORDS:
            aggressive_score += 1.0  # Base score
            contributions['aggressive'].append(f"Keyword: {word}")
            if word.isupper():  # Add weight for uppercase
                aggressive_score += WEIGHTS['uppercase']
                contributions['aggressive'].append(f"Uppercase: {word}")

    # Add weight for punctuation emphasis (outside word loop)
    for mark in punctuation_marks:
        if mark in SARCASTIC_INDICATORS:
            supportive_score += WEIGHTS['punctuation']
            aggressive_score += WEIGHTS['punctuation']
            contributions['supportive'].append(f"Punctuation: {mark}")
            contributions['aggressive'].append(f"Punctuation: {mark}")

    # Add weight for emojis
    for emj, score in EMOJI_SUPPORTIVE.items():
        if emj in text:
            supportive_score += score
            contributions['supportive'].append(f"Emoji: {emj}")
    for emj, score in EMOJI_AGGRESSIVE.items():
        if emj in text:
            aggressive_score += score
            contributions['aggressive'].append(f"Emoji: {emj}")

    # Determine sentiment
    sentiment = "neutral"
    if supportive_score > aggressive_score and supportive_score > 0:
        sentiment = "supportive"
    elif aggressive_score > supportive_score and aggressive_score > 0:
        sentiment = "aggressive"
    elif supportive_score > 0 and aggressive_score > 0:
        sentiment = "sarcastic"

    print(f"Final Scores: Supportive={supportive_score}, Aggressive={aggressive_score}")  # Debug

    return {
        'supportive_score': supportive_score,
        'aggressive_score': aggressive_score,
        'sentiment': sentiment,
        'contributions': contributions
    }

def process_comments(file_path):
    """Process and analyze comments from a JSON file."""
    data = load_json_data(file_path)
    analyzed_comments = []
    
    for comment in data:
        author = comment.get('author', 'Unknown')
        text = comment.get('text', '')
        timestamp = comment.get('timestamp', 'Unknown')
        
        cleaned_text = clean_text(text)
        custom_analysis = custom_keyword_score(cleaned_text)
        
        analyzed_comment = {
            'author': author,
            'original_text': text,
            'cleaned_text': cleaned_text,
            'timestamp': timestamp,
            'analysis': custom_analysis
        }
        analyzed_comments.append(analyzed_comment)
    
    return analyzed_comments

def save_analyzed_data(analyzed_comments, output_file):
    """Save analyzed comments to a JSON file."""
    try:
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(analyzed_comments, file, indent=4, ensure_ascii=False)
        print(f"Analyzed data saved to: {output_file}")
    except Exception as e:
        print(f"Error saving analyzed data: {e}")

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
        
        for comment in analyzed_comments[:2]:  # Show first 2 as examples
            print("\nOriginal:", comment['original_text'])
            print("Cleaned:", comment['cleaned_text'])
            print("Custom Analysis:", comment['analysis'])
    
    output_file = 'output/custom_analyzed_comments.json'
    save_analyzed_data(all_analyzed_comments, output_file)
    print(f"\nTotal comments processed: {len(all_analyzed_comments)}")

if __name__ == "__main__":
    main()
