import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect, CSRFError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='.')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

csrf = CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mensajes = request.form.get('mensaje')
        return f"Захист спрацював! Повідомлення отримано: {mensajes}"
    
    return render_template('index.html')

@app.errorhandler(CSRFError)
def csrf_error(e):
    return f"Помилка CSRF: {e.description}, запит відхилено!", 400

if __name__ == '__main__':
    app.run(debug=True)