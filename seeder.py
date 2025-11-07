from app import create_app
from database import db
from models import Product, User
from werkzeug.security import generate_password_hash

def seed_data():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Create an admin user
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', email='admin@eshop.com', is_admin=True)
            admin_user.set_password('adminpass')
            db.session.add(admin_user)
            print("Admin user 'admin' created with password 'adminpass'")

        # Create a regular user
        if not User.query.filter_by(username='testuser').first():
            test_user = User(username='testuser', email='test@eshop.com')
            test_user.set_password('testpass')
            db.session.add(test_user)
            print("Test user 'testuser' created with password 'testpass'")

        # Add some generic products
        if Product.query.count() == 0:
            products_data = [
                {
                    'name': 'Wireless Ergonomic Mouse',
                    'description': 'A comfortable and precise mouse for everyday use.',
                    'price': 29.99,
                    'stock': 150,
                    'image_url': 'https://www.euronics.lv/UserFiles/Products/Images/319463-480594-medium.png'
                },
                {
                    'name': 'Mechanical Gaming Keyboard',
                    'description': 'High-performance mechanical keyboard with RGB lighting.',
                    'price': 89.99,
                    'stock': 80,
                    'image_url': 'https://www.euronics.lv/UserFiles/Products/Images/288840-370745.png'
                },
                {
                    'name': 'Noise-Cancelling Headphones',
                    'description': 'Immersive audio experience with active noise cancellation.',
                    'price': 149.99,
                    'stock': 120,
                    'image_url': 'https://www.euronics.lv/UserFiles/Products/Images/345387-519121-medium.png'
                },
                {
                    'name': 'USB-C Hub Multiport Adapter',
                    'description': 'Expand your laptop\'s connectivity with multiple ports.',
                    'price': 39.99,
                    'stock': 200,
                    'image_url': 'https://www.euronics.lv/UserFiles/Products/Images/404155-607959-medium.png'
                },
                {
                    'name': 'Portable SSD 1TB',
                    'description': 'Fast and reliable external storage for all your files.',
                    'price': 119.99,
                    'stock': 90,
                    'image_url': 'https://www.euronics.lv/UserFiles/Products/Images/365965-551749-medium.png'
                },
            ]

            for product_data in products_data:
                product = Product(**product_data)
                db.session.add(product)
            db.session.commit()
            print(f"Added {len(products_data)} products to the database.")
        else:
            print("Products already exist in the database. Skipping product seeding.")

if __name__ == '__main__':
    seed_data()