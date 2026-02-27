from flask import Flask, render_template_string, request

app = Flask(__name__, template_folder='.')

HTML = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; padding: 50px; background: #f4f4f4; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        input { padding: 10px; border: 1px solid #ddd; border-radius: 5px; width: 200px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <form method="POST">
            <input type="text" name="data" placeholder="Текст для QR..." required>
            <button type="submit">OK</button>
        </form>
        {% if url %}
            <div style="margin-top:20px;">
                <img src="{{ url }}">
                <p>{{ text }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    url = None
    text = None
    
    if request.method == 'POST':
        text = request.form.get('data')

        url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text}"
    
    return render_template_string(HTML, url=url, text=text)

if __name__ == '__main__':
    app.run(port=5000, debug=True)