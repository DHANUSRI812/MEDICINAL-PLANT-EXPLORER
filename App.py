from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import datetime
import mysql.connector
import sys
import pickle
import warnings
import datetime
import cv2
import numpy as np
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify
from requests import get


english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch'
                          },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'




@app.route("/ask", methods=['GET', 'POST'])
def ask():
    message = str(request.form['messageText'])
    bott = ''
    bott1 = ''
    sresult1 = ''

    bot_response = english_bot.get_response(message)

    print(bot_response)

    while True:

        if bot_response.confidence > 0.5:

            bot_response = str(bot_response)
            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

        elif message == ("bye") or message == ("exit"):

            bot_response = 'Hope to see you soon' + '<a href="http://127.0.0.1:5000">Exit</a>'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

            break

        else:

            try:
                url = "https://en.wikipedia.org/wiki/" + message
                page = get(url).text
                soup = BeautifulSoup(page, "html.parser")
                p = soup.find_all("p")
                return jsonify({'status': 'OK', 'answer': p[1].text})



            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'

                print(bot_response)
                return jsonify({'status': 'OK', 'answer': bot_response})




@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')

@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')




@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('AdminHome.html',data=data)



@app.route("/UserHome")
def UserHome():
    user = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + user + "'")
    data = cur.fetchall()
    return render_template('UserHome.html',data=data)



@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
       if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

           conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
           # cursor = conn.cursor()
           cur = conn.cursor()
           cur.execute("SELECT * FROM regtb ")
           data = cur.fetchall()
           flash('You are Logged In...!')
           return render_template('AdminHome.html' , data=data)

       else:
        flash('Username Or Password is Wrong...!')
        return render_template('AdminLogin.html', error=error)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            print("hai")
            flash('Username Or Password is Wrong...!')
            return render_template('UserLogin.html')



        else:
         print(data[0])
         session['uid'] = data[0]

         conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
         # cursor = conn.cursor()
         cur = conn.cursor()
         cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
         data = cur.fetchall()
         flash('You are Logged In...!')
         return render_template('UserHome.html', data=data)






@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':

        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'


    return render_template('UserLogin.html')




@app.route("/AdminAinfo")
def AdminAinfo():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where  DResult !='waiting'")
    data = cur.fetchall()


    return render_template('AdminAnswer.html', data=data )




@app.route("/EntreLogin")
def EntreLogin():
    return render_template('EntreLogin.html')

@app.route("/NewEntre")
def NewEntre():
    return render_template('NewEntre.html')



@app.route("/newentre", methods=['GET', 'POST'])
def newentre():
    if request.method == 'POST':

        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO enttb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'


    return render_template('EntreLogin.html')



@app.route("/entrelogin", methods=['GET', 'POST'])
def entrelogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['ename'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from enttb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            print("hai")
            flash('Username Or Password is Wrong...!')
            return render_template('EntreLogin.html')




        else:
         print(data[0])
         session['uid'] = data[0]

         conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
         # cursor = conn.cursor()
         cur = conn.cursor()
         cur.execute("SELECT * FROM enttb where username='" + username + "' and Password='" + password + "'")
         data = cur.fetchall()
         flash('You are Logged In...!')
         return render_template('EntreHome.html', data=data)




@app.route("/EntreHome")
def EntreHome():
    user = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM enttb where username='" + user + "'")
    data = cur.fetchall()
    return render_template('EntreHome.html',data=data)



@app.route("/Predict")
def Predict():
    return render_template('Predict.html')



@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':


        file = request.files['fileupload']
        file.save('static/Out/Test.jpg')

        img = cv2.imread('static/Out/Test.jpg')
        if img is None:
            print('no data')

        img1 = cv2.imread('static/Out/Test.jpg')
        print(img.shape)
        img = cv2.resize(img, ((int)(img.shape[1] / 5), (int)(img.shape[0] / 5)))
        original = img.copy()
        neworiginal = img.copy()
        cv2.imshow('original', img1)
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        img1S = cv2.resize(img1, (960, 540))

        cv2.imshow('Original image', img1S)
        grayS = cv2.resize(gray, (960, 540))
        cv2.imshow('Gray image', grayS)

        gry = 'static/Out/gry.jpg'

        cv2.imwrite(gry, grayS)
        from PIL import  ImageOps,Image

        im = Image.open(file)

        im_invert = ImageOps.invert(im)
        inv = 'static/Out/inv.jpg'
        im_invert.save(inv, quality=95)

        dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
        cv2.imshow("Nosie Removal", dst)
        noi = 'static/Out/noi.jpg'

        cv2.imwrite(noi, dst)

        import warnings
        warnings.filterwarnings('ignore')
        import os
        import tensorflow as tf
        classifierLoad = tf.keras.models.load_model('leafmodel.h5')

        import numpy as np
        from keras.preprocessing import image

        base_dir = 'Data/'
        catgo = os.listdir(base_dir)

        test_image = image.load_img('Output/Out/Test.jpg', target_size=(200, 200))
        img1 = cv2.imread('Output/Out/Test.jpg')
        # test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)
        ind = np.argmax(result)

        print(catgo[ind])

        out = ''
        pre = ''
        predicted_class = catgo[ind]

        out = ''
        fer = ''
        if predicted_class == "Alpinia Galanga (Rasna)":
            out = "Alpinia_Galanga_(Rasna)"
            uses = "Treating rheumatism, inflammatory disorders, coughs, colds, fever, muscle spasms, intestinal gas, swelling, killing bacteria, stimulating digestion and appetite, purgative, relaxing muscles, reducing pain and inflammation, detoxification."

        elif predicted_class == "Amaranthus Viridis (Arive-Dantu)":
            out = "Amaranthus_Viridis_(Arive-Dantu)"
            uses = "Antipyretic, anti-inflammatory, used for ulcer, diabetes, asthma, and hyperlipidemia in Ayurvedic medicine."

        elif predicted_class == "Artocarpus Heterophyllus (Jackfruit)":
            out = "Artocarpus_Heterophyllus_(Jackfruit)"
            uses = "Anticarcinogenic, antimicrobial, antifungal, anti-inflammatory, wound healing, and hypoglycemic effects."

        elif predicted_class == "Azadirachta Indica (Neem)":
            out = "Azadirachta_Indica_(Neem)"
            uses = "Treats dental and gastrointestinal disorders, malaria fevers, skin diseases, insect repellent, diuretic, diabetes, headache, heartburn, appetite stimulant."

        elif predicted_class == "Basella Alba (Basale)":
            out = "Basella_Alba_(Basale)"
            uses = "Boosts testosterone in males, safe laxative in pregnancy and children, used for urticaria, burns, and scalds."

        elif predicted_class == "Brassica Juncea (Indian Mustard)":
            out = "Brassica_Juncea_(Indian_Mustard)"
            uses = "Rich in glucosinolates, used for cooking and medicinal properties."

        elif predicted_class == "Carissa Carandas (Karanda)":
            out = "Carissa_Carandas_(Karanda)"
            uses = "Treats acidity, indigestion, wounds, skin diseases, urinary disorders, diabetic ulcer, stomach pain, anemia, and more."

        elif predicted_class == "Citrus Limon (Lemon)":
            out = "Citrus_Limon_(Lemon)"
            uses = "Weight loss, reduces risk of heart disease, anemia, kidney stones, digestive issues, and cancer."

        elif predicted_class == "Ficus Auriculata (Roxburgh fig)":
            out = "Ficus_Auriculata_(Roxburgh_fig)"
            uses = "Treats diarrhea, wounds, edible fruit, used for mumps, cholera, vomiting."

        elif predicted_class == "Ficus Religiosa (Peepal Tree)":
            out = "Ficus_Religiosa_(Peepal_Tree)"
            uses = "Antiulcer, antibacterial, antidiabetic, treats gonorrhea and skin diseases."

        elif predicted_class == "Hibiscus Rosa-sinensis":
            out = "Hibiscus_Rosa-sinensis"
            uses = "Used in teas, herbal medicine for hypertension, cholesterol, and cancer progression."

        elif predicted_class == "Jasminum (Jasmine)":
            out = "Jasminum_(Jasmine)"
            uses = "Used to flavor beverages, desserts, candy, baked goods, gelatins, and puddings."

        elif predicted_class == "Mangifera Indica (Mango)":
            out = "Mangifera_Indica_(Mango)"
            uses = "Restorative tonic, used for heat stroke, asthma, astringent, relief from hiccups and throat affections."

        elif predicted_class == "Mentha (Mint)":
            out = "Mentha_(Mint)"
            uses = "Antimicrobial, carminative, stimulant, antispasmodic, treats headaches and digestive disorders."

        elif predicted_class == "Moringa Oleifera (Drumstick)":
            out = "Moringa_Oleifera_(Drumstick)"
            uses = "Treats edema, liver protection, cancer prevention, stomach issues, bacterial infections, diabetes, bone health, skin health, erectile dysfunction."

        elif predicted_class == "Muntingia Calabura (Jamaica Cherry-Gasagase)":
            out = "Muntingia_Calabura_(Jamaica_Cherry-Gasagase)"
            uses = "Anti-inflammatory, antipyretic, antiulcer, antidiabetic, antihypertensive, cardioprotective, antibacterial, insecticidal properties."

        elif predicted_class == "Nerium Oleander (Oleander)":
            out = "Nerium_Oleander_(Oleander)"
            uses = "Treats heart failure, asthma, corns, cancer, diabetes, epilepsy, has antibacterial, antiviral, immune-boosting properties."

        elif predicted_class == "Nyctanthes Arbor-tristis (Parijata)":
            out = "Nyctanthes_Arbor-tristis_(Parijata)"
            uses = "Treats fevers, cough, arthritis, worm infestation, constipation."

        elif predicted_class == "Ocimum Tenuiflorum (Tulsi)":
            out = "Ocimum_Tenuiflorum_(Tulsi)"
            uses = "Used in sanitizers, mouthwash, water purification, wound healing, herbal preservation, and traveler’s health."

        else:
            out = "Unknown Plant"
            uses = "No information available."

        print(f"Plant: {out}\nUses: {uses}")

        org = 'static/Out/Test.jpg'
        gry ='static/Out/gry.jpg'
        inv = 'static/Out/inv.jpg'
        noi = 'static/Out/noi.jpg'


        return render_template('Predict.html',fer=uses,result=out,org=org,gry=gry,inv=inv,noi=noi)



@app.route("/NewSeed")
def NewSeed():
    return render_template('NewSeed.html')



@app.route("/newseed", methods=['GET', 'POST'])
def newseed():
    if request.method == 'POST':
        ename = session['ename']

        sname = request.form['sname']
        info = request.form['info']
        file = request.files['file']
        file.save("static/uploads/" + file.filename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO seedtb VALUES ('','" + sname + "','" + ename + "','" + info + "','" + file.filename + "','Waiting')")
        conn.commit()
        conn.close()
        # return 'file register successfully'


    return render_template('NewSeed.html')


@app.route("/ESeedInfo")
def ESeedInfo():
    user = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Ename='" + user + "'")
    data = cur.fetchall()
    return render_template('ESeedInfo.html',data=data)



@app.route("/ASeedInfo")
def ASeedInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Waiting'")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Accepted'")
    data1 = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Rejected'")
    data2 = cur.fetchall()
    return render_template('ASeedInfo.html', data=data, data1=data1, data2=data2)


@app.route("/Reject")
def Reject():
    id = request.args.get('id')


    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute(
        "update seedtb set Status='Rejected' where sid='" + id + "'")
    conn.commit()
    conn.close()
    flash('Player Application is Rejected...!')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Waiting'")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Accepted'")
    data1 = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Rejected'")
    data2 = cur.fetchall()
    return render_template('ASeedInfo.html',data=data, data1=data1,data2=data2)


@app.route("/Accept")
def Accept():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute(
        "update seedtb set Status='Accepted' where sid='" + id + "'")
    conn.commit()
    conn.close()
    flash('Player Application is Accepted...!')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Waiting'")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Accepted'")
    data1 = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM seedtb where Status='Rejected'")
    data2 = cur.fetchall()
    return render_template('ASeedInfo.html',data=data, data1=data1, data2=data2)



@app.route("/NewProduct")
def NewProduct():
    uname = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT distinct Sname FROM seedtb where Ename='" + uname + "' and Status='Accepted'")
    data = cur.fetchall()
    return render_template('NewProduct.html',data=data)


@app.route("/EProductInfo")
def EProductInfo():
    uname = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM producttb where Ename='" + uname + "'")
    data = cur.fetchall()
    return render_template('EProductInfo.html',data=data)


@app.route("/newproduct", methods=['GET', 'POST'])
def newproduct():
    if request.method == 'POST':
        pname = request.form['pname']
        ptype = request.form['ptype']
        price = request.form['price']
        qty = request.form['qty']
        session['quanty'] = request.form['qty']
        ben = request.form['ben']

        info = request.form['info']
        file = request.files['file']
        file.save("static/uploads/" + file.filename)
        #size = request.form['size']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO producttb VALUES ('','" + pname + "','" + ptype + "','" + price + "','" + qty + "','" + info + "','" + file.filename + "','nil','" + ben + "','"+ session['ename'] +"')")
        conn.commit()
        conn.close()

    flash('New Product Added successfully')
    return render_template('NewProduct.html')


@app.route("/ARemove")
def ARemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from producttb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Product  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM producttb  ")
    data = cur.fetchall()
    return render_template('EProductInfo.html',data=data)


@app.route("/USearch")
def USearch():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT distinct Sname FROM seedtb where Status='Accepted'")
    data1 = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM producttb")
    data = cur.fetchall()
    return render_template('USearch.html',data=data,data1=data1)

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ptype = request.form['ptype']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM producttb where  ProductType ='" + ptype + "'")
        data = cur.fetchall()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cur = conn.cursor()
        cur.execute("SELECT distinct Sname FROM seedtb where Status='Accepted'")
        data1 = cur.fetchall()
        return render_template('USearch.html', data=data,data1=data1)



@app.route("/Add")
def Add():
    id = request.args.get('id')
    session['pid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM producttb  where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('AddCart.html', data=data)



@app.route("/addcart", methods=['GET', 'POST'])
def addcart():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        pid = session['pid']
        uname = session['uname']
        qty = int(request.form['qty'])

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM regtb  where  UserName='" + uname + "'")
        user = cursor.fetchone()

        if user:
            mob = user[2]
            add = user[4]

        else:
            return 'No Record Found!'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM producttb  where  id='" + pid + "'")
        data = cursor.fetchone()

        if data:
            Productid = data[0]
            ProductName = data[1]
            Producttype = data[2]
            price = data[3]
            quanty = int(data[4])
            Image = data[6]

        else:
            return 'No Record Found!'
        if quanty >= qty:

            quanty = quanty - qty

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
            cursor = conn.cursor()
            cursor.execute(
                "update producttb set Quantity='"+ str(quanty) +"' where id='" + pid + "' ")
            conn.commit()
            conn.close()

            tprice = float(price) * float(qty)
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO carttb VALUES ('','" + uname + "','" + ProductName + "','" + Producttype + "','" + str(
                    price) + "','" + str(qty) + "','" + str(tprice) + "','" +
                Image + "','" + date + "','0','','" + mob + "','" + add + "', 'waiting','"+ str(Productid) +"','Waiting')")
            conn.commit()
            conn.close()

            flash('Add To Cart  Successfully')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM producttb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)
        else:
            flash("Out Of Stock...!")
            return render_template('USearch.html')

@app.route("/Cart")
def Cart():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' and Approvestatus='Accepted'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' and Approvestatus='Accepted'")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]
    else:
        return 'No Record Found!'

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)

@app.route("/RemoveCart")
def RemoveCart():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from carttb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product Remove Successfully!')

    uname = session['username']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)

@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        uname = session['uname']
        cname = request.form['cname']
        Cardno = request.form['cno']
        Cvno = request.form['cvno']

        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
        pro = cur.fetchone()
        if pro:
            productid = pro[14]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
        data1 = cursor.fetchone()
        if data1:
            tqty = data1[0]
            tprice = data1[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) As count  FROM booktb ")
        data = cursor.fetchone()
        if data:
            bookno = data[0]
            print(bookno)

            if bookno == 'Null' or bookno == 0:
                bookno = 1
            else:
                bookno += 1

        else:
            return 'Incorrect username / password !'

        bookno = 'BOOKID' + str(bookno)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "update  carttb set status='1',Bookid='" + bookno + "' where UserName='" + uname + "' and Status='0' ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + uname + "','" + bookno + "','" + str(tqty) + "','" + str(
                tprice) + "','" + cname + "','" + Cardno + "','" + Cvno + "','" + date + "','"+ str(productid) +"','nil')")
        conn.commit()
        conn.close()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
        data1 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
        data2 = cur.fetchall()
        flash("Payment Successful....!")

    return render_template('UBookInfo.html', data1=data1, data2=data2)

@app.route("/UBookInfo")
def UBookInfo():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "' and Image!='nil'")
    data2 = cur.fetchall()
    return render_template('UBookInfo.html', data1=data1, data2=data2)


@app.route("/ABookInfo")
def ABookInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb")
    data1 = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb")
    data2 = cur.fetchall()
    return render_template('ABookInfo.html', data1=data1, data2=data2)



@app.route("/AViewRequest")
def AViewRequest():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb Where Approvestatus='Waiting' ")
    data = cur.fetchall()
    return render_template('AViewRequest.html', data=data)





@app.route("/AReject")
def AReject():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute(
        "update carttb set Approvestatus='Rejected' where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('House Request Rejected...!')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM carttb where Status='waiting'")
    data = cur.fetchall()
    return render_template('AViewRequest.html',data1=data)


@app.route("/AAccept")
def AAccept():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute(
        "update carttb set Approvestatus='Accepted' where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('House Request Accepted...!')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM carttb where Status='waiting'")
    data = cur.fetchall()
    return render_template('AViewRequest.html', data1=data)




@app.route("/Chat")
def Chat():
    return render_template('chat.html')


@app.route("/EBookInfo")
def EBookInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb")
    data1 = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb")
    data2 = cur.fetchall()
    return render_template('EBookInfo.html', data1=data1, data2=data2)



@app.route("/ESlip")
def ESlip():
    id = request.args.get('id')
    session['pid'] = id
    return render_template('ESlip.html')



@app.route("/Update",methods=['GET', 'POST'])
def Update():
    if request.method == 'POST':

        file = request.files['file']
        file.save("static/uploads/" + file.filename)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cursor = conn.cursor()
        cursor.execute(
            "update booktb set Image='" + file.filename + "' where id='" + str(session['pid']) + "' ")
        conn.commit()
        conn.close()
        flash('Product  info Updated   Successfully!')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM booktb  ")
        data2 = cur.fetchall()
        return render_template('EBookInfo.html', data2=data2)


@app.route('/download')
def download():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1herbalclassifydb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM booktb where  id = '" + str(id) + "'")
    data = cursor.fetchone()
    if data:
        filename = "static\\uploads\\"+data[10]
        return send_file(filename, as_attachment=True)
    else:
        return 'Incorrect username / password !'



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)