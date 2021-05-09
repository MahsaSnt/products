from flask import Flask, request, jsonify
from flask_cors import CORS
#from my own code
from digikala import all_digikala, incredible_digikala, special_digikala
from digistyle import all_digistyle, special_digistyle
from timcheh import all_timcheh, special_timcheh, incredible_timcheh
from emalls import all_emalls, special_emalls,shoplist_emalls
# from torob import output_5
# from tagmond import output_6
from banimode import all_banimode, special_banimode, incredible_banimode

app=Flask(__name__)
CORS(app)

@app.route('/api/digikala/all',methods=['POST'])
def digikala1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_digikala(num_pages,subject)
    return jsonify(products= f"{products}")

@app.route('/api/digikala/incredible',methods=['POST'])
def digikala2():
    data = request.get_json()
    get_data = data["get_data"]
    products = incredible_digikala()
    return jsonify(products= f"{products}")

@app.route('/api/digikala/special',methods=['POST'])
def digikala3():
    data = request.get_json()
    num_pages = data["num_pages"]
    products = special_digikala(num_pages)
    return jsonify(products= f"{products}")

@app.route('/api/digistyle/all',methods=['POST'])
def digistyle1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_digistyle(num_pages,subject)
    return jsonify(products= f"{products}")  

@app.route('/api/digistyle/special',methods=['POST'])
def digistyle2():
    data = request.get_json()
    num_pages = data["num_pages"]
    products = special_digistyle(num_pages)
    return jsonify(products= f"{products}")       

@app.route('/api/timcheh/all',methods=['POST'])
def timche1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_timcheh(num_pages,subject)
    return jsonify(products= f"{products}")   

@app.route('/api/timcheh/special',methods=['POST'])
def timche2():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = special_timcheh(num_pages,subject)
    return jsonify(products= f"{products}")   

@app.route('/api/timcheh/incredible',methods=['POST'])
def timche3():
    data = request.get_json()
    get_data = data["get_data"]
    products = incredible_timcheh()
    return jsonify(products= f"{products}")   

@app.route('/api/emalls/all',methods=['POST'])
def emalls1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_emalls(num_pages,subject)
    return jsonify(products= f"{products}") 

@app.route('/api/emalls/special',methods=['POST'])
def emalls2():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_emalls(num_pages,subject)
    return jsonify(products= f"{products}")     

@app.route('/api/emalls/shoplist',methods=['POST'])
def emalls3():
    data = request.get_json()
    shoplist = data["shoplist"]
    products = shoplist_emalls(shoplist)
    return jsonify(products= f"{products}")         


@app.route('/api/banimode/all',methods=['POST'])
def banimode1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_banimode(num_pages,subject)
    return jsonify(products= f"{products}") 


@app.route('/api/banimode/special',methods=['POST'])
def banimode2():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = special_banimode(num_pages,subject)
    return jsonify(products= f"{products}") 

@app.route('/api/banimode/incredible',methods=['POST'])
def banimode3():
    data = request.get_json()
    get_data = data["get_data"]
    products = incredible_banimode()
    return jsonify(products= f"{products}") 


# @app.route('/api/torob',methods=['POST'])
# def torob():
#     data = request.get_json()
#     subject = data["subject"]
#     num_items = data["num_items"]
#     products = output_5(num_items,subject)
#     return jsonify(products= f"{products}")   

# @app.route('/api/tagmond',methods=['POST'])
# def tagmond():
#     data = request.get_json()
#     subject = data["subject"]
#     num_pages = data["num_pages"]
#     products = output_6(num_pages,subject)
#     return jsonify(products= f"{products}")           
if __name__ == '__main__':
    app.run(debug=True)
    