from yumroad import create_app, db
from yumroad.models import Product
app = create_app('dev')

def reset():
    with app.app_context():
        db.drop_all()
        setup()

def setup():
    with app.app_context():
        db.create_all()
        for i in range(10):
            prod = Product(name='Product {}'.format(i*20),
                           description='Book v{}'.format(i))
            db.session.add(prod)
        db.session.commit()
