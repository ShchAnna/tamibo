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
            return str(model_)
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

@app.route('/shipment/create' , methods = ['GET','POST'])
def CreateShipment():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        model_id = request.form['model_id']
        shipment_date = request.form['shipment_date']
        products_number = request.form['products_number']
        rulers_number = request.form['rulers_number']
        NewShipment = shipment(model_id, shipment_date, products_number, rulers_number)
        db.session.add(NewShipment)
        db.session.commit()
        return str(NewShipment)

@app.route('/shipment', methods=['GET'])
def RetrieveShipmentList():
    shipment_ = shipment.query.all()
    return str(shipment_)

@app.route('/shipment/<int:id>', methods = ['GET','POST', 'DELETE'])
def RetrieveUpdateDeleteSingleShipment(id):
    shipment_ = shipment.query.filter_by(shipment_id=id).first()
    if request.method == 'GET':
        if shipment_:
            return str(shipment_)
        return f"Shipment with id ={id} Doenst exist"
    if request.method == 'POST':
        if shipment_:
            shipment_.model_id = request.form['model_id']
            shipment_.shipment_date = request.form['shipment_date']
            shipment_.products_number = request.form['products_number']
            shipment_.rulers_number = request.form['rulers_number']
            db.session.add(shipment_)
            db.session.commit()
            up = shipment.query.filter_by(shipment_id=id).first()
            return str(up)
        return f"Shipment with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if shipment_:
            db.session.delete(shipment_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(shipment_)

@app.route('/delivery/create' , methods = ['GET','POST'])
def CreateDelivery():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        shipment_id = request.form['shipment_id']
        from_where = request.form['from_where']
        to_where = request.form['to_where']
        tipe_delivery = request.form['tipe_delivery']
        object_delivery = request.form['object_delivery']
        delivery_cost = request.form['delivery_cost']
        NewDelivery = Delivery(shipment_id, from_where, to_where, tipe_delivery, object_delivery, delivery_cost)
        db.session.add(NewDelivery)
        db.session.commit()
        return str(NewDelivery)

@app.route('/delivery', methods=['GET'])
def RetrieveDeliveryList():
    delivery_ = Delivery.query.all()
    return str(delivery_)

@app.route('/delivery/<int:id>', methods = ['GET','POST', 'DELETE'])
def RetrieveUpdateDeleteSingleDelivery(id):
    delivery_ = Delivery.query.filter_by(delivery_id=id).first()
    if request.method == 'GET':
        if delivery_:
            return str(delivery_)
        return f"Shipment with id ={id} Doenst exist"
    if request.method == 'POST':
        if delivery_:
            delivery_.shipment_id = request.form['shipment_id']
            delivery_.from_where = request.form['from_where']
            delivery_.to_where = request.form['to_where']
            delivery_.tipe_delivery = request.form['tipe_delivery']
            delivery_.object_delivery = request.form['object_delivery']
            delivery_.delivery_cost = request.form['delivery_cost']
            db.session.add(delivery_)
            db.session.commit()
            up = Delivery.query.filter_by(delivery_id=id).first()
            return str(up)
        return f"Delivery with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if delivery_:
            db.session.delete(delivery_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(delivery_)

@app.route('/packing/create' , methods = ['GET','POST'])
def CreatePacking():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        shipment_id = request.form['shipment_id']
        tags_cost = request.form['tags_cost']
        label_cost = request.form['label_cost']
        packege_cost = request.form['packege_cost']
        NewPacking = Packing(shipment_id, tags_cost, label_cost, packege_cost)
        db.session.add(NewPacking)
        db.session.commit()
        return str(NewPacking)

@app.route('/packing/<int:id>', methods = ['GET','POST', 'DELETE'])
def RetrieveUpdateDeleteSinglePacking(id):
    packing_ = Packing.query.filter_by(packing_id=id).first()
    if request.method == 'GET':
        if packing_:
            return str(packing_)
        return f"Packing with id ={id} Doenst exist"
    if request.method == 'POST':
        if packing_:
            packing_.shipment_id = request.form['shipment_id']
            packing_.tags_cost = request.form['tags_cost']
            packing_.label_cost = request.form['label_cost']
            packing_.packege_cost = request.form['packege_cost']

            db.session.add(packing_)
            db.session.commit()
            up = Packing.query.filter_by(packing_id=id).first()
            return str(up)
        return f"Packing with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if packing_:
            db.session.delete(packing_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(packing_)

@app.route('/jobs/create' , methods = ['GET','POST'])
def CreateJobs():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        shipment_id = request.form['shipment_id']
        jobs_tipe = request.form['jobs_tipe']
        employee = request.form['employee']
        jobs_cost = request.form['jobs_cost']
        NewJobs = Jobs(shipment_id, jobs_tipe, employee, jobs_cost)
        db.session.add(NewJobs)
        db.session.commit()
        return str(NewJobs)

@app.route('/jobs/<int:id>', methods = ['GET','POST', 'DELETE'])
def RetrieveUpdateDeleteSingleJobs(id):
    jobs_ = Jobs.query.filter_by(jobs_id=id).first()
    if request.method == 'GET':
        if jobs_:
            return str(jobs_)
        return f"Jobs with id ={id} Doenst exist"
    if request.method == 'POST':
        if jobs_:
            jobs_.shipment_id = request.form['shipment_id']
            jobs_.jobs_tipe = request.form['jobs_tipe']
            jobs_.employee = request.form['employee']
            jobs_.jobs_cost = request.form['jobs_cost']

            db.session.add(jobs_)
            db.session.commit()
            up = Jobs.query.filter_by(jobs_id=id).first()
            return str(up)
        return f"Packing with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if jobs_:
            db.session.delete(jobs_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(jobs_)


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
