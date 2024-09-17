import requests
import streamlit as st

data = requests.get("https://intranet.portodesantos.com.br/_json/operadores.asp").json()

st.write(data)
