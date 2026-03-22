from flask import Flask, render_template, request, redirect, url_for
from langdetect import detect
from googletrans import Translator
from rake_nltk import Rake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd
#from google.cloud import translate_v2 as translate

app = Flask(__name__)

# Sample news article text (for testing)
news_article = """
The economy is facing challenges due to the ongoing pandemic.
The government announced a new healthcare initiative to improve public health.
The education department launched a new program for student scholarships.
"""

# Sample news article 2 (for testing)
news_article_2 = """
The company announced massive layoffs, leaving hundreds of employees jobless.
The stock market crashed, causing investors to incur heavy losses.
Severe weather conditions led to widespread flooding and property damage.
"""

# Language Detection and Translation
def detect_and_translate(text):
    try:
        language = detect(text)
        print(f"Detected language: {language}")
        if language != 'en':
            translator = Translator()
            translated = translator.translate(text, src=language, dest='en')
            print("Translation complete")
            return translated.text
        return text
    except Exception as e:
        print(f"Error detecting or translating language: {str(e)}")
        return text

# def detect_and_translate(text):
#     try:
#         # Instantiate the Translator
#         translator = Translator()
#
#         # Detect the language
#         detection = translator.detect(text)
#         language = detection.lang
#         print(f"Detected language: {language}")
#
#         # Translate the text if it's not in English
#         if language != 'en':
#             translated = translator.translate(text, src=language, dest='en')
#             print("Translation complete")
#             return translated.text
#
#         return text
#     except AttributeError as e:
#         print(f"AttributeError: {str(e)}")
#         if 'group' in str(e):
#             print("This error is likely due to an issue with the googletrans library.")
#         return text
#     except Exception as e:
#         print(f"Error detecting or translating language: {str(e)}")
#         return text


# def detect_and_translate(text):
#     try:
#         # Instantiate the Translator
#         translator = translate.Client()
#
#         # Detect the language
#         detection = translator.detect_language(text)
#         language = detection['language']
#         print(f"Detected language: {language}")
#
#         # Translate the text if it's not in English
#         if language != 'en':
#             translation = translator.translate(text, target_language='en')
#             print("Translation complete")
#             return translation['translatedText']
#
#         return text
#     except Exception as e:
#         print(f"Error detecting or translating language: {str(e)}")
#         return text


# Keyword Extraction
def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()

# Sentiment Analysis for Negative News Detection
def detect_negative_news(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    print(f"Sentiment score: {compound_score}")
    if compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Positive'

def send_email_notification(file_content, url, sentiment):
    email_address = 'kartik20csu232@ncuindia.edu'
    email_password = 'keym mbjf slqu ioob'
    recipient_email = 'arpit20csu221@ncuindia.edu'

    subject = f"{sentiment} News Detected"
    message_body = f"{sentiment} news detected.\n\nLink: {url}\n\nContent:\n{file_content}"

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        text = msg.as_string()
        server.sendmail(email_address, recipient_email, text)
        server.quit()
        print("Email sent successfully")
        return "Email notification sent."
    except Exception as e:
        print(f"Error sending email notification: {str(e)}")
        return f"Error sending email notification: {str(e)}"

# Sentiment Analysis for Negative News Detection
def detect_negative_news(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    print(f"Sentiment score: {compound_score}")
    if compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Positive'


def web_scraper():
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    websites = [
        # 'https://indianexpress.com/article/political-pulse/',
        # 'https://indianexpress.com/article/india/',
        #'https://www.bhaskar.com/local/',
        #'https://www.bhaskar.com/national/',
        'https://www.bhaskar.com/national/national/news/delhi-liquor-policy-scam-case-ed-vs-aap-manish-sisodia-133018633.html',
        'https://www.bhaskar.com/national/national/news/aap-leader-swati-maliwal-misbehavior-case-updates-133020707.html'



    ]

    workbook = xlsxwriter.Workbook('ScrapedData.xlsx')
    worksheet = workbook.add_worksheet()

    headers = ["Heading", "Body", "Category", "URL"]
    worksheet.write_row(0, 0, headers)
    row = 1

    def scrape_website(base_url):
        nonlocal row
        try:
            r = requests.get(base_url, headers=HEADERS)
            urls_to_visit = []
            unique_urls = {}

            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                for link in soup.findAll('a', href=True):
                    href = link['href']
                    if href.startswith('/') and base_url + href not in unique_urls:
                        full_url = base_url + href if href.startswith('/') else href
                        if full_url not in unique_urls:
                            unique_urls[full_url] = True
                            urls_to_visit.append(full_url)

            for url in urls_to_visit:
                page = requests.get(url, headers=HEADERS)
                if page.status_code == 200:
                    soup = BeautifulSoup(page.content, 'html.parser')
                    heading = soup.find('h1').text.strip() if soup.find('h1') else ''
                    body = '\n'.join([p.text.strip() for p in soup.find_all('p')])
                    category = soup.find('span', class_='kicker').text.strip() if soup.find('span', class_='kicker') else ''
                    worksheet.write(row, 0, heading)
                    worksheet.write(row, 1, body)
                    worksheet.write(row, 2, category)
                    worksheet.write(row, 3, url)
                    row += 1
        except Exception as e:
            print(f"Error scraping {base_url}: {e}")

    for website in websites:
        scrape_website(website)

    workbook.close()
    print("Data written to worksheet successfully.")

def analyze_articles_and_notify():
    try:
        df = pd.read_excel('ScrapedData.xlsx')
        for index, row in df.iterrows():
            body1 = row['Body']
            url = row['URL']
            if pd.isna(body1) or body1.strip() == "":
                print(f"Skipping empty article at {url}")
                continue
            print(f"Analyzing article: {url}")
            body = detect_and_translate(body1)
            sentiment = detect_negative_news(body)
            send_email_notification(body1, url, sentiment)
    except Exception as e:
        print(f"Error in analysis and notification: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    email_notification = None

    # if request.method == 'POST':
    #     if 'file' in request.files:
    #         uploaded_file = request.files['file']
    #         if uploaded_file and uploaded_file.filename != '':
    #             file_content = uploaded_file.read().decode('utf-8')
    #             email_notification = send_email_notification(file_content, "Uploaded file", sentiment = sent)
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file and uploaded_file.filename != '':
                file_content = uploaded_file.read().decode('utf-8')
                email_notification = send_email_notification(file_content, "Uploaded file", detect_negative_news(file_content))

        if 'scrape' in request.form:
            web_scraper()
            analyze_articles_and_notify()
            email_notification = 'Scraping and Analysis Complete'

        return render_template('index.html', email_notification=email_notification)

    return render_template('index.html', email_notification=None)

@app.route('/home.html')
def next_page():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)