from flask import Flask, render_template, request, redirect, url_for, session
from utils.produkty import produkty

SESSION_KEY = 'fuifgbuieafh7832h41294o128rg89bfc9A83H289RT3289FBU'

app = Flask(__name__)

# app.secret_key = os.getenv("SESSION_KEY")

app.secret_key = SESSION_KEY

@app.route("/")
def sklep():

    name_list, price_list, image_list = produkty.show_all()


    products = list(zip(name_list, price_list, image_list))


    return render_template('index.html', products=products)


if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=5000,
            debug=True)