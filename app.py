from flask import Flask, render_template_string, request, redirect
from models import db, InventoryItem
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    inventory = InventoryItem.query.all()
    alerts = [item for item in inventory if item.quantity <= 3]
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>在庫管理アプリ</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="container mt-4">
        <h1 class="mb-4">在庫管理アプリ</h1>

        <form method="POST" action="/add" class="row g-3">
            <div class="col-md-3">
                <input type="text" name="item_name" class="form-control" placeholder="商品名" required>
            </div>
            <div class="col-md-2">
                <input type="number" name="quantity" class="form-control" placeholder="数量" required>
            </div>
            <div class="col-md-2">
                <input type="number" name="unit_price" class="form-control" placeholder="単価" required>
            </div>
            <div class="col-md-3">
                <input type="date" name="purchase_date" class="form-control" required>
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-success">追加</button>
            </div>
        </form>

        <h2 class="mt-5">在庫一覧</h2>
        <table class="table table-striped table-bordered mt-3">
            <thead class="table-light">
                <tr>
                    <th>商品名</th>
                    <th>数量</th>
                    <th>単価</th>
                    <th>仕入れ日</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                {% for item in inventory %}
                <tr>
                    <td>{{ item.item_name }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ item.unit_price }}</td>
                    <td>{{ item.purchase_date }}</td>
                    <td>
                        <a href="/edit/{{ item.id }}" class="btn btn-sm btn-primary">編集</a>
                        <a href="/delete/{{ item.id }}" class="btn btn-sm btn-danger" onclick="return confirm('本当に削除しますか？');">削除</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        {% if alerts %}
        <div class="alert alert-warning mt-4">
            <h4>在庫アラート！</h4>
            <ul>
                {% for item in alerts %}
                    <li>{{ item.item_name }} が少なくなっています（残り {{ item.quantity }} 個）</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </body>
    </html>
    """, inventory=inventory, alerts=alerts)

@app.route('/add', methods=['POST'])
def add():
    item = InventoryItem(
        item_name=request.form['item_name'],
        quantity=int(request.form['quantity']),
        unit_price=int(request.form['unit_price']),
        purchase_date=date.fromisoformat(request.form['purchase_date'])
    )
    db.session.add(item)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = InventoryItem.query.get_or_404(id)
    if request.method == 'POST':
        item.item_name = request.form['item_name']
        item.quantity = int(request.form['quantity'])
        item.unit_price = int(request.form['unit_price'])
        item.purchase_date = date.fromisoformat(request.form['purchase_date'])
        db.session.commit()
        return redirect('/')
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>在庫編集</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="container mt-4">
        <h2>在庫編集</h2>
        <form method="POST" class="row g-3">
            <div class="col-md-4">
                <input type="text" name="item_name" class="form-control" value="{{ item.item_name }}" required>
            </div>
            <div class="col-md-2">
                <input type="number" name="quantity" class="form-control" value="{{ item.quantity }}" required>
            </div>
            <div class="col-md-2">
                <input type="number" name="unit_price" class="form-control" value="{{ item.unit_price }}" required>
            </div>
            <div class="col-md-3">
                <input type="date" name="purchase_date" class="form-control" value="{{ item.purchase_date }}" required>
            </div>
            <div class="col-md-1">
                <button type="submit" class="btn btn-primary">更新</button>
            </div>
        </form>
        <a href="/" class="btn btn-link mt-3">← 戻る</a>
    </body>
    </html>
    """, item=item)

@app.route('/delete/<int:id>')
def delete(id):
    item = InventoryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

