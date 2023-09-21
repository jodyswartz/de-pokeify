from flask import Flask, render_template, request

app = Flask(__name__)

with open('documentation/assets/pokemon_names.txt', 'r') as file:
    main_list = [line.strip() for line in file]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    input_list = request.form.get('input_list')

    input_words = [word.strip() for word in input_list.split(",")]
    contained_words = [word for word in input_words if word in main_list]
    not_contained_words = [word for word in input_words if word not in main_list]

    return render_template('result.html',
                           contained_words=contained_words,
                           not_contained_words=not_contained_words)


if __name__ == '__main__':
    app.run(debug=True)
