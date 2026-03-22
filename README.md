# 📰 Intelligent News Monitoring & Sentiment Analysis System

## 📌 Overview

This project is an automated news monitoring and sentiment analysis system that collects news articles from web sources, analyzes their sentiment, and sends email notifications based on detected sentiment.

The system is designed to identify negative news trends and provide real-time alerts, making it useful for decision-making, media monitoring, and reputation management.

---

## 🚀 Features

* 🌐 Web scraping of news articles from multiple sources
* 🌍 Automatic language detection and translation to English
* 🔑 Keyword extraction from articles
* 📊 Sentiment analysis (Positive / Negative classification)
* 📧 Automated email notifications for detected sentiment
* 📁 Data storage in Excel format for further analysis
* 🖥️ Simple web interface using Flask

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Libraries:**

  * Pandas
  * BeautifulSoup
  * Requests
  * VADER Sentiment Analysis
  * RAKE (Keyword Extraction)
  * Langdetect
  * Googletrans
* **Other Tools:** SMTP (Email automation), XlsxWriter

---

## 📊 Workflow

1. Scrape news articles from websites
2. Extract headings, content, category, and URLs
3. Detect language and translate to English (if needed)
4. Perform sentiment analysis using VADER
5. Classify news as Positive or Negative
6. Send email alerts for detected sentiment
7. Store processed data in Excel file

---

## 🔍 Key Functionalities

### 🧠 Sentiment Analysis

* Uses VADER sentiment analyzer
* Classifies news based on compound score

### 🌐 Web Scraping

* Extracts real-time news content using BeautifulSoup

### 📧 Email Notification

* Automatically sends alerts when specific sentiment is detected

### 🌍 Multilingual Support

* Detects and translates non-English news

---

## 📈 Results

* Successfully automated news monitoring pipeline
* Real-time detection of negative news articles
* Efficient alert system for quick response

---

## 💡 Future Improvements

* Deploy as a web app (Streamlit/Cloud)
* Add real-time dashboard for analytics
* Integrate advanced NLP models (BERT, Transformers)
* Improve scraping scalability using APIs

---



## 👩‍💻 Author

**Ishita Kadyan**
Master’s in Computer Science & Engineering

---

