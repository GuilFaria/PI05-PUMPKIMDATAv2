import streamlit as st
import psycopg2
from dotenv import load_dotenv, dotenv_values
import hashlib
import io
import os
from streamlit_router import StreamlitRouter

#------------------------Pre-Works---------------------------#


# Usuário e senha teste: guilhe@faria.com, gui123


 
load_dotenv()

host = os.getenv("HOST_DB")
port = os.getenv("PORT_VALUE")
username = os.getenv("USER_APP")
pw_db = os.getenv("PASSWORD")
database = os.getenv("DATABASE")


cache = st.session_state


def encriptografa_sha3_256(content: list | io.BytesIO | str= str) -> list[str] | str: 
    '''Criptografia de sha3-256 é feito da seguinte forma (Número EXCLUSIVO, sempre diferente)'''
    
    if isinstance(content, str):
        hash_text = content.encode()
        hash = hashlib.sha3_256(hash_text)
        return hash.hexdigest()
        
    elif isinstance(content, io.BytesIO):
        hash = hashlib.sha3_256(content)
        return hashs_list.hexdigest()
        
    elif isinstance(content, list):
        hashs_list = []
        for string in content:
            string = str(string)
            encoded_text = string.encode()
            hashed_text = hashlib.sha3_256(encoded_text).hexdigest()
            hashs_list.append(hashed_text)
        return hashs_list        



#---------------TELA DE CADASTRO ALUNO---------------#


def tela_cadastro_aluno():
    return None


def tela_login(router: StreamlitRouter):
    
    st.header("SIPA - Brasil")
    with st.form(key="login e senha", enter_to_submit=False):

        login = st.text_input("Login de Usuário", placeholder="Digite seu usuário aqui")
        senha = st.text_input("Senha", type='password', placeholder="Digite sua senha aqui")
        
        col1, col2= st.columns([4.3, 1], gap="large", vertical_alignment="center")
        
        with col1:
            enter_button = st.form_submit_button(label="Entrar")
        
        with col2:
            button_cad = st.form_submit_button(label="Cadastrar")
        print(router.endpoint_session_name)
        if enter_button:
            user = {}
            
            user['login'] = login
            user['senha'] = senha
            
            password_enc = encriptografa_sha3_256(senha)
            
            if user_auth(login, password_enc):
                if 'login' in cache:
                    del cache['login']
                if 'email' in cache:
                    del cache['senha']
                
                cache["login"] = user["login"]
                cache["password"] = user["senha"]
                print(router.urls.script_name)
                return router.redirect(*router.build("teste_main"))
            
            else:
                st.error("Login ou senha inválidos")

        elif button_cad:
            popup_cadastrar()



@st.dialog("Cadastro | SIPA")
def popup_cadastrar():
        
        st_cad_errors = 0

        st.write("Realize o seu sign-up aqui.")
        
        user_cad_name: str = st.text_input("Nome", placeholder="Digite seu nome aqui", autocomplete='name')
        if user_cad_name:
            if len(user_cad_name.split(' ')) <= 1:
                st.error("Coloque seu nome completo.")
                st_cad_errors += 1

        user_cad_email: str = st.text_input("E-mail",  placeholder="Digite seu e-mail aqui", autocomplete='email')
        if user_cad_email:
            if "@" not in user_cad_email:
                st.error("Coloque um e-mail válido.")
                st_cad_errors += 1
            elif "." not in user_cad_email:
                st.error("Coloque um e-mail válido.")
                st_cad_errors += 1

        user_password: str = st.text_input("Senha",type="password", placeholder="Digite sua senha aqui")
        user_password_conf: str = st.text_input("Confirmar senha", type="password",placeholder="Confirme sua senha")
        user_cad_button = st.button(label="Cadastrar", key="button_cadastrar_finish")

        if user_cad_button:
            if user_password == user_password_conf:
                user = {}
                user['nome'] = user_cad_name
                user['email'] = user_cad_email
                user['senha'] = encriptografa_sha3_256(user_password)

                cadastro_usuario = cad_user(user)
                
                if cadastro_usuario:
                    st.success("Cadastro realizado com sucesso")
                    #Inserir st.state para o usuario aparecer depois de cadastro

                else:
                    st.error("Erro ao realizar cadastro")
            else:
                st.error("Senhas não conferem")



def cad_user(userDict: dict):
    
    # Conectar ao banco de dados
    try:
        global host
        global username
        global port
        global pw_db
        global database


        conn = psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=pw_db
            )
        

        cur = conn.cursor()
        
        cur.execute("SELECT id_user FROM usuario WHERE user_login = %s", (userDict['email'],))
        user_auth_exists = cur.fetchone()

        if user_auth_exists:
            conn.close()
            return False
    
        cur.execute('''INSERT INTO usuario (user_name, user_login, user_password) VALUES (%s, %s, %s)''',
                    (userDict["nome"], userDict["email"], userDict["senha"])
                    )
        
        conn.commit()
        conn.close()

    except Exception as e:
        st.write(e)
        conn.close()
        return False

    return True
    
    

def user_auth(login, password_enc):
    
    # Conectar ao banco de dados
    global host
    global username
    global port
    global pw_db
    global database
    
    
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=username,
        password=pw_db
        )
    
    cur = conn.cursor()
    
    cur.execute('''SELECT us.id_user FROM usuario us 
                WHERE 1=1
                AND us.user_login = %s 
                AND us.user_password = %s''', 
                (login, password_enc)
                )
    
    fetched = cur.fetchone()

    if fetched:
        return True
    
    else:
        return False
   