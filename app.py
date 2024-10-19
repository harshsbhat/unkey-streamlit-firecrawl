import os
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import textstat

load_dotenv()

firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
unkey_root_key = os.getenv('UNKEY_ROOT_KEY')
firecrawl_app = FirecrawlApp(api_key=firecrawl_api_key)

st.title('Content Readability Scorer')

st.sidebar.header('User Input')
url = st.sidebar.text_input('Enter URL to analyze:')
analyze_button = st.sidebar.button('Analyze Content')

def get_client_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        ip_data = response.json()
        return ip_data['ip']
    except Exception as e:
        st.error(f"Could not retrieve IP address: {e}")
        return None

def check_unkey_rate_limit(ip_address):
    url = "https://api.unkey.dev/v1/ratelimits.limit"
    payload = {
        "namespace": "firecrawl.streamlit",
        "identifier": ip_address,
        "limit": 3,
        "duration": 180000, 
        "cost": 1,
    }
    headers = {
        "Authorization": f"Bearer {unkey_root_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def analyze_readability(url):
    result = firecrawl_app.scrape_url(url, params={'formats': ['html']})
    html_content = result.get('html', '')
    soup = BeautifulSoup(html_content, 'html.parser')
    
    main_content = soup.find(['main', 'article', 'body'])
    if main_content:
        text_content = main_content.get_text(separator=' ', strip=True)
    else:
        text_content = soup.get_text(separator=' ', strip=True)

    text_content = clean_text(text_content)
    
    if not text_content:
        raise ValueError("No readable text found on the page.")

    flesch_reading_ease = textstat.flesch_reading_ease(text_content)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(text_content)
    smog_index = textstat.smog_index(text_content)
    coleman_liau_index = textstat.coleman_liau_index(text_content)
    automated_readability_index = textstat.automated_readability_index(text_content)
    
    sentences = re.split(r'[.!?]+', text_content)
    sentences = [s for s in sentences if s]
    words = simple_word_tokenize(text_content)
    
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    return {
        'flesch_reading_ease': flesch_reading_ease,
        'flesch_kincaid_grade': flesch_kincaid_grade,
        'smog_index': smog_index,
        'coleman_liau_index': coleman_liau_index,
        'automated_readability_index': automated_readability_index,
        'avg_sentence_length': avg_sentence_length,
        'avg_word_length': avg_word_length,
        'total_words': len(words),
        'total_sentences': len(sentences)
    }

def simple_word_tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def interpret_score(score, metric):
    if metric == 'flesch_reading_ease':
        if score >= 90: return 'Very Easy'
        elif score >= 80: return 'Easy'
        elif score >= 70: return 'Fairly Easy'
        elif score >= 60: return 'Standard'
        elif score >= 50: return 'Fairly Difficult'
        elif score >= 30: return 'Difficult'
        else: return 'Very Difficult'
    else:  
        if score <= 6: return 'Easy'
        elif score <= 10: return 'Average'
        elif score <= 14: return 'Difficult'
        else: return 'Very Difficult'

if analyze_button and url:
    client_ip = get_client_ip()  
    if client_ip:
        rate_limit_response = check_unkey_rate_limit(client_ip)

        if rate_limit_response.get("success", False):
            with st.spinner('Analyzing content readability...'):
                try:
                    results = analyze_readability(url)
                    
                    st.subheader('Readability Analysis Results')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Flesch Reading Ease", f"{results['flesch_reading_ease']:.2f}", 
                                  interpret_score(results['flesch_reading_ease'], 'flesch_reading_ease'))
                        st.metric("Flesch-Kincaid Grade", f"{results['flesch_kincaid_grade']:.2f}", 
                                  interpret_score(results['flesch_kincaid_grade'], 'grade'))
                        st.metric("SMOG Index", f"{results['smog_index']:.2f}", 
                                  interpret_score(results['smog_index'], 'grade'))
                    with col2:
                        st.metric("Coleman-Liau Index", f"{results['coleman_liau_index']:.2f}", 
                                  interpret_score(results['coleman_liau_index'], 'grade'))
                        st.metric("Automated Readability Index", f"{results['automated_readability_index']:.2f}", 
                                  interpret_score(results['automated_readability_index'], 'grade'))
                    
                    st.subheader('Additional Metrics')
                    st.write(f"Average Sentence Length: {results['avg_sentence_length']:.2f} words")
                    st.write(f"Average Word Length: {results['avg_word_length']:.2f} characters")
                    st.write(f"Total Words: {results['total_words']}")
                    st.write(f"Total Sentences: {results['total_sentences']}")
                    
                    # Creating the bar plot for readability scores
                    fig, ax = plt.subplots()
                    scores = [
                        results['flesch_reading_ease'], 
                        results['flesch_kincaid_grade'], 
                        results['smog_index'], 
                        results['coleman_liau_index'], 
                        results['automated_readability_index']
                    ]
                    labels = [
                        'Flesch Reading Ease', 
                        'Flesch-Kincaid Grade', 
                        'SMOG Index', 
                        'Coleman-Liau Index', 
                        'Automated Readability Index'
                    ]
                    sns.barplot(x=labels, y=scores, ax=ax)
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                    ax.set_ylabel('Score')
                    ax.set_title('Readability Scores')
                    st.pyplot(fig)
                    
                    st.subheader('Interpretation')
                    st.write("""
                    - Flesch Reading Ease: Higher scores indicate easier readability (0-100 scale).
                    - Other indices approximate the U.S. grade level needed to understand the text.
                    - Aim for a Flesch Reading Ease score above 60 for general audience content.
                    - For most web content, aim for a grade level between 7-9 for optimal readability.
                    """)
                    
                except Exception as e:
                    st.error(f"Error analyzing {url}: {str(e)}")
        else:
            st.error("Rate limit exceeded. Please try again later.")

st.sidebar.subheader('Firecrawl API Status')
if firecrawl_api_key:
    st.sidebar.success('Firecrawl API key is set')
else:
    st.sidebar.error('Firecrawl API key is not set')
