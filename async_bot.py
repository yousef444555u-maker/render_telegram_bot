from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
os.makedirs('static/uploads', exist_ok=True)

videos = [
    {"url": "https://www.w3schools.com/html/mov_bbb.mp4", "user": "@yousef", "desc": "تجربة مدرسية سرمدا"},
    {"url": "https://www.w3schools.com/html/movie.mp4", "user": "@sarmada", "desc": "تطبيق ريلز بسيط"},
]

@app.route('/')
def home():
    q = request.args.get('q', '').lower()
    filtered = [v for v in videos if q in v['desc'].lower() or q in v['user'].lower()] if q else videos
    return render_template('index.html', videos=filtered)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('video')
    if file:
        path = f"static/uploads/{file.filename}"
        file.save(path)
        videos.insert(0, {"url": f"/{path}", "user": "@yousef", "desc": request.form.get('desc','فيديو جديد')})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
