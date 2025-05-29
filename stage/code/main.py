import streamlit as st
from streamlit_router import StreamlitRouter


from login import tela_login
from processes.create_qrcode import fn_create_values

cache = st.session_state

st.set_page_config(page_title= 'Pumpkim Intelligence', page_icon= ':material/nutrition:', layout= "wide")

router = StreamlitRouter()

router.register(tela_login, "/")
router.register(fn_create_values, "/main")
router.serve()