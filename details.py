from flask import  Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
app.app_context().push()
# these above lines are to made connection with sql database

class Contact(db.Model):
    __tablename__ = "Contacts"

    srno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    number = db.Column(db.Text,unique=True, nullable=False)
    address = db.Column(db.Text,nullable=False)
    email_id = db.Column(db.Text,nullable=False)
    Company = db.Column(db.Text,nullable=False)

    def __init__(self,name,number,address,email_id,Company):
        self.name=name
        self.number=number
        self.address=address
        self.email_id=email_id
        self.Company=Company

db.create_all()

@app.route("/",methods=["get","post"])
def details():
    if request.method == "POST":
        fn= request.form.get('name')
        ph_no= request.form.get('ph_no')
        add= request.form.get('address')
        email= request.form.get('for_email')
        company= request.form.get('company')
        entry=Contact(name=fn,number=ph_no,address=add,email_id=email,Company=company)
        
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("details"))
    else:
        return render_template("home.html",contact=Contact.query.order_by(Contact.name).all())

@app.route("/search",methods=["POST","GET"])
def search():
    if request.method == "POST":
        cont_cap = request.form.get('search')
        
        if cont_cap.isalpha(): 
            contact_ifalpha= Contact.query.filter_by(name=cont_cap).all()
            return render_template("home.html",contact=contact_ifalpha)
        elif cont_cap.isdigit():
            cont_ph = Contact.query.filter_by(phone=cont_cap).all()
            return render_template("home.html",contact=cont_ph)
    
    return redirect(url_for("home"))


@app.route("/update_list",methods = ['GET', 'POST'])
def c_update():
    if request.method == 'POST':
        my_Contact = Contact.query.get(request.form.get('srno'))
        my_Contact.name = request.form['name']
        my_Contact.number= request.form['ph_no']
        my_Contact.address= request.form['address']
        my_Contact.email_id= request.form['for_email']
        my_Contact.Company= request.form['company']
        
        db.session.commit()

        return redirect(url_for('details'))

    else:

        return render_template('home.html',contact=Contact.query.all())

@app.route("/delete/<srno>/", methods = ['GET','POST'])
def delete_list(srno):
        my_Contact = Contact.query.get(srno)
        db.session.delete(my_Contact)
        db.session.commit()
        return redirect(url_for('details'))

app.run(host='localhost', port=5000)