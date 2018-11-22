from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Category, Item, User
from sqlalchemy.sql import func
import datetime

from flask import session as login_session

app = Flask(__name__)

engine = create_engine('sqlite:///catalogitems.db', connect_args={'check_same_thread':False},poolclass=StaticPool) # Which DB python will communicate with
Base.metadata.bind = engine # Makes connection between class and tables

DBSession = sessionmaker(bind=engine) # Link of communication between our code execution
                                      # and the created engine
session = DBSession() # interefaz that allow to create DB operations



# #Fake categories
# category = {'name': 'Football', 'id': '1'}

# categories = [{'name': 'Football', 'id': '1'}, {'name':'Baseball', 'id':'2'},{'name':'Tennis', 'id':'3'}]
# #categories2 ={};

# #Fake Category Items
# items = [ {'name':'Ball', 'description':'Addidas ball', 'price':'$80.0', 'id':'1'}, {'name':'Real Madrid uniform','description':'The first Real Madrid uniform for the 2019 season', 'price':'$160','id':'2'},{'name':'Football shoes Nike Olimpus', 'description':' The best performance for the best players','price':'$100', 'id':'3'},{'name':'Jamb Beckembauer', 'description':'made of propileny','price':'$12','id':'4'},{'name':'Nike ball ', 'description':' Soft and endurable','price':'$80', 'id':'5'} ]
# item =  {'name':'Ball', 'description':'Addidas ball', 'price':'$80.0', 'id':'1'}
# items2 = []



@app.route('/')
@app.route('/catalog', methods=['GET', 'POST'])
def showCategories():
    
    categories = session.query(Category).order_by(Category.name)
    
    return render_template('categories.html', categories=categories)


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():

    if request.method == 'POST':
        category_new = Category(name=request.form['name'], user_id= 2) #login_session['user_id']
        session.add(category_new)
        session.commit()
        #flash('New Restaurant Created')
        #return redirect(url_for('showCategories'))
        return render_template('newItem.html', category_name=category_new.name)
    else:
        return render_template('newcategory.html')

    



@app.route('/catalog/<string:category_name>/edit', methods=['GET', 'POST'])
def editCategory(category_name):

    category_edit = session.query(Category).filter_by(name=category_name).one()
    #category_edit.name = request.form['name']
    if request.method == 'POST':
        if request.form['name']:
            category_edit.name = request.form['name']
            session.add(category_edit)
            session.commit()
        #flash('Restaurant Successfully Edited')
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category_name=category_edit.name)
    


@app.route('/catalog/<string:category_name>/delete', methods=['GET', 'POST'])
def deleteCategory(category_name):

    category_dele = session.query(Category).filter_by(name=category_name).one()
    if request.method == 'POST':
       
        session.delete(category_dele)
        session.commit()
        #flash('Restaurant Successfully Deleted')
        return redirect(url_for('showCategories'))
    else:
        return render_template('deletecategory.html', category_name=category_dele.name)



    


@app.route('/catalog/<string:category_name>/items')
def showItems(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()


    return render_template('items.html', category_name=category.name, items=items)


@app.route('/catalog/<string:category_name>/new', methods=['GET', 'POST'])
def newItem(category_name):

    category = session.query(Category).filter_by(name=category_name).one()

    if request.method == 'POST':
        item_new = Item(name=request.form['name'], description=request.form['description'], price=request.form['price'], category_id=category.id, user_id=2) # Add user info login_session['email']
        session.add(item_new)
        session.commit()
        #flash('New Menu Item Created')
        return redirect(url_for('showItems',category_name=category.name))
    else:
        return render_template('newItem.html', category_name=category.name)
    

@app.route('/catalog/<string:category_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):

    categories = session.query(Category).order_by(Category.name)
    #print((categories))
    category = session.query(Category).filter_by(name=category_name).one()
    item_edited = session.query(Item).filter((Item.name==item_name) & (Item.category_id==category.id)).one()
    
    if request.method == 'POST':
        if request.form['name']:
            item_edited.name = request.form['name']
            item_edited.date_update = func.now()
        #print("This is name")    
        if request.form['description']:
            item_edited.description = request.form['description']
            item_edited.date_update = func.now()
        #print("This is description")
        if request.form['price']:
            item_edited.price = request.form['price']
            item_edited.date_update = func.now()
        #print("This is price")    
        if request.form['picture']:
            item_edited.picture = request.form['picture']
            item_edited.date_update = func.now()
        #print("This is picture")
       # print(type(request.form['category']))
        if category_name != categories[int(request.form['category'])]:
            item_edited.category = categories[int(request.form['category'])]
            item_edited.date_update = func.now()  
        # print(type(request.form['category']))
        # print("This is category")       
        session.add(item_edited)  
        session.commit()  
        return redirect(url_for('showItems',category_name=category.name))   
    else:
        return render_template('edititem.html', category_name=category.name, item=item_edited, categories=categories)
    
                



    return render_template('edititem.html', category_name=category['name'], categories=categories, item=item)




@app.route('/catalog/<string:category_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):

    category = session.query(Category).filter_by(name=category_name).one()
    item_deleted = session.query(Item).filter((Item.name==item_name) & (Item.category_id==category.id)).one()
    if request.method == 'POST':
        session.delete(item_deleted)
        session.commit()

        return redirect(url_for('showItems',category_name=category.name))   
    
    else:
        return render_template('deleteitem.html', category_name=category.name, item=item_deleted)

@app.route('/catalog/<string:category_name>/<string:item_name>')
def infoItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(name=item_name).all()
    #print("This item is repeated %s times!"%len(items))
    # If there are more than one item name in another category
    if len(items) > 1:
        for i in items:
            if category.id == i.category_id:
                item = i
    else:
        item = items
    return render_template('item.html', category_name=category_name, item=item)

# Methods for getting user information
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user
    


def createUser(login_session):
    newUser = User(name=login_session['username'], email=
        login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':  # Only will run if the code is execute inside the python interpreter
    app.secret_key = 'super_secret_key'
    app.debug = True
    #app.run(host='0.0.0.0', port = 5000, ssl_context=('cert.pem', 'key.pem'))
    app.run(host='0.0.0.0', port=5000)
