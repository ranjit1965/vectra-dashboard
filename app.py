from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)



# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['vectra']
user_data_collection = db['user_data']


@app.route('/add')
def add_page():
    return render_template('Add.html')


@app.route('/edit')
def edit_page():
    return render_template('edit.html')
    
@app.route('/delete')
def delete_page():
    return render_template('delete.html')


@app.route('/')
def home():
    return render_template('index.html')  # Render your homepage with the "Add" button


@app.route('/add_user_data', methods=['POST'])
def add_user():
    name = request.form['Name']
    phone_number = request.form['Phonenumber']
    ip_address = request.form['IPAddress']
    date = request.form['Date']
    foundation_number = request.form['Foundationnumber']

    # Insert data into MongoDB
    user_data_collection.insert_one({
        'name': name,
        'phone_number': phone_number,
        'ip_address': ip_address,
        'date': date,
        'foundation_number': foundation_number
    })

    return render_template('add_success.html', name=name, phone_number=phone_number,
                            ip_address=ip_address, date=date, foundation_number=foundation_number)


@app.route('/edit_user_data', methods=['POST'])
def edit_user_data():
    name = request.form['Name']
    phone_number = request.form['Phonenumber']
    last_digit = request.form['lastDigit']
    ip_address = f"192.168.0.{last_digit}"
    date = request.form['Date']
    foundation_number = request.form['Foundationnumber']

    # Update user data in MongoDB
    result = user_data_collection.update_one(
        {'name': name},
        {'$set': {
            'phone_number': phone_number,
            'ip_address': ip_address,
            'date': date,
            'foundation_number': foundation_number
        }}
    )

    if result.modified_count > 0:
        return render_template('update_success.html', name=name, phone_number=phone_number,
                               ip_address=ip_address, date=date, foundation_number=foundation_number)
    else:
        return jsonify({"status": "error", "message": "No user found to update."})


@app.route('/delete_user_data', methods=['POST'])
def delete_user_data():
    name = request.form['Name']  # Get the user name from the form

    # Delete user from MongoDB
    result = user_data_collection.delete_one({'name': name})

    if result.deleted_count > 0:
        return render_template('delete_confirmation.html', name=name)  # Render confirmation page
    else:
        return jsonify({"status": "error", "message": "No user found to delete."})


@app.route('/display_users',methods=['GET'])
def display_users():
    # Fetch all user data from MongoDB
    users = user_data_collection.find()

    # Convert the MongoDB cursor object into a list of dictionaries
    data = []
    for user in users:
        data.append({
            'name': user.get('name'),
            'phone_number': user.get('phone_number'),
            'ip_address': user.get('ip_address'),
            'date': user.get('date'),
            'foundation_number': user.get('foundation_number')
        })
    
    # Render the data in the display.html template
    return render_template('display.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
