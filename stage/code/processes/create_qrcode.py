import segno
import base64
import io

import streamlit as st
import datetime as dt

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



def cria_json_qrcode(dict_ingredientes):
    # Criação do JSON para o QRCode
    
    json_qrcode = {}

    json_qrcode["email"] = cache["login"]
    json_qrcode["data_criacao"] = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    json_qrcode["ingredientes"] = dict_ingredientes

    return json_qrcode

@st.dialog('QR Code foi gerado!', width= "large")
def cria_qrcode(json_qrcode):

    path = r'C:\Users\guilh\Desktop\Projetos\Home\PI05 - PumpkimDataV2\stage\images\temp_qcode'
    date_format = '%d_%m_%Y_%H_%M_%S'
    date_atual = dt.datetime.now().strftime(date_format)
    
    video = segno.make(codifica_base64(str(json_qrcode)), micro= False)

    video.save(fr'{path}\temp{date_atual}.png', dark="yellow", light="#323524", scale=15)

    st.subheader('', divider= 'orange')
    st.write("_Certifique-se de fazer o Download e imprima-o no produto/marmita cadastrada._")
    colunas = st.columns(3)
    with colunas[1]:
        st.image(fr'{path}\temp{date_atual}.png')

def fn_create_values():

    
    st.image(r'C:\Users\guilh\Desktop\Projetos\Home\PI05 - PumpkimDataV2\stage\images\stage_images\pumpkim_logo.png')
    st.subheader('Pumpkim Intelligence | Controle de Estoque')
    
    list_ingredients = ['Cenora', 'Tomate', 'Pepino', 'Alface', 'Brocolis', 'Beterraba', 'Açafrão', 'Escarrola']

    
    list_ingredients_selected = st.multiselect('Selecione os ingredientes', list_ingredients)
    
    dict_valores = {}

    if len(list_ingredients_selected) >= 1:

        for ingrediente in list_ingredients_selected:
            st.divider()
            peso = st.slider(f'Selecione a quantidade do **{ingrediente}** - (Em gramas):', min_value= 1, max_value= 1000, value= 100, step= 1, )
            dict_valores[ingrediente] = peso

        enviar = st.button('Criar QR Code')

        if enviar:
            
            json_qrcode = cria_json_qrcode(dict_valores)
            
            cria_qrcode(json_qrcode)
            