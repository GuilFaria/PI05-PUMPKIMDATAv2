# import streamlit as st
# import segno
# import io
# from PIL  import Image

# st._config()
import streamlit as st
import os

from streamlit_router import StreamlitRouter

from login import tela_login


cache = st.session_state

st.set_page_config(page_title= 'SIPA', page_icon= ':smile:')


router = StreamlitRouter()


router.register(tela_login, "/")
router.register(teste_main, "/main")


router.serve()



# def fn_create_values():

#     st.image(r'C:\Users\guilh\Desktop\Projetos\Home\PI05 - PumpkimDataV2\stage\images\stage_images\pumpkim_logo.png')
#     st.subheader('Pumpkim Intelligence | Controle de Estoque')
    
#     list_ingredients = ['Cenora', 'Tomate', 'Pepino', 'Alface', 'Brocolis', 'Beterraba', 'Açafrão', 'Escarrola']

    
#     list_ingredients_selected = st.multiselect('Selecione os ingredientes', list_ingredients)
    
#     dict_valores = {}

#     if len(list_ingredients_selected) >= 1:

#         for ingrediente in list_ingredients_selected:
#             st.divider()
#             peso = st.slider(f'Selecione a quantidade do **{ingrediente}** - (Em gramas):', min_value= 1, max_value= 1000, value= 100, step= 1, )
#             dict_valores[ingrediente] = peso

#         enviar = st.button('Enviar')

#         if enviar:

#             st.write('**Quantidade de ingredientes selecionados:**', len(list_ingredients_selected))
#             st.write('**Ingredientes selecionados:**', list_ingredients_selected)
#             st.write('**Quantidade de cada ingrediente:**', peso)
#             st.json(dict_valores)

            
#             video = segno.make(str(dict_valores), micro= False)
#             video.save(r'C:\Users\guilh\Desktop\Projetos\Home\PI05 - PumpkimDataV2\stage\images\temp_qrcodes\Video.png', dark="yellow", light="#323524", scale=15, )


#             st.write('Comprar o arquivo de dados')
#             st.image(r'C:\Users\guilh\Desktop\Projetos\Home\PI05 - PumpkimDataV2\stage\images\temp_qrcodes\Video.png', )


#     #Formatos
#     #Quantidade





# fn_create_values()

# # # bytes_image = io.BytesIO(video)