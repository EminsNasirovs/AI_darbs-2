from flask import Blueprint, render_template, redirect, url_for, flash
from models import Product
from database import db
from forms import AddProductForm
from flask_login import current_user, login_required
from functools import wraps

admin_bp = Blueprint('admin', __name__, template_folder='../templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    products = Product.query.all()
    return render_template('admin/dashboard.html', title='Admin Dashboard', products=products)

@admin_bp.route('/add_item', methods=['GET', 'POST'])
@login_required
@admin_required
def add_item():
    form = AddProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            image_url=form.image_url.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_item.html', title='Add New Product', form=form)

@admin_bp.route('/edit_item/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_item(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_item.html', title='Edit Product', form=form, product=product) # Reuse add_item template

@admin_bp.route('/delete_item/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_item(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))