from flask import Flask

from model import ModelModel, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Sun580800@localhost/tomibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def base():
    return "penis"

@app.route('/test')
def create():
    model1 = ModelModel(model_name='testModel', article_number='article')
    db.session.add(model1)
    db.session.commit()
    return "good"


@app.route('/test/delete')
def delete():
    return "hui"


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
