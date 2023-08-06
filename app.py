from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'b0e7e1da93055c15370a3fff4821652d'

# Configure the database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="heelplay",
    database="heel_play_db"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        graduation_year = request.form['graduation_year']
        major = request.form['major']
        sport = request.form['sport']
        position = request.form['position']
        bio = request.form['bio']
        profile_pic = request.files['profile_pic']


        # Check if passwords match
        if password != confirm_password:
            error_message = 'Passwords do not match'
            return render_template('register.html', error=error_message, 
                                   name=name, email=email, graduation_year=graduation_year,
                                   major=major, sport=sport, position=position, bio=bio)
        
        # Save the uploaded profile picture
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(filename)
        else:
            filename = None

        # Create a database cursor
        cursor = db.cursor()

        # Insert user data into the database
        sql = "INSERT INTO users (name, email, password, graduation_year, major, sport, position, bio, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, email, password, graduation_year, major, sport, position, bio, filename)
        cursor.execute(sql, values)

        # Commit the transaction and close the cursor
        db.commit()
        cursor.close()

        # Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        # Create a database cursor
        cursor = db.cursor()

        # Execute the SQL query to fetch user data
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(sql, values)

        # Fetch the column names from the cursor
        columns = ('id', 'name', 'email', 'password', 'graduation_year', 'major', 'sport', 'position', 'bio', 'profile_pic')

        # Fetch the result
        user_data = cursor.fetchone()
        #print("User data: ", user_data)

        # Close the cursor
        cursor.close()

        if user_data:
            user = dict(zip(columns, user_data))
            #print("User dictionary:", user)

            # Set the 'session' variable with the user's email
            session['email'] = user['email']
            #print(session['email'])

            # User found, redirect to the main project screen
            return redirect(url_for('main_project_screen'))

        # User not found or invalid credentials, show an error message
        error_message = 'Invalid email or password'
        return render_template('index.html', error=error_message)
    
    return render_template('index.html')


@app.route('/main')
def main_project_screen():
    # Fetch the user's profile information from the database
    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE email = %s"
    values = (session['email'],)  # Assuming you store the user's email in the 'session' variable
    cursor.execute(sql, values)
    user_data = cursor.fetchone()
    cursor.close()

    # Convert the user data to a dictionary
    columns = ('id', 'name', 'email', 'password', 'graduation_year', 'major', 'sport', 'position', 'bio', 'profile_pic')
    user = dict(zip(columns, user_data))

    #print(user)

    # Render the profile page and pass the user profile data
    return render_template('main.html', user=user)

@app.route('/profile')
def profile():
    # Fetch the user's profile information from the database
    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE email = %s"
    values = (session['email'],)
    cursor.execute(sql, values)
    user_data = cursor.fetchone()
    cursor.close()

    # Convert the user data to a dictionary
    columns = ('id', 'name', 'email', 'password', 'graduation_year', 'major', 'sport', 'position', 'bio', 'profile_pic')
    user = dict(zip(columns, user_data))
    
    # Render the profile page and pass the user profile data
    return render_template('profile.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    #print("Edit Profile route called.")
    # Fetch the user's profile information from the database using their email in the session
    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE email = %s"
    values = (session['email'],)
    cursor.execute(sql, values)
    user_data = cursor.fetchone()
    cursor.close()
    
    # Convert the user data to a dictionary
    columns = ('id', 'name', 'email', 'password', 'graduation_year', 'major', 'sport', 'position', 'bio', 'profile_pic')
    user = dict(zip(columns, user_data))

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', user['name'])
        email = request.form.get('email', user['email'])
        graduation_year = request.form.get('graduation_year', user['graduation_year'])
        major = request.form.get('major', user['major'])
        sport = request.form.get('sport', user['sport'])
        position = request.form.get('position', user['position'])
        bio = request.form.get('bio', user['bio'])
        profile_pic = request.files.get('profile_pic')

        # Save the uploaded profile picture if a new one is provided
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(filename)
        else:
            filename = user['profile_pic']

        # Create a database cursor
        cursor = db.cursor()

        # Update user data in the database
        sql = "UPDATE users SET name = %s, graduation_year = %s, major = %s, sport = %s, position = %s, bio = %s, profile_pic = %s WHERE email = %s"
        values = (name, graduation_year, major, sport, position, bio, filename, email)
        cursor.execute(sql, values)

        # Commit the transaction and close the cursor
        db.commit()
        cursor.close()

        # Redirect to the main profile screen after successful update
        return redirect(url_for('profile'))

    # Render the edit profile page and pass the user profile data
    return render_template('edit_profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

