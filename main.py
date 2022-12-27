from flask import Flask, request, render_template, redirect, abort
from db_init import db

from model import ModelModel, Sizes
from Shipment import shipment
from Delivery import Delivery
from Packing import Packing
from Jobs import Jobs
from Accessories import Accessories
from Materials import Materials
from Accessories_cost import Accessories_cost
from Materials_cost import Materials_cost

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Sun580800@localhost/tamibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def base():
    return "penis"

@app.route('/model/create' , methods = ['GET','POST'])
def CreateModel():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        model_name = request.form['model_name']
        article_number = request.form['article_number']
        photo = bytearray(request.form['photo'], encoding='utf-8')
        layout_patterns = bytearray(request.form['layout_patterns'], encoding='utf-8')
        tailoring_technology = request.form['tailoring_technology']
        size_range = request.form['size_range']
        NewModel = ModelModel(model_name, article_number, photo, layout_patterns, tailoring_technology, size_range)
        db.session.add(NewModel)
        db.session.commit()
        return str(NewModel)

@app.route('/model', methods=['GET'])
def RetrieveModelList():
    model_ = ModelModel.query.all()
    return str(model_)

@app.route('/model/<int:id>', methods = ['GET','POST', 'DELETE'])
def RetrieveUpdateDeleteSingleModel(id):
    model_ = ModelModel.query.filter_by(model_id=id).first()
    if request.method == 'GET':
        if model_:
            return render_template('Model.html', model_)
        return f"Model with id ={id} Doenst exist"
    if request.method == 'POST':
        if model_:
            model_.model_name = request.form['model_name']
            model_.article_number = request.form['article_number']
            model_.photo = bytearray(request.form['photo'], encoding = 'utf-8')
            model_.layout_patterns = bytearray(request.form['layout_patterns'], encoding = 'utf-8')
            model_.tailoring_technology = request.form['tailoring_technology']
            model_.size_range = request.form['size_range']
            #model_ = ModelModel(model_name, article_number, photo, layout_patterns, tailoring_technology, size_range)
            #NewModel.model_id=id
            db.session.add(model_)
            db.session.commit()
            up = ModelModel.query.filter_by(model_id=id).first()
            return str(up)
        return f"Model with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if model_:
            db.session.delete(model_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(model_)



@app.route('/go')
def createShipment():
    shipment1 = shipment(model_id=2, products_number = 20, rulers_number=2)
    db.session.add(shipment1)
    db.session.commit()
    return "go"

@app.route('/deliv')
def createDeliv():
    delivery1 = Delivery(3, 'kudykina gora', 'tudykina gora','Papa Slava', 'Soks', 3000)
    db.session.add(delivery1)
    db.session.commit()
    return "Papa Slava doechal"

@app.route('/pack')
def createPacking():
    packing1 = Packing(shipment_id=3, tags_cost=100, packege_cost=800, label_cost=200)
    db.session.add(packing1)
    db.session.commit()
    return "Korobochky"

@app.route('/jobs')
def createJobs():
    jobs1 = Jobs(3, 'kroy', 'cech', 200)
    db.session.add(jobs1)
    db.session.commit()
    return "cech chech"

@app.route('/acc')
def createAcc():
    accessories1 = Accessories(2, 'pugovka', 21)
    db.session.add(accessories1)
    db.session.commit()
    return "mnogo pugovak"

@app.route('/acc/cost')
def createAccCost():
    accessories_cost1 = Accessories_cost(3, 2, 100, 1200)
    db.session.add(accessories_cost1)
    db.session.commit()
    return "money pugovak"

@app.route('/mat')
def createMaterials():
    materials1 = Materials(3, 'pugovka', 2.1)
    db.session.add(materials1)
    db.session.commit()
    return "mnogo tkani"

@app.route('/mat/cost')
def createMaterialsCost():
    materials_cost1 = Materials_cost(3, 2, 10, 20.1)
    db.session.add(materials_cost1)
    db.session.commit()
    return "mnogo tkani"



if __name__ == '__main__':
    app.run(host='localhost', port=5000)
