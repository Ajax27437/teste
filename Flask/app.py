from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import webbrowser
import threading

# Criação da instância da aplicação Flask
app = Flask(__name__)

# Função para abrir o navegador automaticamente
def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

# Função para inicializar o banco de dados e criar a tabela se não existir
def init_db():
    conn = sqlite3.connect("pacientes.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            idade INTEGER,
            cpf INTEGER,
            hora INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Rota da página principal
@app.route("/")
def homepage():
    return render_template("principal.html")  # HTML padrão

# Rota para a lista de pacientes
@app.route('/pacientes')
def pacientes():
    conn = sqlite3.connect("pacientes.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM pacientes")
    pacientes = cur.fetchall()
    conn.close()

    # Passa os dados para o template
    return render_template('pacientes.html', pacientes=pacientes)

# Rota para exibir o formulário de pacientes e inserir novos pacientes
@app.route('/novo_paciente', methods=['GET', 'POST'])
def novo_paciente():
    if request.method == 'POST':
        # Captura os valores do formulário
        nome = request.form.get('name')
        idade = request.form.get('age')
        cpf = request.form.get('cpf')
        hora = request.form.get('hour')

        # Conecta ao banco de dados e insere os dados
        conn = sqlite3.connect("pacientes.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO pacientes (nome, idade, cpf, hora) VALUES (?, ?, ?, ?)",
                    (nome, idade, cpf, hora))
        conn.commit()
        conn.close()

        # Redireciona para a página de pacientes
        return redirect(url_for('pacientes'))

    return render_template('pacientes.html')  # Formulário para inserir pacientes

# Rota para deletar um paciente
@app.route('/deletar_paciente/<int:paciente_id>', methods=['POST'])
def deletar_paciente(paciente_id):
    conn = sqlite3.connect("pacientes.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM pacientes WHERE id=?", (paciente_id,))
    conn.commit()
    conn.close()

    # Redireciona para a lista de pacientes
    return redirect(url_for('pacientes'))

# Inicializa o banco de dados
init_db()

# Função principal que roda a aplicação
if __name__ == "__main__":
    # Inicia o servidor e abre o navegador em uma nova thread
    threading.Timer(0.1, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True)






