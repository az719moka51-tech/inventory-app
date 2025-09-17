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
<h1>在庫一覧</h1>
<table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th>商品名</th>
    <th>数量</th>
    <th>単価</th>
    <th>仕入れ日</th>
  </tr>
  {% for item in inventory %}
  <tr>
    <td>{{ item.item_name }}</td>
    <td>{{ item.quantity }}</td>
    <td>{{ item.unit_price }}</td>
    <td>{{ item.purchase_date }}</td>
  </tr>
  {% endfor %}
</table>

{% if alerts %}
<h2>在庫アラート！</h2>
<ul>
  {% for item in alerts %}
    <li>{{ item.item_name }} が少なくなっています（残り {{ item.quantity }} 個）</li>
  {% endfor %}
</ul>
{% endif %}

<h2>在庫を追加</h2>
<form method="POST" action="/add">
  商品名: <input type="text" name="item_name" required><br>
  数量: <input type="number" name="quantity" required><br>
  単価: <input type="number" name="unit_price" required><br>
  仕入れ日: <input type="date" name="purchase_date" required><br>
  <input type="submit" value="登録">
</form>

    
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

