from app.models.author_model import authors
from app import db

def listar():
    return authors.query.all()

def inserir(name, email, phone, password):
    if authors.query.filter_by(email=email).first():
        print(f"Erro: O email '{email}' já está em uso.")
        return None
    new_user = authors(name=name, email=email, phone=phone)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def excluir(author_id):
    author = authors.query.get(author_id)
    if author:
        db.session.delete(author)
        db.session.commit()

# --- FUNÇÕES DE ATUALIZAÇÃO AJUSTADAS ---

def recupera_autor(autor_id):
    """Busca um usuário pelo seu ID. usa .get() que é mais direto."""
    return authors.query.get(autor_id)

def atualiza_autor(id, name, email, phone):
    """Encontra o usuário pelo ID e atualiza seus dados."""
    user = authors.query.get(id)
    if user:
        user.name = name
        user.email = email
        user.phone = phone
        db.session.commit() # Salva as alterações no banco de dados
