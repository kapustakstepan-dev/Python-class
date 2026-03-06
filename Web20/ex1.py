from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

@app.route("/", methods=["GET", "POST"])
def index():
    file_content = None
    
    if request.method == "POST": 
        file = request.files.get("file")
        
        if file and file.filename != '':
            try:
                file_content = file.read().decode("utf-8")
            except UnicodeDecodeError:
                file_content = "Помилка: Файл має бути у кодуванні UTF-8."

    return render_template('index.html', content=file_content)

if __name__ == '__main__':
    app.run(debug=True)