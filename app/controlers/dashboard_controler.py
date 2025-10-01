from flask import Blueprint, render_template
from app import db
import pandas as pd
from sqlalchemy import text

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    # Buscar dados do banco
    result = db.session.execute(text("SELECT id, title FROM books")).fetchall()

    # Converter para DataFrame
    df = pd.DataFrame(result, columns=["id", "title"])

    # Exemplo de métrica: tamanho do título
    df["tamanho"] = df["title"].apply(len)

    dados = {
        "titulos": df["title"].tolist(),
        "tamanhos": df["tamanho"].tolist()
    }

    return render_template("dashboard/dashboard.html", dados=dados)
