from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

#koneksi ke database
app.secret_key = 'bebas'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='luxstay'
mysql = MySQL(app)




@app.route('/')
def home():
    return render_template('index.html')
#registrasi
@app.route('/registrasi', methods=('GET','POST'))
def registrasi():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        level = request.form['level']
        
        #cek username/email
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_users WHERE username=%s OR email=%s', (username, email))
        akun = cursor.fetchone()
        if akun is None:
            cursor.execute('INSERT INTO tb_users VALUES (NULL, %s, %s, %s, %s)', 
               (username, email, generate_password_hash(password), level))

            mysql.connection.commit()
            flash('Registrasi Berhasil', 'success')
        else :
            flash('Username sudah ada', 'danger')
            
    return render_template('registrasi.html')

#login
@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        #cek data user
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_users WHERE email=%s', (email, ))
        akun = cursor.fetchone()
        if akun is None:
            flash('Login Gagal, Cek Username Anda', 'danger')
        elif not check_password_hash(akun[3], password):
            flash('Login Gagal, Cek Username Anda', 'danger')
        else:
            session['loggedin'] = True  
            session['username'] = akun[1]   
            session['level'] = akun[4]   
            return redirect(url_for('base'))
    return render_template('login.html')

#logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('level', None)
    return redirect(url_for('login'))

#base
@app.route('/')
def base():
    if 'loggedin' in session:
        return render_template('base.html')
    flash('Harap Login terlebih dahulu', 'danger')
    return redirect(url_for('login'))

#tampil data
@app.route('/admin')
def customertampildata():
    cur = mysql.connection.cursor()
    cur.execute (" SELECT * FROM customer ORDER BY id DESC")
    datatampil= cur.fetchall()
    cur.close()
    return render_template('admin.html', datapemesan = datatampil)

#insert into
@app.route('/', methods=['POST'])
def customerinsert():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['phone']
        tipe = request.form['tipe']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jml = request.form['jml']
        ket = request.form['ket']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer (nama, email, phone, tipe, checkin, checkout, jml, ket) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nama, email, phone, tipe, checkin, checkout, jml, ket))
        mysql.connection.commit()
        flash("Data berhasil di kirim ")
        return redirect(url_for('home'))
    
#insert into
@app.route('/customerupdate', methods=['POST'])
def customerupdate():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['phone']
        tipe = request.form['tipe']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jml = request.form['jml']
        status = request.form['status']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE customer SET nama=%s, email=%s, phone=%s, tipe=%s, checkin=%s, checkout=%s, jml=%s, status=%s WHERE id=%s", (nama, email, phone, tipe, checkin, checkout, jml, status, id,))
        mysql.connection.commit()
        flash("Data berhasil di Update ")
        return redirect(url_for('customertampildata'))


# delete data
@app.route('/customerhapus/<int:id>', methods=["GET"])
def customerhapus(id):
    cur = mysql.connection.cursor()
    cur.execute ("DELETE FROM customer WHERE id=%s", (id,))
    mysql.connection.commit()
    flash("data Berhasil di Hapus")
    return redirect( url_for('customertampildata'))

@app.route('/kamar')
def typekamar():
    return render_template('kamar.html')

@app.route('/fasilitas')
def fasilitas():
    return render_template('fasilitas.html')

if __name__ == '__main__' :
    app.run(debug=True)