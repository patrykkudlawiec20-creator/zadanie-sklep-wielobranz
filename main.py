from flask import Flask, render_template, request, redirect, url_for, session
from utils.produkty import produkty
from utils.logowanie import logowanie

SESSION_KEY = 'fuifgbuieafh7832h41294o128rg89bfc9A83H289RT3289FBU'

app = Flask(__name__)

# app.secret_key = os.getenv("SESSION_KEY")

app.secret_key = SESSION_KEY

@app.route("/")
def sklep():

    name_list, price_list, image_list = produkty.show_all()


    products = list(zip(name_list, price_list, image_list))


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





if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=5000,
            debug=True)