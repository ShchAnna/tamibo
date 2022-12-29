from User import User
from flask import Flask, request, render_template, redirect, abort, url_for

import flask_excel as excel
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user

from UserLogin import UserLogin
from db_init import db

from models.Model import ModelModel
from models.Shipment import Shipment
from models.Delivery import Delivery
from models.Packing import Packing
from models.Jobs import Jobs
from models.Accessories import Accessories
from models.Materials import Materials
from models.Accessories_cost import Accessories_cost
from models.Materials_cost import Materials_cost

app = Flask(__name__)
excel.init_excel(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/tamibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager(app)


def doGetAll(model):
    q = db.select(model)
    return db.session.execute(q).scalars().all()


def get_attrs_names(model):
    return [c_attr.key for c_attr in inspect(model).mapper.column_attrs]


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, db)


@app.route('/')
def base():
    return "penis"


@app.route('/model/create', methods=['GET', 'POST'])
def CreateModel():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        model_name = request.form['model_name']
        article_number = request.form['article_number']
        photo = request.form['photo']
        layout_patterns = request.form['layout_patterns']
        tailoring_technology = request.form['tailoring_technology']
        size_range = request.form['size_range']
        NewModel = ModelModel(model_name, article_number, photo, layout_patterns, tailoring_technology, size_range)
        db.session.add(NewModel)
        db.session.commit()
        return str(NewModel)


@app.route('/model', methods=['GET'])
def RetrieveModelList():
    # model_ = ModelModel.query(ModelModel.model_id, ModelModel.model_name).all()
    result = doGetAll(ModelModel)
    return render_template("models_template.html", rows=result)


@app.route('/model/download', methods=['GET'])
def dowload():
    result = doGetAll(ModelModel)
    headers = [c_attr.key for c_attr in inspect(ModelModel).mapper.column_attrs]
    return excel.make_response_from_query_sets(query_sets=result, column_names=headers, file_type="xls",
                                               file_name='sukarabotai')


@app.route('/model/<int:id>', methods=['GET', 'POST', 'DELETE'])
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
            model_.photo = request.form['photo']
            model_.layout_patterns = request.form['layout_patterns']
            model_.tailoring_technology = request.form['tailoring_technology']
            model_.size_range = request.form['size_range']
            # model_ = ModelModel(model_name, article_number, photo, layout_patterns, tailoring_technology, size_range)
            # NewModel.model_id=id
            db.session.add(model_)
            db.session.commit()
            up = ModelModel.query.filter_by(model_id=id).first()
            return str(up)
        return f"Model with id = {id} Does nit exist"
    return str(model_)


@app.route('/model/<int:id>/delete', methods=['POST'])
def deleteModel(id):
    model_ = ModelModel.query.filter_by(model_id=id).first()
    if model_:
        db.session.delete(model_)
        db.session.commit()
        return redirect(url_for('RetrieveModelList'))
    abort(404)


@app.route('/shipment/create', methods=['GET', 'POST'])
def CreateShipment():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        model_id = request.form['model_id']
        shipment_date = request.form['shipment_date']
        products_number = request.form['products_number']
        rulers_number = request.form['rulers_number']
        NewShipment = Shipment(model_id, shipment_date, products_number, rulers_number)
        db.session.add(NewShipment)
        db.session.commit()
        return str(NewShipment)


@app.route('/shipment', methods=['GET'])
def RetrieveShipmentList():
    headers, result = doGetAll(Shipment)
    return render_template("entity_table.html",
                           page={'title': 'Партии', 'link': '/shipment'},
                           t={'headers': headers, 'rows': result})


@app.route('/shipment/<int:id>', methods=['GET', 'POST'])
def RetrieveUpdateDeleteSingleShipment(id):
    shipment_ = Shipment.query.filter_by(shipment_id=id).first()
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
            up = Shipment.query.filter_by(shipment_id=id).first()
            return str(up)
        return f"Shipment with id = {id} Does nit exist"


@app.route('/shipment/<int:id>/delete', methods=['POST'])
def deleteShipment(id):
    shipment_ = Shipment.query.filter_by(shipment_id=id).first()
    if shipment_:
        db.session.delete(shipment_)
        db.session.commit()
        return redirect(url_for('RetrieveShipmentList'))
    abort(404)


@app.route('/delivery/create', methods=['GET', 'POST'])
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
    headers, result = doGetAll(Delivery)
    return render_template("entity_table.html",
                           page={'title': 'Доставка', 'link': '/delivery'},
                           t={'headers': headers, 'rows': result})


@app.route('/delivery/<int:id>/delete', methods=['POST'])
def deleteDelivery(id):
    delivery_ = Delivery.query.filter_by(delivery_id=id).first()
    if delivery_:
        db.session.delete(delivery_)
        db.session.commit()
        return redirect(url_for('RetrieveDeliveryList'))
    abort(404)


@app.route('/delivery/<int:id>', methods=['GET', 'POST'])
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


@app.route('/packing/create', methods=['GET', 'POST'])
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


@app.route('/packing', methods=['GET'])
def RetrievePackingList():
    packing_ = Packing.query.all()
    return str(packing_)


@app.route('/packing/<int:id>', methods=['GET', 'POST', 'DELETE'])
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


@app.route('/jobs/create', methods=['GET', 'POST'])
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


@app.route('/jobs', methods=['GET'])
def RetrieveJobsList():
    jobs_ = Jobs.query.all()
    return str(jobs_)


@app.route('/jobs/<int:id>', methods=['GET', 'POST', 'DELETE'])
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


@app.route('/accessories/create', methods=['GET', 'POST'])
def CreateAccessories():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        model_id = request.form['model_id']
        accessories_name = request.form['accessories_name']
        number_per_one = request.form['number_per_one']
        NewAccessories = Accessories(model_id, accessories_name, number_per_one)
        db.session.add(NewAccessories)
        db.session.commit()
        return str(NewAccessories)


@app.route('/accessories', methods=['GET'])
def RetrieveAccessoriesList():
    accessories_ = Accessories.query.all()
    return str(accessories_)


@app.route('/accessories/<int:id>', methods=['GET', 'POST', 'DELETE'])
def RetrieveUpdateDeleteSingleAccessories(id):
    accessories_ = Accessories.query.filter_by(accessories_id=id).first()
    if request.method == 'GET':
        if accessories_:
            return str(accessories_)
        return f"Accessories with id ={id} Doenst exist"
    if request.method == 'POST':
        if accessories_:
            accessories_.model_id = request.form['model_id']
            accessories_.accessories_name = request.form['accessories_name']
            accessories_.number_per_one = request.form['number_per_one']

            db.session.add(accessories_)
            db.session.commit()
            up = Accessories.query.filter_by(accessories_id=id).first()
            return str(up)
        return f"Accessories with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if accessories_:
            db.session.delete(accessories_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(accessories_)


@app.route('/accessories_cost/create', methods=['GET', 'POST'])
def CreateAccessories_cost():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        shipment_id = request.form['shipment_id']
        accessories_id = request.form['accessories_id']
        accessories_number = request.form['accessories_number']
        accessories_cost = request.form['accessories_cost']
        NewAccessories_cost = Accessories_cost(shipment_id, accessories_id, accessories_number, accessories_cost)
        db.session.add(NewAccessories_cost)
        db.session.commit()
        return str(NewAccessories_cost)


@app.route('/accessories_cost', methods=['GET'])
def RetrieveAccessories_costList():
    accessories_cost_ = Accessories_cost.query.all()
    return str(accessories_cost_)


@app.route('/accessories_cost/<int:id>', methods=['GET', 'POST', 'DELETE'])
def RetrieveUpdateDeleteSingleAccessories_cost(id):
    accessories_cost_ = Accessories_cost.query.filter_by(accessories_cost_id=id).first()
    if request.method == 'GET':
        if accessories_cost_:
            return str(accessories_cost_)
        return f"Accessories_cost with id ={id} Doenst exist"
    if request.method == 'POST':
        if accessories_cost_:
            accessories_cost_.shipment_id = request.form['shipment_id']
            accessories_cost_.accessories_id = request.form['accessories_id']
            accessories_cost_.accessories_number = request.form['accessories_number']
            accessories_cost_.accessories_cost = request.form['accessories_cost']

            db.session.add(accessories_cost_)
            db.session.commit()
            up = Accessories_cost.query.filter_by(accessories_cost_id=id).first()
            return str(up)
        return f"Accessories_cost with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if accessories_cost_:
            db.session.delete(accessories_cost_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(accessories_cost_)


@app.route('/materials/create', methods=['GET', 'POST'])
def CreateMaterials():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        model_id = request.form['model_id']
        materials_name = request.form['materials_name']
        m_per_ruler = request.form['m_per_ruler']
        NewMaterials = Materials(model_id, materials_name, m_per_ruler)
        db.session.add(NewMaterials)
        db.session.commit()
        return str(NewMaterials)


@app.route('/materials', methods=['GET'])
def RetrieveMaterialsList():
    materials_ = Materials.query.all()
    return str(materials_)


@app.route('/materials/<int:id>', methods=['GET', 'POST', 'DELETE'])
def RetrieveUpdateDeleteSingleMaterials(id):
    materials_ = Materials.query.filter_by(materials_id=id).first()
    if request.method == 'GET':
        if materials_:
            return str(materials_)
        return f"Materials with id ={id} Doenst exist"
    if request.method == 'POST':
        if materials_:
            materials_.model_id = request.form['model_id']
            materials_.materials_name = request.form['materials_name']
            materials_.m_per_ruler = request.form['m_per_ruler']

            db.session.add(materials_)
            db.session.commit()
            up = Materials.query.filter_by(materials_id=id).first()
            return str(up)
        return f"Accessories with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if materials_:
            db.session.delete(materials_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(materials_)


@app.route('/materials_cost/create', methods=['GET', 'POST'])
def CreateMaterials_cost():
    if request.method == 'GET':
        return render_template('createModel.html')

    if request.method == 'POST':
        shipment_id = request.form['shipment_id']
        materials_id = request.form['materials_id']
        materials_number = request.form['materials_number']
        materials_cost = request.form['materials_cost']
        NewMaterials_cost_ = Materials_cost(shipment_id, materials_id, materials_number, materials_cost)
        db.session.add(NewMaterials_cost_)
        db.session.commit()
        return str(NewMaterials_cost_)


@app.route('/materials_cost', methods=['GET'])
def RetrieveMaterials_costList():
    materials_cost_ = Materials_cost.query.all()
    return str(materials_cost_)


@app.route('/materials_cost/<int:id>', methods=['GET', 'POST', 'DELETE'])
def RetrieveUpdateDeleteSingleMaterials_cost(id):
    materials_cost_ = Materials_cost.query.filter_by(materials_cost_id=id).first()
    if request.method == 'GET':
        if materials_cost_:
            return str(materials_cost_)
        return f"Materials_cost with id ={id} Doenst exist"
    if request.method == 'POST':
        if materials_cost_:
            materials_cost_.shipment_id = request.form['shipment_id']
            materials_cost_.materials_id = request.form['materials_id']
            materials_cost_.materials_number = request.form['materials_number']
            materials_cost_.materials_cost = request.form['materials_cost']

            db.session.add(materials_cost_)
            db.session.commit()
            up = Materials_cost.query.filter_by(materials_cost_id=id).first()
            return str(up)
        return f"Materials_cost with id = {id} Does nit exist"
    if request.method == 'DELETE':
        if materials_cost_:
            db.session.delete(materials_cost_)
            db.session.commit()
            return 'deleted'
        abort(404)
    return str(materials_cost_)


@app.route('/document/cost_price/<int:id>', methods=['GET'])
def Cost_price(id):
    if request.method == 'GET':
        delivery_cost = 0.0
        deliveries = db.session.query(Delivery).filter_by(shipment_id=id).all()
        countDelivery = db.session.query(Delivery).filter_by(shipment_id=id).count()
        for i in range(countDelivery):
            delivery_cost = delivery_cost + float(deliveries[0].delivery_cost)

        jobs_cost = 0.0
        jobses = db.session.query(Jobs).filter_by(shipment_id=id).all()
        countJobs = db.session.query(Jobs).filter_by(shipment_id=id).count()
        for i in range(countJobs):
            jobs_cost = jobs_cost + float(jobses[0].jobs_cost)

        packing_cost = 0.0
        packings = db.session.query(Packing).filter_by(shipment_id=id).all()
        countPacking = db.session.query(Packing).filter_by(shipment_id=id).count()
        for i in range(countPacking):
            packing_cost = packing_cost + float(packings[0].tags_cost) + float(packings[0].label_cost) + float(
                packings[0].packege_cost)

        accessories_cost = 0.0
        accessories_costes = db.session.query(Accessories_cost).filter_by(shipment_id=id).all()
        countAccessories_cost = db.session.query(Accessories_cost).filter_by(shipment_id=id).count()
        for i in range(countAccessories_cost):
            accessories_cost = accessories_cost + float(accessories_costes[0].accessories_cost)

        materials_cost = 0.0
        materials_costes = db.session.query(Materials_cost).filter_by(shipment_id=id).all()
        countMaterials_cost = db.session.query(Materials_cost).filter_by(shipment_id=id).count()
        for i in range(countMaterials_cost):
            materials_cost = materials_cost + float(materials_costes[0].materials_cost)

        cost_price = delivery_cost + jobs_cost + packing_cost + accessories_cost + materials_cost

        return str(cost_price)


def getUser(user_id):
    res = db.session.query(User).filter_by(user_id=user_id).first()
    if not res:
        print("Пользователь не найден")
        return False

    return res


def getUserByEmail(email):
    res = db.session.query(User).filter_by(email=email).first()
    if not res:
        print("Пользователь не найден")
        return False

    return res


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))

        return "Неверная пара логин/пароль", "error"

    return 0


def addUser(name, email, hpsw):
    user_ = User.query.filter_by(email=email).first()
    if user_:
        print("Пользователь с таким email уже существует")
        return False

    NewUser = User(name, email, hpsw)
    db.session.add(NewUser)
    db.session.commit()

    return True


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 2 and len(request.form['email']) > 4 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = addUser(request.form['name'], request.form['email'], hash)
            if res:
                return redirect(url_for('login'))
            else:
                return "Ошибка при добавлении в БД", "error"
        else:
            return "Неверно заполнены поля", "error"

    return 0


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
