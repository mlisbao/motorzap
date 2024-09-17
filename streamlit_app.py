import streamlit as st
import pandas as pd
import requests
from twilio.rest import Client

# Função para buscar dados da API e converter para DataFrame
def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Verifica se houve algum erro na requisição
        data = response.json()  # Supondo que a API retorne dados em formato JSON
        df = pd.DataFrame(data)  # Converte os dados para DataFrame
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return None

# Função para comparar dois dataframes
def compare_dataframes(df1, df2):
    # Comparar os DataFrames e retornar as diferenças
    diff = df1.compare(df2, keep_shape=True, keep_equal=False)
    return diff

# Função para enviar mensagem no WhatsApp
def send_whatsapp_message(to_number, message_body):
    account_sid = 'SEU_ACCOUNT_SID_AQUI'  # Substitua pelo seu Account SID
    auth_token = 'SEU_AUTH_TOKEN_AQUI'    # Substitua pelo seu Auth Token
    client = Client(account_sid, auth_token)

    from_whatsapp_number = 'whatsapp:+14155238886'  # Número WhatsApp Twilio
    to_whatsapp_number = f'whatsapp:{to_number}'    # Número para o qual deseja enviar

    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

    return message.sid

# Interface do Streamlit
st.title("Comparador de DataFrames de APIs com Notificação via WhatsApp")

# Entrada para URLs das APIs
api_url_1 = st.text_input("Insira a URL da primeira API", "")
api_url_2 = st.text_input("Insira a URL da segunda API", "")

# Verificar se as URLs foram fornecidas
if api_url_1 and api_url_2:
    st.write("Buscando dados das APIs...")

    # Buscar os dados das duas APIs
    df1 = fetch_data_from_api(api_url_1)
    df2 = fetch_data_from_api(api_url_2)

    if df1 is not None and df2 is not None:
        # Exibir os DataFrames obtidos
        st.write("Primeiro DataFrame:")
        st.dataframe(df1)

        st.write("Segundo DataFrame:")
        st.dataframe(df2)

        # Comparar os DataFrames
        st.write("Comparando os DataFrames...")
        differences = compare_dataframes(df1, df2)

        if not differences.empty:
            st.write("Diferenças encontradas:")
            st.dataframe(differences)

            # Input para número do WhatsApp
            to_number = st.text_input("Número do WhatsApp para notificação (inclua o código do país)", "+55")

            # Enviar notificação via WhatsApp
            if st.button("Enviar notificação via WhatsApp"):
                message_body = f"Diferenças encontradas entre os DataFrames: {differences.to_string()}"
                try:
                    message_sid = send_whatsapp_message(to_number, message_body)
                    st.success(f"Mensagem enviada com sucesso! SID: {message_sid}")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao enviar a mensagem: {e}")
        else:
            st.write("Nenhuma diferença encontrada entre os DataFrames.")
    else:
        st.error("Erro ao carregar os dados das APIs. Verifique as URLs.")


