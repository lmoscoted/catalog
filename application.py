from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def showCategories():
    return "These are all categories!"


@app.route('/catalog/new')
def newCategory():
    return "Creating a new Category!"


@app.route('/catalog/<string:category_name>/edit')
def editCategory(category_name):
    return "Editing a Category!"


@app.route('/catalog/<string:category_name>/delete')
def deleteCategory(category_name):
    return "Deleting Category!"


@app.route('/catalog/<string:category_name>/items')
def showItems(category_name):
    return "Items for the category %s" % category_name


@app.route('/catalog/<string:category_name>/new')
def newItem(category_name, item_name):
    return "Item  added!"

@app.route('/catalog/<string:category_name>/<string:item_name>/edit')
def editItem(category_name, item_name):
    return " Editing %s from the %s categroy" % (item_name, category_name)


@app.route('/catalog/<string:category_name>/<string:item_name>/delete')
def deleteItem(category_name, item_name):
    return " Deleting %s from the %s categroy" % (item_name, category_name)

@app.route('/catalog/<string:category_name>/<string:item_name>')
def infoItem(category_name, item_name):
    return " This is a description of %S" % (item_name)



if __name__ == '__main__':  # Only will run if the code is execute inside the python interpreter
    app.secret_key = 'super_secret_key'
    app.debug = True
    #app.run(host='0.0.0.0', port = 5000, ssl_context=('cert.pem', 'key.pem'))
    app.run(host='0.0.0.0', port=5000)
