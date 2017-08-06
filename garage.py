from flask import Flask, render_template, flash, url_for, redirect, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, validators
from functools import wraps

app = Flask(__name__)


# Config Mysql
app.config['MYSQL_HOST'] = '127.0.0.1 localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tiger'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# init Mysql
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')



class CreateParkingGarageForm(Form):
    numberofParking = StringField('NumberofParking',[validators.Length(min=1,max=10)])

@app.route('/createParkingGarage',methods = ['GET','POST'])
def createParkingGarage():
    form = CreateParkingGarageForm(request.form)
    if request.method == 'POST' and form.validate():
        numberofParking = int(form.numberofParking.data)
        print numberofParking

        # Create cursor
        cur = mysql.connection.cursor()

        # execute query
        for i in range(numberofParking):
            cur.execute("INSERT INTO garage(registration,color) VALUES(%s,%s)",("null","null"))
            mysql.connection.commit()


        cur.close()
        flash('you have Created parking garage', 'success')
        return redirect(url_for('index'))

    return render_template('createParkingGarage.html',form=form)



class Leave(Form):
    slotNumber = StringField('SlotNumber',[validators.Length(min=1,max=10)])

@app.route('/leave',methods = ['GET','POST'])
def leave():
    form = Leave(request.form)
    if request.method == 'POST' and form.validate():
        slotNumber = int(form.slotNumber.data)
        print slotNumber

        # Create cursor
        cur = mysql.connection.cursor()

        # execute query
        cur.execute("UPDATE garage SET registration=%s ,color=%s WHERE slot=%s",("null","null",slotNumber))
        mysql.connection.commit()


        cur.close()
        flash('Slot number %d is free'%int(slotNumber), 'success')
        return redirect(url_for('index'))

    return render_template('leave.html',form=form)




class ParkingForm(Form):
    slot = StringField('Slot', [validators.Length(min=1)])
    vcnumber = StringField('VCnumber',[validators.Length(min=1, max=50)])
    color = StringField('Color',[validators.Length(min=1,max=30)])


@app.route('/parking',methods = ['GET','POST'])
def parking():
    form = ParkingForm(request.form)
    if request.method == 'POST' and form.validate():
        slot = form.slot.data
        vcnumber = form.vcnumber.data
        color = form.color.data
        print vcnumber
        print color
        print slot

        # Create cursor
        cur = mysql.connection.cursor()

        # execute query
        cur.execute("UPDATE garage SET registration=%s,color=%s WHERE slot=%s",(vcnumber,color,slot))
        mysql.connection.commit()

        cur.close()
        flash('Parked in slot number %d'%int(slot), 'success')
        return redirect(url_for('index'))
    else:
        # Create cursor
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT slot from garage WHERE color='null' ORDER BY slot asc limit 1")
        slotN = cur.fetchone()
        print slotN
        # flash('Park at slot number %s'%(slotN), 'success')
        if result>0:
            return render_template('parking.html',form=form,slotN=slotN)
        else:
            flash('Sorry, parking garage is full','success')
            return redirect(url_for('index'))
        cur.close()

    return render_template('parking.html',form=form)

@app.route('/status')
def status():
    # Create cursor
    cur = mysql.connection.cursor()

    # GET article
    result = cur.execute("SELECT * FROM garage")

    slots = cur.fetchall()

    if result > 0:
        return render_template('status.html',slots=slots)
    else:
        msg = 'No parking found'
        return render_template('status.html',msg=msg)
    # Close connection
    cur.close()





if __name__ == "__main__":
    app.secret_key = 'secret1234'
    app.run(debug=True)