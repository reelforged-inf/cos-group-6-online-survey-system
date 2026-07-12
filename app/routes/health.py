from flask import Blueprint, render_template

health_bp = Blueprint('health', __name__, template_folder='../../templates')

@health_bp.route('/')
def index():
    return render_template('index.html')

@health_bp.route('/login')
def login():
    return render_template('login.html')
