from flask import render_template, request, redirect, url_for, Blueprint
from app.services import author_service

author_bp = Blueprint('author', __name__)


# ROTA 1: Página principal que agora SOMENTE exibe o formulário de cadastro
@author_bp.route('/', methods=['GET'])
def author():
    """Renderiza a página com o formulário de cadastro."""
    return render_template('cadastro.html')


# ROTA 2 (NOVA): Página que SOMENTE exibe a lista de usuários
@author_bp.route('/lista', methods=['GET'])
def lista_usuarios():
    """Busca os usuários e renderiza a página de listagem."""
    usuarios_cadastrados = author_service.listar()
    return render_template('lista_usuarios.html', usuarios=usuarios_cadastrados)


@author_bp.route('/add', methods=['POST'])
def add_author():
    """Processa o formulário de cadastro e redireciona para a lista."""
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    senha = request.form.get('senha')
    author_service.inserir(nome, email, telefone, senha)
    #  Redireciona para a nova página da lista
    return redirect(url_for('author.lista_usuarios'))


@author_bp.route('/delete/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    """Exclui um usuário e redireciona para a lista."""
    author_service.excluir(author_id)
    # Redireciona para a nova página da lista
    return redirect(url_for('author.lista_usuarios'))


@author_bp.route('/atualiza/<int:id>', methods=["GET", "POST"])
def atualiza_autor(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        author_service.atualiza_autor(id, name, email, phone)
        # ALTERADO: Redireciona para a nova página da lista
        return redirect(url_for('author.lista_usuarios'))

    autor = author_service.recupera_autor(id)
    # A página de atualização continua a mesma
    return render_template("atualiza_autor.html", autor=autor)




# ... aqui ficam as outras rotas (cadastro, lista etc)

@author_bp.route('/relatorio')
def relatorio():
    print("###############RELATORIO##########")
    filename = 'out.pdf'
    path = os.getcwd()
    static_dir = os.path.abspath(os.path.join(path, os.pardir))
    static_dir = os.path.join(static_dir, 'static')
    if not os.path.isdir(static_dir):
        static_dir = os.path.join(os.getcwd(), 'app', 'static')
    pdf_path = os.path.join(static_dir, filename)

    query = text("SELECT name, email, phone FROM authors ORDER BY name")
    rows = db.session.execute(query).fetchall()

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    x = 50
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "Relatório de Cadastros")
    y -= 30
    c.setFont("Helvetica", 12)

    for r in rows:
        name = r[0] if len(r) > 0 else ''
        email = r[1] if len(r) > 1 else ''
        phone = r[2] if len(r) > 2 else ''
        c.drawString(x, y, f"Nome: {name}")
        y -= 16
        c.drawString(x+10, y, f"E-mail: {email}")
        y -= 16
        c.drawString(x+10, y, f"Telefone: {phone}")
        y -= 22
        if y < 80:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, f"Total de cadastros: {len(rows)}")
    c.save()

    return render_template('relatorio.html', pdf_filename=filename)

