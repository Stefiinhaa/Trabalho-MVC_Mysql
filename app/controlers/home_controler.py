
from app import app
from flask import Flask, render_template, request, redirect, url_for, Blueprint

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
   return render_template('home.html')




