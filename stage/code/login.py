import streamlit as st
import psycopg2
from dotenv import load_dotenv, dotenv_values
import hashlib
import io
import os
from streamlit_router import StreamlitRouter

#------------------------Pre-Works---------------------------#

# Usuário e senha teste: guilhe@faria.com, senha: gui, 
# senha hash: 35f413a6cfe5475b20aa870e4e90b4e6c2f5b25abf131cb954fc852a444883a9
 
load_dotenv()

host = os.getenv("HOST_DB")
port = os.getenv("PORT_VALUE")
username = os.getenv("USER_APP")
pw_db = os.getenv("PASSWORD")
database = os.getenv("DATABASE")


cache = st.session_state

def validar_cpf_extenso(cpf: str) -> bool:
    # Verifica se tem 11 dígitos numéricos
    if not cpf.isdigit() or len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais (caso inválido como 11111111111)
    if cpf == cpf[0] * 11:
        return False

    # Cálculo do primeiro dígito verificador
    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10) % 11
    if digito1 == 10:
        digito1 = 0

    # Cálculo do segundo dígito verificador
    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10) % 11
    if digito2 == 10:
        digito2 = 0

    # Verifica se os dígitos batem com os dois últimos do CPF
    return cpf[-2:] == f"{digito1}{digito2}"


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

def valida_valores_dicionario(userDict: dict):
    userDict['senha'] = encriptografa_sha3_256(userDict["senha"]) 
    userDict["sexo"] = userDict["sexo"][0].upper()
    
    return userDict
            


#---------------TELA DE CADASTRO ALUNO---------------#


def tela_cadastro_aluno():
    return None


def tela_login(router: StreamlitRouter):
    
    st.header("Pumpkim Intelligence")
    with st.form(key="login e senha", enter_to_submit=False):

        login = st.text_input("Login de Usuário", placeholder="Digite seu usuário aqui")
        senha = st.text_input("Senha", type='password', placeholder="Digite sua senha aqui")
        
        col1, col2= st.columns([4.3, 1], gap="large", vertical_alignment="center")
        
        with col1:
            enter_button = st.form_submit_button(label="Entrar")
        
        with col2:
            button_cad = st.form_submit_button(label="Cadastrar")
        
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

                router.redirect(*router.build("fn_create_values"))
            
            else:
                st.error("Login ou senha inválidos")

        elif button_cad:
            popup_cadastrar()



@st.dialog("Cadastro | Pumpkim Saudável")
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

        user_cpf = st.text_input("CPF", placeholder= "Digite seu CPF aqui. (Em formato extenso)")
        if user_cpf:
            if not validar_cpf_extenso(user_cpf):
                st.error("Coloque um CPF válido.")
                st_cad_errors += 1
            
        user_date_burned = st.date_input('Data de Nascimento', value= None, format= "DD/MM/YYYY")
        user_cell_number = st.text_input("Número de Telefone", placeholder= "Ex: 1194071231...", autocomplete='tel')
        user_endereco = st.text_input("Endereço", placeholder="Ex: Rua Alfredo Neres...", autocomplete= 'street-address')
        user_sex = st.selectbox('Sexo', options= ["Masculino", "Feminino"], )
        user_cargo = st.text_input('Que cargo você ocupa?', placeholder= "Ex: Analista de Estoque...")

        user_password: str = st.text_input("Senha",type="password", placeholder="Digite sua senha aqui")
        user_password_conf: str = st.text_input("Confirmar senha", type="password",placeholder="Confirme sua senha")
        user_cad_button = st.button(label="Cadastrar", key="button_cadastrar_finish")

        if user_cad_button and not st_cad_errors:
            if user_password == user_password_conf:
                dict_funcionario = {}

                dict_funcionario['nome'] = user_cad_name
                dict_funcionario['email'] = user_cad_email
                dict_funcionario['cpf'] = user_cpf
                dict_funcionario['data_nascimento'] = user_date_burned
                dict_funcionario['numero_telefone'] = user_cell_number
                dict_funcionario['endereco'] = user_endereco
                dict_funcionario['sexo'] = user_sex
                dict_funcionario['cargo'] = user_cargo
                dict_funcionario['senha'] = user_password

                dict_funcionario = valida_valores_dicionario(dict_funcionario)
                cadastro_usuario = cad_user(dict_funcionario)
                
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
        
        cur.execute("SELECT pk_id_usuario FROM sch_privated_users.tb_usuarios WHERE usuario = %s", (userDict['email'],))
        user_auth_exists = cur.fetchone()

        if user_auth_exists:
            conn.close()
            return False
    # Inserção na tabela 'usuario' (principal)
        cur.execute('''
            INSERT INTO public.tb_funcionario (nome, cpf, data_nascimento, numero_telefone, endereco, sexo, cargo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_funcionario;
        ''', (
            userDict["nome"],
            userDict["cpf"],
            userDict["data_nascimento"],
            userDict["numero_telefone"],
            userDict["endereco"],
            userDict["sexo"],
            userDict["cargo"]
        ))

        usuario_id = cur.fetchone()[0]

        # Inserção na tabela privada
        cur.execute('''
            INSERT INTO sch_privated_users.tb_usuarios (usuario, enc_ps, id_funcionario)
            VALUES (%s, %s, %s);
        ''', (
            userDict["email"],
            userDict["senha"],
            usuario_id
        ))

        # Commit se tudo deu certo
        conn.commit()
        flag_create_user = True

    except Exception as e:
        # Rollback se qualquer erro ocorrer
        conn.rollback()
        print("Erro ao criar usuário:", e)
        flag_create_user = False 

    finally:
        # Sempre fechar a conexão
        cur.close()
        conn.close()
        return flag_create_user
    
    

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
    
    cur.execute('''SELECT us.pk_id_usuario FROM sch_privated_users.tb_usuarios us 
                WHERE 1=1
                AND us.usuario = %s 
                AND us.enc_ps = %s''', 
                (login, password_enc)
                )
    
    fetched = cur.fetchone()

    if fetched:
        return True
    
    else:
        return False