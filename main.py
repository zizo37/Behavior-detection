# import json
# import re
# import os
# import emoji  # Library to handle emojis

# def load_json_data(file_path):
#     """Load data from a JSON file"""
#     try:
#         if not os.path.exists(file_path):
#             print(f"File not found: {file_path}")
#             return []
        
#         with open(file_path, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     except json.JSONDecodeError as e:
#         print(f"Invalid JSON format in {file_path}: {e}")
#         return []
#     except Exception as e:
#         print(f"Error loading {file_path}: {e}")
#         return []

# def clean_text(text):
#     """Clean and preprocess text while retaining sentiment-relevant features"""
#     if not isinstance(text, str):
#         return ""
    
#     # Replace emojis with their textual descriptions
#     text = emoji.demojize(text)  # Converts 😀 to :grinning_face:
    
#     # Remove URLs
#     text = re.sub(r'http\S+|www.\S+', '', text)
    
#     # Remove mentions (e.g., @username)
#     text = re.sub(r'@\w+', '', text)
    
#     # Remove extra whitespace
#     text = ' '.join(text.split())
    
#     # Retain punctuation and basic characters, but remove other special characters
#     text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    
#     return text.strip()

# def process_comments(file_path):
#     """Process all comments in a JSON file"""
#     data = load_json_data(file_path)
#     cleaned_comments = []
    
#     for comment in data:
#         # Check if required keys exist
#         author = comment.get('author', 'Unknown')
#         text = comment.get('text', '')
#         timestamp = comment.get('timestamp', 'Unknown')
        
#         cleaned_comment = {
#             'author': author,
#             'original_text': text,
#             'cleaned_text': clean_text(text),
#             'timestamp': timestamp
#         }
#         cleaned_comments.append(cleaned_comment)
    
#     return cleaned_comments

# def save_cleaned_data(cleaned_comments, output_file):
#     """Save cleaned comments to a new JSON file"""
#     try:
#         output_dir = os.path.dirname(output_file)
#         if output_dir and not os.path.exists(output_dir):
#             os.makedirs(output_dir)
            
#         with open(output_file, 'w', encoding='utf-8') as file:
#             json.dump(cleaned_comments, file, indent=4, ensure_ascii=False)
#         print(f"Cleaned data saved to: {output_file}")
#     except Exception as e:
#         print(f"Error saving cleaned data: {e}")

# def main():
#     # Process both JSON files
#     files = [
#         'json/comments_data_of_post_1.json',
#         'json/comments_data_of_post_2.json'
#     ]
    
#     all_cleaned_comments = []
#     for file_path in files:
#         print(f"\nProcessing {file_path}:")
#         cleaned_comments = process_comments(file_path)
#         all_cleaned_comments.extend(cleaned_comments)
        
#         # Print example of original and cleaned text
#         for comment in cleaned_comments[:2]:  # Show first 2 comments as example
#             print("\nOriginal:", comment['original_text'])
#             print("Cleaned:", comment['cleaned_text'])
    
#     # Save all cleaned comments to a new file
#     output_file = 'outputs/cleaned_comments.json'
#     save_cleaned_data(all_cleaned_comments, output_file)
    
#     # Print summary
#     print(f"\nTotal comments processed: {len(all_cleaned_comments)}")

# if __name__ == "__main__":
#     main()



import json
import re
import os
import json
import re
import os
import emoji

def load_json_data(file_path):
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
    if not isinstance(text, str):
        return ""
    text = emoji.demojize(text)
    text = re.sub(r'http\S+|www.\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = ' '.join(text.split())
    return text.strip()  #" Hello world " → "Hello world"

def is_supportive(comment):
    supportive_keywords = [
        'great', 'well done', 'excellent', 'proud', 'amazing', 'fantastic', 
        'support', 'encourage', 'good job', 'congratulations', 'love'
    ]
    
    
    matched_keywords = []
    for keyword in supportive_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', comment, re.IGNORECASE):
            matched_keywords.append(keyword)
    
    return (bool(matched_keywords), matched_keywords)

def process_comments(file_path):
    data = load_json_data(file_path)
    analyzed_comments = []
    
    for comment in data:
        author = comment.get('author', 'Unknown')
        text = comment.get('text', '')
        timestamp = comment.get('timestamp', 'Unknown')
        
        cleaned_text = clean_text(text)
        supportive, rationale = is_supportive(cleaned_text)
        
        analyzed_comment = {
            'author': author,
            'original_text': text,
            'cleaned_text': cleaned_text,
            'timestamp': timestamp,
            'supportive': supportive,
            'rationale': rationale if supportive else []
        }
        analyzed_comments.append(analyzed_comment)
    
    return analyzed_comments

def save_cleaned_data(cleaned_comments, output_file):
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
        
        for comment in analyzed_comments[:2]:
            print("\nOriginal:", comment['original_text'])
            print("Cleaned:", comment['cleaned_text'])
            print("Supportive:", comment['supportive'])
            if comment['supportive']:
                print("Rationale:", comment['rationale'])
    
    output_file = 'output3/analyzed_comments.json'
    save_cleaned_data(all_analyzed_comments, output_file)
    
    print(f"\nTotal comments processed: {len(all_analyzed_comments)}")

if __name__ == "__main__":
    main()
