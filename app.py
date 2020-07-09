from flask import Flask 
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeSerializer

app = Flask(__name__)


############  Mongo DB connection ################
app.config['SECRET_KEY'] = 'Hemmelig!'  ## is required
app.config["MONGO_DBNAME"] = "rat"  ## DB name
app.config["MONGO_URI"] = "mongodb://localhost:27017/rat"   ## local DB, But can be used MLab(free 500MB) https://mlab.com/

mongo = PyMongo(app)
login_manager = LoginManager(app)
serializer = URLSafeSerializer(app.secret_key)

class Teacher(UserMixin):
    def __init__(self, teacher_data):
        self.teacher_data = teacher_data

    def get_id(self):
        return self.teacher_data['session_token']

@login_manager.user_loader
def load_user(session_token):
    teachers = mongo.db.teachers 
    teacher_data = teachers.find_one({'session_token': session_token})
    if teacher_data:
        return Teacher(teacher_data)
    return None

@app.route('/create')
def create():
    teachers = mongo.db.teachers
    session_token = serializer.dumps(['Solo', 'Nypass'])
    teachers.insert({'name' : 'Ola', 'session_token' : session_token})

    return '<h1>Lærer er Klar!</h1>'

@app.route('/login')
def index():
    teachers = mongo.db.teachers
    teachers = teachers.find_one({'name' : 'Ola'})
    
    ola = Teacher(teachers)

    login_user(ola)

    return '<h1>Nå du er inne!</h1>'

@app.route('/home')
@login_required
def home():
    return '<h1>Velkommen {}</h1>'.format(current_user.teacher_data['name'])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<h1> Du er ute, Ha det bra!</h>'

if __name__ == '__main__':
    app.run(debug=True)