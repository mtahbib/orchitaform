from flask import Flask, render_template, request, redirect, url_for, jsonify  # Add 'jsonify' import
import mysql.connector

app = Flask(__name__)

# Replace these with your MySQL database credentials
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'mybook'

# Create a MySQL connection
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = connection.cursor()

# Create the 'employee_data' table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS employee_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    emp_id INT,
    designation VARCHAR(255)
)
'''
cursor.execute(create_table_query)

@app.route('/')
def index():
    # Fetch and display existing employee data
    cursor.execute('SELECT id, name, emp_id, designation FROM employee_data')
    data = cursor.fetchall()
    return render_template('index.html', employees=data)

@app.route('/save', methods=['POST'])
def save():
    data = {
        'name': request.form['name'],
        'emp_id': int(request.form['emp_id']),
        'designation': request.form['designation']
    }

    save_to_database(data)

    return redirect(url_for('index'))

# ... (previous Flask code) ...

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    if request.method == 'POST':
        # Update employee data in the database
        name = request.form['name']
        emp_id = int(request.form['emp_id'])
        designation = request.form['designation']

        update_query = '''
        UPDATE employee_data SET name=%s, emp_id=%s, designation=%s WHERE id=%s
        '''
        cursor.execute(update_query, (name, emp_id, designation, id))
        connection.commit()

        # Assuming you want to send a JSON response
        return jsonify({'message': 'Employee updated successfully'})

    # Fetch the existing employee data for the selected ID
    cursor.execute('SELECT * FROM employee_data WHERE id=%s', (id,))
    employee_data = cursor.fetchone()

    return render_template('update.html', employee=employee_data)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    if request.method == 'POST':
        # Delete employee data from the database
        delete_query = 'DELETE FROM employee_data WHERE id=%s'
        cursor.execute(delete_query, (id,))
        connection.commit()

        # Assuming you want to send a JSON response
        return jsonify({'message': 'Employee deleted successfully'})

    # If it's a GET request, you can redirect or render a template if needed
    return redirect(url_for('index'))



def save_to_database(data):
    insert_query = '''
    INSERT INTO employee_data (name, emp_id, designation) VALUES (%s, %s, %s)
    '''

    cursor.execute(insert_query, (data['name'], data['emp_id'], data['designation']))
    connection.commit()

if __name__ == '__main__':
    app.run(debug=True)
