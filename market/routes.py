from market import app
from flask import render_template,redirect,url_for,flash,request
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from market import db
from flask_login import login_user,logout_user,login_required,current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
@login_required
def market_place():
    purchase_form=PurchaseItemForm()
    sell_form=SellItemForm()
    if request.method=="POST":
        #Purchase Item Logic Implementation
        purchased_item=request.form.get('purchased_item')
        p_item_obj=Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.owner=current_user.id
                current_user.budget-=p_item_obj.price
                db.session.commit()
                flash(f'Congratulations! You purchased {p_item_obj.name} for {p_item_obj.price}',category='success')
            else:
                flash(f'Your budget seems to be low to purchase {p_item_obj.name}',category='danger')
        #Sell Item Logic Implementation
        sold_item=request.form.get('sold_item')
        s_item_object=Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.owner=None
                current_user.budget+=s_item_object.price
                db.session.commit()
                flash(f'Congratulations! You sold {s_item_object.name} for {s_item_object.price}',category='success')
            else:
                flash(f'Something went wrong with selling {s_item_object.name}',category='danger')
        return redirect(url_for('market_place'))
    if request.method=="GET":
        items_list=Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items_list,
        purchase_form=purchase_form,owned_items=owned_items,sell_form=sell_form)


@app.route('/base')
def base_layout():
    return render_template('base_layout.html')

@app.route('/register',methods=['GET','POST'])
def Register_Page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,
                            email=form.email.data,
                            password=form.password1.data,
                            budget=form.budget.data
                            )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created succesfully! You are now logged in as {user_to_create.username}',category='success')
        return redirect(url_for('market_place'))
    if form.errors!={}:       #Errors generated is not equal to empty dictionary
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}',category='danger')

    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    login=LoginForm()
    if login.validate_on_submit():
        attempted_user=User.query.filter_by(username=login.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=login.password.data):
            login_user(attempted_user)
            flash(f'Logged In Succesfully! Hello {attempted_user.username}',category='success')
            return redirect(url_for('market_place'))
        else:
            flash('Incorrect Username or Password! Try again',category='danger')
    return render_template('login.html',form=login)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out",category='info')
    return redirect(url_for('home_page'))
if __name__=="__main__":
    app.run(debug=True)
