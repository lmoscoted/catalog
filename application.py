from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Category, Item, User
from sqlalchemy.sql import func
import datetime

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import *
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response
from flask import session as login_session
import random, string

app = Flask(__name__)

# Google Client ID 
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
print(CLIENT_ID)

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


# Login page with Anti forgery Atack.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)



#handle the code sent back from the callback method   
@app.route('/gconnect', methods=['POST'])
def gconnect():
    print("BEGIN HERE")
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data  
    print("SECOND TRACE")
    try:
    # Upgrade the authorized code into a credentials object  
        print("THIRD TRACE")
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        print("FOUR TRACE")
        oauth_flow.redirect_uri = 'postmessage'
        print("FIFTH TRACE")
        credentials = oauth_flow.step2_exchange(code)
        print("SIXTH TRACE")

    except FlowExchangeError:
        print("SEVENTH TRACE")
        response = make_response(json.dumps('Failed to upgrade the authorization code. '), 401)
        print("EIGTH TRACE")
        response.headers['Content-Type'] = 'application/json'
        print("NINE TRACE")
        print('Failed to upgrade the authorization code. ')
        return response
    # Check that the access token is valid.
    print("THIRD TRACE")
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])   
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is used for intended use
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's ."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check to see if the user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected. "), 200)
        response.headers['Content-Type'] = 'application/json'
    
    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id


    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data['email']

    # See if user exists, if it does not make a new one
    
    #user_db = session.query(User).filter_by(email=).one()

    if getUserID(login_session['email']) == None:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id

    login_session['user_id'] = getUserID(login_session['email'])




    output = ''
    output += '<h1> Welcome, '
    output += login_session['username']

    output += '!<h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px;-moz-border-radius: 150px; ">'
    flash("you are now logged in as %s "%login_session['username'])
    return  output


# DISCONNECT - Revoke a current user's token and reset their
#login_session
@app.route('/gdisconnect')
def gdisconnect():
    #Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Execute HTTP GET request to revoke current token    
    # print 'In gdisconnect access token is %s', access_token
    # print 'User name is: '
    # print login_session['username']
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    
    if result['status'] == '200':
    #     #Reset the user's session
    #     del login_session['credentials']
    #     del login_session['gplus_id']
    #     del login_session['username']
    #     del login_session['email']
    #     del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
       #For whatever reason, the given token was invalid
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# DISCONNECT function for any provider
@app.route('/disconnect')
def disconnect():

    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook']
    
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have Successfully been logged out. ")
        return redirect(url_for('showCategories'))
    else:
        flash("You are not logged in to begin with!")
        redirect(url_for('showCategories'))

@app.route('/')
@app.route('/catalog', methods=['GET', 'POST'])
def showCategories():
    
    categories = session.query(Category).order_by(Category.name)
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories, login_session=login_session)
        

    #return render_template('publiccategories.html', categories=categories)


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():

    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        category_new = Category(name=request.form['name'], user_id= getUserID(login_session['email'])) #login_session['user_id']
        session.add(category_new)
        session.commit()
        #flash('New Restaurant Created')
        #return redirect(url_for('showCategories'))
        return render_template('newItem.html', category_name=category_new.name)
    else:
        return render_template('newcategory.html')

    



@app.route('/catalog/<string:category_name>/edit', methods=['GET', 'POST'])
def editCategory(category_name):

    if 'username' not in login_session:
        return redirect('/login')

    category_edit = session.query(Category).filter_by(name=category_name).one()

    if category_edit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are no authorized to edit this category. Please create a new category in order to edit');location.href='/catalog';}</script><body onload='myFunction()''>"
    

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

    if 'username' not in login_session:
        return redirect('/login')

    category_dele = session.query(Category).filter_by(name=category_name).one()
    items_dele = session.query(Item).filter_by(category_id=category_dele.id).all()    


    if category_dele.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are no authorized to delete this category. Please access to your own category in order to delete');location.href='/catalog';}</script><body onload='myFunction()''>"
    
    if request.method == 'POST':
       
        session.delete(category_dele)

        for i in items_dele:
            session.delete(i)
        session.commit()
        #flash('Restaurant Successfully Deleted')
        return redirect(url_for('showCategories'))
    else:
        return render_template('deletecategory.html', category_name=category_dele.name)



    


@app.route('/catalog/<string:category_name>/items')
def showItems(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()

    if not items:
        return "<script>function myFunction() {alert('This category do not have items yet. Please add new items for this category');location.href='/catalog/%s/new';}</script><body onload='myFunction()''>" % category_name
    
    if 'username' not in login_session:
        return render_template('publicitems.html', category_name=category.name, items=items)

    else:    
        return render_template('items.html', category_name=category.name, items=items)
    #return render_template('publicitems.html', category_name=category.name, items=items)


@app.route('/catalog/<string:category_name>/new', methods=['GET', 'POST'])
def newItem(category_name):

    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(name=category_name).one()

   # Anybody can add an item to any category
    if request.method == 'POST':
        item_new = Item(name=request.form['name'], description=request.form['description'], price=request.form['price'], category_id=category.id, user_id= getUserID(login_session['email'])) # Add user info login_session['email']
        session.add(item_new)
        session.commit()
        #flash('New Menu Item Created')
        return redirect(url_for('showItems',category_name=category.name))
    else:
        return render_template('newItem.html', category_name=category.name)
    

@app.route('/catalog/<string:category_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):

    if 'username' not in login_session:
        return redirect('/login')

    categories = session.query(Category).order_by(Category.name)
    #print((categories))
    category = session.query(Category).filter_by(name=category_name).one()
    item_edited = session.query(Item).filter((Item.name==item_name) & (Item.category_id==category.id)).one()

    if item_edited.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are no authorized to edit this item.');location.href='/catalog/%s/items';}</script><body onload='myFunction()''>" % category_name
    
    
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

    if 'username' not in login_session:
        return redirect('/login')


    category = session.query(Category).filter_by(name=category_name).one()
    item_deleted = session.query(Item).filter((Item.name==item_name) & (Item.category_id==category.id)).one()

    if item_deleted.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are no authorized to delete this item.');location.href='/catalog/%s/items';}</script><body onload='myFunction()''>" % category_name
    



    if request.method == 'POST':
        session.delete(item_deleted)
        session.commit()

        return redirect(url_for('showItems',category_name=category.name))   
    
    else:
        return render_template('deleteitem.html', category_name=category.name, item=item_deleted)

@app.route('/catalog/<string:category_name>/<string:item_name>')
def infoItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter((Item.name==item_name) & (Item.category_id == category.id)).one()

    if 'username' not in login_session:
        return render_template('publicitem.html', category_name=category_name, item=item)


    #print("This item is repeated %s times!"%len(items))
    # If there are more than one item name in another category
    # if len(items) > 1:
    #     for i in items:
    #         if category.id == i.category_id:
    #             item = i
    # else:
    #     item = items
    #return render_template('item.html', category_name=category_name, item=item)
    

    else: 
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
