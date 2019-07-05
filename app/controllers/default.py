from flask import Flask, render_template, flash, redirect, url_for, request, Session
from flask_login import login_user, logout_user, login_required
from app import app, db, lm
from app.models.tables import User, Role, Permission
from app.models.forms import LoginForm, RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.decorators import admin_required, permission_required




@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/principal")
@app.route("/")
def principal():
    return render_template('principal.html')

@app.route("/regulamento")
def regulamento():
    return render_template('regulamento.html')

@app.route("/origem")
def origem():
    return render_template('origem.html')

@app.route("/brasileirao2018")
def brasileirao2018():
    return render_template('brasileirao2018.html')

@app.route("/brasileirao2008")
def brasileirao2008():
    return render_template('Brasileirao2008.html')

@app.route("/copadomundo")
def copadomundo():
    return render_template('copadomundo.html')


@app.route("/jogadores")
def jogadores():
    return render_template('jogadores.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm( )
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            mensagem = "Seja bem vindo ao meu site: " + user.username + "!"
            flash(mensagem)
            return redirect(url_for("principal"))
        else:
            flash("Login invalido.")
    else:
        print(form.errors)
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Deslogado")
    return redirect(url_for("principal"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        cadastro = User(username=form_register.username.data, password=form_register.password.data, name=form_register.name.data, email=form_register.email.data)
        db.session.add(cadastro)
        db.session.commit()
        login_user(cadastro)
        mensagem = "Usuário registrado e logado com sucesso! Seja bem vindo ao meu site: " + cadastro.username + "!"
        flash(mensagem)
        return redirect(url_for('principal'))
    else:          
        return render_template('register.html', form_register=form_register)    
                             

            
@app.route("/lista")
@login_required
@admin_required
def lista():
    usuarios = User.query.all()
    return render_template("lista.html", usuarios=usuarios)

@app.route("/excluir/<int:id>")
def excluir(id):
    usuario = User.query.filter_by(id=id).first()

    db.session.delete(usuario)
    db.session.commit()

    usuarios = User.query.all()
    flash('Usuário removido com sucesso.')
    return render_template("lista.html", usuarios=usuarios)


@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    usuarios = User.query.filter_by(id=id).first()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        email = request.form.get("email")     
        if username and password and name and email:
            usuarios.username = username
            usuarios.password = password
            usuarios.name = name
            usuarios.email = email       
            db.session.commit()
                    
                        
            return redirect(url_for("lista"))
    return render_template("atualizar.html", usuarios=usuarios)



@app.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@app.route('/moderator')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"

@app.route("/teste")
def teste():
    Role.insert_roles()
    return "a"


    
