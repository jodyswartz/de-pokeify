from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

with open('documentation/assets/pokemon_names.txt', 'r') as file:
    main_list = [line.strip() for line in file]


def extract_technical_words(text, not_contained_words):
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)

    # Remove stopwords
    words = [word.lower() for word in words if word.lower() not in stopwords.words('english')]

    # Perform part-of-speech tagging
    tagged_words = nltk.pos_tag(words)

    # Identify technical words based on their tags
    tech_words_found = [word for word, tag in tagged_words if tag.startswith('NN') and word in not_contained_words]

    technical_words_found = list(set(tech_words_found))
    return technical_words_found


def fetch_and_parse_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text
    except Exception as e:
        print(f"Error fetching or parsing URL: {e}")
        return ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    input_list = request.form.get('input_list')
    urls = ["https://en.wikipedia.org/wiki/List_of_computing_and_IT_abbreviations"]

    input_words = [word.strip() for word in input_list.split(",")]
    contained_words = [word for word in input_words if word in main_list]
    not_pokemon_words = [word for word in input_words if word not in main_list]

    for url in urls:
        text = fetch_and_parse_url(url)
        tech_term_words = extract_technical_words(text, not_pokemon_words)
        print(f"Technical words found in {url}: {tech_term_words}")

    unique_to_list1 = [word for word in not_pokemon_words if word not in tech_term_words]
    unique_to_list2 = [word for word in tech_term_words if word not in not_pokemon_words]

    unknown_words = unique_to_list1 + unique_to_list2

    return render_template('result.html',
                           contained_words=contained_words,
                           tech_term_words=tech_term_words,
                           unknown_words=unknown_words)


if __name__ == '__main__':
    app.run(debug=True, port=5041)
