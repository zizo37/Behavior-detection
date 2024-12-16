# import json
# import re
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from textblob import TextBlob
# import pandas as pd
# from mongo import connect_to_mongo, fetch_comments
# import emoji  

# # Download required NLTK data
# try:
#     nltk.download('punkt')
#     nltk.download('stopwords')
#     nltk.download('wordnet')
#     nltk.download('averaged_perceptron_tagger')
# except:
#     print("NLTK data already downloaded or failed to download")

# class CommentPreprocessor:
#     def __init__(self):
#         self.lemmatizer = WordNetLemmatizer()
#         self.stop_words = set(stopwords.words('english'))
        
#     def load_comments_from_json(self, file_path):
#         """Load comments from JSON file"""
#         try:
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 data = json.load(file)
#                 return [comment['text'] for comment in data]
#         except Exception as e:
#             print(f"Error loading JSON file: {e}")
#             return []

#     def clean_text(self, text):
#         """Clean and preprocess text"""
#         # Convert emojis to text
#         text = emoji.demojize(text, delimiters=(" ", " "))  # Converts 😊 to :smiling_face:
        
#         # Convert to lowercase
#         text = text.lower()
        
#         # Remove URLs
#         text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
#         # Remove special characters and numbers, but keep emoji descriptions
#         text = re.sub(r'[^\w\s:_-]', '', text)  # Modified to keep emoji descriptions
#         text = re.sub(r'\d+', '', text)
        
#         # Tokenization
#         tokens = word_tokenize(text)
        
#         # Remove stopwords and lemmatize, but keep emoji descriptions
#         tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
#                  if token not in self.stop_words or ':' in token]  # Keep emoji descriptions
        
#         return ' '.join(tokens)

#     def analyze_sentiment(self, text):
#         """Analyze sentiment of text using TextBlob"""
#         analysis = TextBlob(text)
        
#         # Get polarity score (-1 to 1)
#         polarity = analysis.sentiment.polarity
        
#         # Classify sentiment
#         if polarity > 0.3:
#             return 'supportive'
#         elif polarity > 0:
#             return 'slightly_supportive'
#         elif polarity == 0:
#             return 'neutral'
#         elif polarity > -0.3:
#             return 'slightly_negative'
#         else:
#             return 'negative'

#     def process_comments(self, comments):
#         """Process a list of comments and return analysis results"""
#         results = []
        
#         for comment in comments:
#             cleaned_text = self.clean_text(comment)
#             sentiment = self.analyze_sentiment(cleaned_text)
            
#             results.append({
#                 'original_text': comment,
#                 'cleaned_text': cleaned_text,
#                 'sentiment': sentiment
#             })
        
#         return results

# def main():
#     # Initialize preprocessor
#     preprocessor = CommentPreprocessor()
    
#     # Load comments from JSON
#     json_file = 'comments_data_of_post_2.json'  # Update path as needed
#     comments = preprocessor.load_comments_from_json(json_file)
    
#     # Process comments
#     results = preprocessor.process_comments(comments)lll
    
#     # Convert results to DataFrame for better visualization
#     df = pd.DataFrame(results)
    
#     # Print summary
#     print("\nSentiment Analysis Results:")
#     try:
#         print(df['sentiment'].value_counts())
#     except KeyError:
#         print("Error: 'sentiment' column not found in the DataFrame. Please ensure the data was loaded and processed correctly.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
    
#     # Print detailed results
#     print("\nDetailed Analysis:")
#     for idx, row in df.iterrows():
#         print(f"\nOriginal Text: {row['original_text']}")
#         print(f"Sentiment: {row['sentiment']}")

# if __name__ == "__main__":
#     main() 



import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import pandas as pd
from mongo import connect_to_mongo, fetch_comments
import emoji  

# Download required NLTK data
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
except:
    print("NLTK data already downloaded or failed to download")

class CommentPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def load_comments_from_json(self, file_path):
        """Load comments from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [comment['text'] for comment in data]
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return []

    def clean_text(self, text):
        """Clean and preprocess text"""
        # Convert emojis to text
        text = emoji.demojize(text, delimiters=(" ", " "))  # Converts 😊 to :smiling_face:
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove special characters and numbers, but keep emoji descriptions
        text = re.sub(r'[^\w\s:_-]', '', text)  # Modified to keep emoji descriptions
        text = re.sub(r'\d+', '', text)
        
        # Tokenization
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize, but keep emoji descriptions
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words or ':' in token]  # Keep emoji descriptions
        
        return ' '.join(tokens)

    def process_comments(self, comments):
        """Process a list of comments and return cleaned results"""
        results = []
        
        for comment in comments:
            cleaned_text = self.clean_text(comment)
            
            results.append({
                'original_text': comment,
                'cleaned_text': cleaned_text
            })
        
        return results
