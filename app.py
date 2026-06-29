from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'rahasia_uas_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tokobangunan.db'
db = SQLAlchemy(app)

class Produk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    stok = db.Column(db.Integer, default=0)

class Transaksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produk_id = db.Column(db.Integer, db.ForeignKey('produk.id'))
    jumlah = db.Column(db.Integer)

@app.route('/')
def index():
    query = request.args.get('q')
    if query:
        produk = Produk.query.filter(Produk.nama.contains(query)).all()
    else:
        produk = Produk.query.all()
    return render_template('index.html', produk=produk, transaksi=Transaksi.query.all())

@app.route('/tambah', methods=['POST'])
def tambah():
    db.session.add(Produk(nama=request.form['nama'], stok=int(request.form['stok'])))
    db.session.commit()
    flash('Produk berhasil ditambahkan!', 'success')
    return redirect(url_for('index'))

@app.route('/hapus/<int:id>')
def hapus(id):
    db.session.delete(Produk.query.get(id))
    db.session.commit()
    flash('Produk dihapus!', 'warning')
    return redirect(url_for('index'))

@app.route('/transaksi', methods=['POST'])
def transaksi():
    p = Produk.query.get(int(request.form['produk_id']))
    jml = int(request.form['jumlah'])
    if p and p.stok >= jml:
        p.stok -= jml
        db.session.add(Transaksi(produk_id=p.id, jumlah=jml))
        db.session.commit()
        flash(f'Penjualan {p.nama} berhasil!', 'success')
    else:
        flash('Stok tidak mencukupi!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)