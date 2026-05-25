from flask import Flask, render_template, request, redirect, url_for, session
from utils.produkty import produkty
from utils.logowanie import logowanie
from utils.koszyk import koszyk
from utils.zakup import zamowienie
from flask import jsonify
from utils.db import db
import datetime

SESSION_KEY = 'fuifgbuieafh7832h41294o128rg89bfc9A83H289RT3289FBU'

app = Flask(__name__)

# app.secret_key = os.getenv("SESSION_KEY")

app.secret_key = SESSION_KEY

@app.route("/")
def sklep():

    products = produkty.show_all()
    return render_template('index.html', products=products)

@app.route("/api/user")
def api_user():
    email = session.get('email')

    return {"email": email}



@app.route("/login", methods=["GET", "POST"])
def login_page():
    msg = ""
    try:
        if request.method == "POST":
            login_val = request.form["login"]
            haslo_val = request.form["haslo"]
            msg, user_id, email = logowanie.zaloguj(login_val, haslo_val)

            if msg == "Zalogowano pomyślnie":

                session['user_id'] = str(user_id)
                session['email'] = email

                return redirect(url_for('sklep'))
    except Exception as e:
        print(e)
        msg = "Blad przy logowaniu. Spróbuj ponownie"
    return render_template("login.html", msg=msg)




@app.route("/register", methods=["GET", "POST"])
def register_page():
    msg=''
    if request.method == "POST":
        try:
            login_val = request.form["login"]
            haslo_val = request.form["haslo"]
            msg = logowanie.zarejestruj(login_val, haslo_val)
        except Exception as e:
            print(e)
            msg = "Blad rejestracji. Spróbuj ponownie"

    
    return render_template("rejestracja.html", msg=msg)


@app.route('/kategorie/<category>', methods=["POST", "GET"])
def kategorie_stronka(category):

    if category == 'dla_ciebie':
        
        pass

    products = produkty.show(category)
    return render_template('kategorie_stronka.html', products=products, category=category)

@app.route('/kupteraz/<product>', methods=["POST", "GET"])
def kupteraz(product):

    name, description, price, active, image = produkty.show_one(product)

    return render_template("kupteraz1.html", name=name,
                            description=description,
                              peice=price,
                                active=active,
                                  image=image
                           )


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for('sklep'))

@app.route('/Koszyczek', methods=['GET', 'POST'])
def koszyczek():
   
    user_id = session.get('user_id') or session.get('email')

    if not user_id:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        data = request.get_json()
        if data.get('value') == 'historia':
            names, prices, quants, image = koszyk.delivered_already(user_id)
        else:
            names, prices, quants, image = koszyk.not_delivered_yet(user_id)
            
        return {"names": names, "prices": prices, "quants": quants, "image": image}

    names, prices, quants, image = koszyk.not_delivered_yet(user_id)

    formatted_products = []
    total_price = 0
    
    if names:
        for i in range(len(names)):
            formatted_products.append({
                "name": names[i],
                "price": prices[i],
                "quantity": quants[i],
                "image": image[i]
            })
            total_price += float(prices[i]) * int(quants[i])
    
    return render_template('koszyk.html', products=formatted_products, total_price=total_price)


@app.route('/finalizuj_zakup', methods=['POST'])
def finalizuj_zakup():
    user_id = session.get('user_id') or session.get('email')
    if not user_id:
        return redirect(url_for('login_page'))

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

  
    db.orders.update_many(
        {"user_id": user_id, "status": "delive"},
        {
            "$set": {
                "status": "completed",
                "created_at": now_str
            }
        }
    )

    return render_template('zakup1.html', message="Dziękujemy za udane zakupy!")


@app.route('/api/koszyk/usun', methods=['POST'])
def usun_z_koszyka():
    user_id = session.get('user_id') or session.get('email')
    if not user_id:
        return jsonify({"error": "Niezalogowany"}), 401

    data = request.get_json()
    product_name = data.get('name')

    db.orders.delete_one({
        "user_id": user_id,
        "status": "delive",
        "items.name": product_name
    })

    return jsonify({"success": True}), 200


@app.route("/zakup", methods=['GET', 'POST'])
def zakup():

    if request.method == 'POST':
        try:
            product_name = request.form.get('product')
            user = session.get('user_id')

            if not product_name:
                return redirect(url_for('sklep'))
                
            if 'user_id' not in session:

                image, price, quantity = zamowienie.check(product_name, None)
                return render_template("zakup1.html",
                                        name=product_name,
                                        image=image,
                                        price=price,
                                        quantity=1)
                    
            else:
                image, price, quantity = zamowienie.check(product_name, user)
                return render_template("zakup1.html",
                                    name=product_name,
                                    image=image,
                                    price=price,
                                    quantity=quantity)

        except Exception as e:
            print(e)

            return redirect(url_for('sklep'))
        
@app.route('/api/user/history', methods=['GET'])
def get_user_history():
    try:
        user_id = session.get('user_id') or session.get('email')
        if not user_id:
            return jsonify({"error": "Niezalogowany", "products": []}), 401

       
        names, prices, quants, image = koszyk.delivered_already(user_id)

        products_history = []
        
      
        if names:
            for i in range(len(names)):
              
                try:
                    p_name = names[i]
                    p_price = prices[i] if i < len(prices) else 0
                    p_quant = quants[i] if i < len(quants) else 1
                    p_img = image[i] if i < len(image) else ""
                    
                    products_history.append({
                        "name": p_name,
                        "price": p_price,
                        "quantity": p_quant,
                        "image": p_img
                    })
                except Exception as inner_e:
                    print(f"Błąd przy pakowaniu produktu indeks {i}: {inner_e}")
                    continue

        return jsonify({"products": products_history}), 200

    except Exception as e:
     
        print(f"BŁĄD BACKENDU HISTORII: {e}")
        return jsonify({"error": str(e), "products": []}), 500


@app.route("/konto")
def konto():
    return render_template('konto.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=5000,
            debug=True)