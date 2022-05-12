from flask import Flask,  render_template,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

class NameForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    tel = StringField('Phone',validators=[DataRequired()])
    submit = SubmitField('submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard guess string'
# database URI removed for saftey purposes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False


bootstrap = Bootstrap(app)
moment=Moment(app)
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__='contacts'
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64), unique=True,index=True)
    tel= db.Column(db.String,unique=True)

    def __repr__(self):
        return '<Contact %r>' % self.name

@app.route('/')
def index():
    contacts = Contact.query.all() 
    return render_template('index.html',contacts = contacts,current_time=datetime.utcnow())


@app.route('/contacts/',methods=['GET','POST'])
def contacts():
    form = NameForm()
    if form.validate_on_submit():        
        contact=Contact(name=form.name.data,tel=form.tel.data)
        db.session.add(contact)
        db.session.commit()
        flash('New contact added successfully')
        form.name.data = ''
        form.tel.data = ''
        return redirect(url_for('index'))
    
    return render_template('contact.html',form=form)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route('/delete/<int:contact_id>')
def delete(contact_id):
    contact= Contact.query.filter_by(id=contact_id).first()
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Contact=Contact)


if __name__=='__main__':
    app.run(debug=True)