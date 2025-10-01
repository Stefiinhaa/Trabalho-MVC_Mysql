from flask import Blueprint, render_template
from app import db
from sqlalchemy import text
from fpdf import FPDF
import os

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.route("/relatorio/pdf")
def generate_pdf():
    # Buscar os cadastros
    query = text("""
        SELECT name, email, phone
        FROM authors
        ORDER BY name
    """)
    result = db.session.execute(query).fetchall()

    # Criar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatório de Cadastros", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for row in result:
        pdf.cell(0, 10, f"Nome: {row.name}", ln=True)
        pdf.cell(0, 8, f"E-mail: {row.email}", ln=True)
        pdf.cell(0, 8, f"Telefone: {row.phone}", ln=True)
        pdf.ln(5)

    # Resumo
    pdf.set_font("Arial", "B", 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Total de cadastros: {len(result)}", ln=True)

    # Salvar no static (igual MVC_Mysql)
    pdf_path = os.path.join("app", "static", "out.pdf")
    pdf.output(pdf_path)

    # Renderiza a página com o link
    return render_template("pdf/pdf_view.html")
