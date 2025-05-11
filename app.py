#importing libraries
import streamlit as st
import nltk
import pickle
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download necessary NLTK data
nltk.download("punkt")
nltk.download('stopwords')

#Load model
model = pickle.load(open("fakenews_detection_model.pkl", "rb"))
#load vectorizer
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

with st.sidebar:
     st.image("img.png", use_column_width =True)
     st.markdown(""" ## 📰 Fake News Detector  
                 
This app analyzes news content and predicts whether it's **Real** or **Fake** using Natural Language Processing and Machine Learning.
""")
#App title 
st.title("📰 Fake News Detector")
text = st.text_area("✍️ Your News", height=150)
st.write("Enter a news below and click **Predict** to it's real or fake.")

# defining function to clean input news
def data_cleaning(text):
    stop_words = set(stopwords.words("english")) #loading stopwords form nltk
    # wordnet lemmatizer to reduce words to their base form
    lemmatizer = WordNetLemmatizer()
    text = re.sub("[^a-zA-Z]", " ", str(text))   #removing all characters except alphabets
    text = re.sub(r"\s+", " ", text)
    text = text.lower()                          #converting into lowercase
    tokens = word_tokenize(text)                 #tokenizing text into words
    # removing stopwords and tokens and apply lemmatization
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and len(token) > 1]
    return " ".join(tokens)

if text:
    cleaned_text = data_cleaning(text)
    # converting data into vectors
    X_tfidf = vectorizer.transform([cleaned_text])

# predicting    
if st.button("🔮 Predict"):
        prediction = model.predict(X_tfidf)
        st.subheader("🧠 Prediction Result")
        if (prediction[0]==1):
             st.success("✅ Real News")
        else:
             st.error("❌ Fake News")

