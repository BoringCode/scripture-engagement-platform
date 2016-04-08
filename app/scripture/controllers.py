from flask import Flask, render_template, Blueprint

from app.scripture.bg_api import BGAPI

scripture = Blueprint('scripture', __name__)

app = Flask(__name__)
bg_api = BGAPI()

@scripture.route('/translations')
def list_translations():
    return render_template('scripture/translation-list.html', translations=bg_api.list_translations())


@scripture.route('/bible/<xlation>')
def get_translation_info(xlation):
    return render_template('scripture/translation-detail.html', translation=bg_api.get_translation(xlation))


@scripture.route('/bible/<xlation>/book/<book_osis>')
def get_book_info(xlation, book_osis):
    return render_template('scripture/book-detail.html', book=bg_api.get_book_info(xlation, book_osis), translation=xlation)


@scripture.route('/bible/<xlation>/passage/<passage_osis>')
def get_passage(xlation, passage_osis):
    return render_template('scripture/passage.html', verse=bg_api.get_passage(xlation, passage_osis))

if __name__ == '__main__':
    app.run(debug=True)



