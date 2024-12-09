from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# Flask uygulamasını oluştur ve yapılandır
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Veritabanı dosyasının yolu
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         # Deprecation uyarılarını kapat
db = SQLAlchemy(app)                                         # Veritabanı nesnesi

# Veritabanı modeli tanımla
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)            # Birincil anahtar
    title = db.Column(db.String(80), nullable=False)        # Görev başlığı
    complete = db.Column(db.Boolean, default=False)         # Görev tamamlanma durumu

# Anasayfa rotası
@app.route("/")
def index():
    todos = Todo.query.all()                                # Tüm görevleri al
    return render_template("index.html", todos=todos)

# Görevi tamamlama durumu değiştirme
@app.route("/complete/<int:id>")
def completeTodo(id):
    todo = Todo.query.get_or_404(id)                        # Görevi al veya hata döndür
    todo.complete = not todo.complete                       # Tamamlama durumunu değiştir
    db.session.commit()
    return redirect(url_for("index"))

# Yeni görev ekleme
@app.route("/add", methods=["POST"])
def addTodo():
    title = request.form.get("title")                       # Formdan başlık al
    if title:                                               # Başlık boş değilse ekle
        newTodo = Todo(title=title, complete=False)
        db.session.add(newTodo)
        db.session.commit()
    return redirect(url_for("index"))

# Görev silme
@app.route("/delete/<int:id>")
def deleteTodo(id):
    todo = Todo.query.get_or_404(id)                        # Görevi al veya hata döndür
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

# Ana dosya olarak çalıştırıldığında veritabanını oluştur ve uygulamayı çalıştır
if __name__ == "__main__":
    with app.app_context():                                 # Uygulama bağlamını oluştur
        db.create_all()                                     # Veritabanını oluştur
    app.run(debug=True)                                     # Flask uygulamasını çalıştır
