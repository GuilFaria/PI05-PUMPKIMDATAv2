import segno
import base64
import io
import time

import streamlit as st
import datetime as dt
import psycopg2
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

host = os.getenv("HOST_DB")
port = os.getenv("PORT_VALUE")
username = os.getenv("USER_APP")
pw_db = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

cache = st.session_state

    #Melhorias:
    #Ingredientes Direto do Banco de Dados
    #Ajustar JSON para pegar usuario que criou, id_produto, id_ingrediente
    #Ajustar, no banco, qual seria a validade de cada produto
    #Considerar Entrada de Produto (tabela movimentações)

def codifica_base64(content: list | io.BytesIO | str  = str) -> list[str] | str:

    '''
    Codificação de BASE64 é feito da seguinte forma(Número não exclusivo, apenas uma máscara):
    '''
    
    if isinstance(content, str):
        try:
            content = content.encode() #Para transformar em uma string correta, utiliza-se o decode no final
            encoded_value = base64.b64encode(content).decode()
        
        except Exception as e:
            raise(f'Erro ao codificar: {e}')
                
            
    elif isinstance(content, io.BytesIO):
        try:
            encoded_value = base64.b64encode(content).decode()
        
        except Exception as e:
            raise(f'Erro ao codificar: {e}')
            
    elif isinstance(content, list):
        try:            
            encoded_value = []
            for text in content:
                text = str(text)
                text_encoded = text.encode()
                based_text = base64.b64encode(text_encoded).decode()
                encoded_value.append(based_text)

        except Exception as e:
            raise(f'Erro ao codificar: {e}')
    
    return encoded_value



def aplica_marmita_entrada(str_id_marmita: str):
    # Criação do JSON para o QRCode
    
    try:
        int_id_marmita = int(str_id_marmita)
    except Exception as e:
        st.error(f'Erro ao converter id_marmita para int: {e}')
        return
    
    json_qrcode = {}

     
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
    
    cur.execute('''SELECT id FROM public.movimentacao
                ORDER BY id DESC
                LIMIT 1''')
    
    fetched = cur.fetchone()

    while fetched is not None:
        new_id_mov = int(fetched[0]) + 1
        fetched = cur.fetchone()
    

    cur.execute('''INSERT INTO public.movimentacao(id, tipo_movimento, quantidade, id_funcionario, id_marmita)
                VALUES (%s, 'entrada', 1, %s, %s) ''',
                (new_id_mov, cache["id_funcionario"], int_id_marmita))
    
    conn.commit()
    
    
    

    json_qrcode["id"] = new_id_mov
    # json_qrcode["data_criacao"] = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # json_qrcode["ingredientes"] = str_marmita_cod

    return json_qrcode

@st.dialog('QR Code foi gerado!', width= "large")
def cria_qrcode(json_qrcode):

    path = r'C:\Users\guilh\Desktop\Projetos\Home\PI05 - PumpkimDataV2\stage\images\temp_qcode'
    date_format = '%d_%m_%Y_%H_%M_%S'
    date_atual = dt.datetime.now().strftime(date_format)
    
    video = segno.make(str(json_qrcode), micro= False)


    qr_code_temp = fr'{path}\temp{date_atual}.png'



    video.save(qr_code_temp, dark="yellow", light="#323524", scale=15)

    st.subheader('', divider= 'orange')
    st.write("_Certifique-se de fazer o Download e imprima-o no produto/marmita cadastrada._")
    colunas = st.columns(3)
    with colunas[1]:
        with open(qr_code_temp, 'rb') as f:
            donwload_archives = io.BytesIO(f.read())
            
        st.image(donwload_archives)
        st.download_button("Download QRCode", donwload_archives, file_name="qrcode.png", mime="image/png")

def fn_cria_lista_marmitas():
    # Criação da lista de ingredientes para o QRCode
    dict_marmitas = {}
    
    
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
    
    cur.execute('''SELECT marmita_id, descricao FROM public.marmitas''')
    
    fetched = cur.fetchone()

    while fetched is not None:

        dict_marmitas[fetched[1]] = fetched[0]
        fetched = cur.fetchone()
    
    time.sleep(2.5)
    return dict_marmitas


def fn_create_values():

    nome_func = cache['nome_funcionario']
    nome_func = nome_func.split(' ')[0].capitalize()


    st.image(r'C:\Users\guilh\Desktop\Projetos\Home\PI05 - PumpkimDataV2\stage\images\stage_images\pumpkim_logo.png')
    st.subheader('Pumpkim Intelligence | Controle de Estoque', divider= 'grey')
    st.write(f'_Olá, **{nome_func}**!_')

    st.write('')
    
    dict_marmitas = fn_cria_lista_marmitas()
    list_marmitas = list(dict_marmitas.keys())
    
    str_marmita_seleted = st.selectbox('Selecione o tipo de marmita retirada.', list_marmitas)
    
    enviar = st.button('Enviar')

    if enviar:
        
        id_marmita_selected = dict_marmitas.get(str_marmita_seleted)
        json_qrcode = aplica_marmita_entrada(id_marmita_selected)
        
        cria_qrcode(json_qrcode)