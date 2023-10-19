from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(30))
    title = db.Column(db.String(30))
    composer = db.Column(db.String(30))
    arranger = db.Column(db.String(30))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        scores = Score.query.all()
        return render_template('index.html', scores=scores)

    else:
        number = request.form.get('number')
        title = request.form.get('title')
        composer = request.form.get('composer')
        arranger = request.form.get('arranger')

        new_score = Score(number=number, title=title, composer=composer, arranger=arranger)

        db.session.add(new_score)
        db.session.commit()
        return redirect('/')

@app.route('/add', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        form_number = request.form.get("number")
        form_title = request.form.get("title")
        form_composer = request.form.get("composer")
        form_arranger = request.form.get("arranger")

        score = Score(
            number = form_number,
            title = form_title,
            composer = form_composer,
            arranger = form_arranger
        )
        db.session.add(score)
        db.session.commit()
        return render_template('add.html')

@app.route('/score_list')
def score_list():
    scores = Score.query.all()
    return render_template('score_list.html', scores=scores)

@app.route('/score_search', methods=['GET', 'POST'])
def score_search():
    if request.method == 'GET':
        return render_template('score_search.html')
    if request.method == 'POST':
        form_title = request.form.get("title")
        search_results = db.session.query(Score).filter(Score.title.contains(form_title))
        return render_template('result.html', search_results=search_results)

@app.route('/scores/<int:id>/delete', methods=['POST'])
def score_delete(id):
    score = Score.query.get(id)
    db.session.delete(score)
    db.session.commit()
    return redirect(url_for('score_list'))

@app.route('/scores/<int:id>/edit', methods=['GET'])
def score_edit(id):
    # 編集ページ表示用
    score = Score.query.get(id)
    return render_template('score_edit.html', score=score)

@app.route('/scores/<int:id>/update', methods=['POST'])
def score_update(id):
    score = Score.query.get(id) 
    score.number = request.form.get("number")
    score.title = request.form.get("title")
    score.composer = request.form.get("composer")
    score.arranger = request.form.get("arranger")

    db.session.merge(score)
    db.session.commit()
    return redirect(url_for('score_list'))

if __name__ == '__main__':
	app.run()