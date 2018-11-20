from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


#Fake categories
category = {'name': 'Football', 'id': '1'}

categories = [{'name': 'Football', 'id': '1'}, {'name':'Baseball', 'id':'2'},{'name':'Tennis', 'id':'3'}]
#categories2 ={};

#Fake Category Items
items = [ {'name':'Ball', 'description':'Addidas ball', 'price':'$80.0', 'id':'1'}, {'name':'Real Madrid uniform','description':'The first Real Madrid uniform for the 2019 season', 'price':'$160','id':'2'},{'name':'Football shoes Nike Olimpus', 'description':' The best performance for the best players','price':'$100', 'id':'3'},{'name':'Jamb Beckembauer', 'description':'made of propileny','price':'$12','id':'4'},{'name':'Nike ball ', 'description':' Soft and endurable','price':'$80', 'id':'5'} ]
item =  {'name':'Ball', 'description':'Addidas ball', 'price':'$80.0', 'id':'1'}
items2 = []

@app.route('/')
@app.route('/catalog', methods=['GET', 'POST'])
def showCategories():
    return render_template('categories.html', categories=categories)



@app.route('/catalog/new')
def newCategory():
    return render_template('newcategory.html')



@app.route('/catalog/<string:category_name>/edit')
def editCategory(category_name):
    return render_template('editcategory.html', category_name=category['name'])


@app.route('/catalog/<string:category_name>/delete')
def deleteCategory(category_name):
    return render_template('deletecategory.html', category_name=category['name'])


@app.route('/catalog/<string:category_name>/items')
def showItems(category_name):
    return render_template('items.html', category_name=category['name'], items=items)


@app.route('/catalog/<string:category_name>/new')
def newItem(category_name):
    return render_template('newitem.html', category_name=category['name'], categories=categories)

@app.route('/catalog/<string:category_name>/<string:item_name>/edit')
def editItem(category_name, item_name):
    return render_template('edititem.html', category_name=category['name'], categories=categories, item=item)


@app.route('/catalog/<string:category_name>/<string:item_name>/delete')
def deleteItem(category_name, item_name):
    return render_template('deleteitem.html', category_name=category['name'], categories=categories, item=item)

@app.route('/catalog/<string:category_name>/<string:item_name>')
def infoItem(category_name, item_name):
    return render_template('item.html', category_name=category['name'], categories=categories, item=item)



if __name__ == '__main__':  # Only will run if the code is execute inside the python interpreter
    app.secret_key = 'super_secret_key'
    app.debug = True
    #app.run(host='0.0.0.0', port = 5000, ssl_context=('cert.pem', 'key.pem'))
    app.run(host='0.0.0.0', port=5000)
