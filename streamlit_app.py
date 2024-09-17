import streamlit as st
from twilio.rest import Client

# Função para enviar mensagem no WhatsApp
def send_whatsapp_message(to_number, message_body):
    account_sid = 'ACf5c5464b9e54cfa3a70c9b444f7a54e4'  # Substitua pelo seu Account SID
    auth_token = 'b819f29e814194d7fc965ed21f4745ef'    # Substitua pelo seu Auth Token
    client = Client(account_sid, auth_token)

    from_whatsapp_number = 'whatsapp:+14155238886'  # Número WhatsApp Twilio
    to_whatsapp_number = f'whatsapp:{to_number}'    # Número para o qual deseja enviar

    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

    return message.sid

# Configurando a interface do Streamlit
st.title("Envio de Mensagens no WhatsApp")
st.write("Envie mensagens diretamente pelo WhatsApp usando Twilio.")

# Input para o número do destinatário
to_number = st.text_input("Número do destinatário (inclua o código do país)", "+55")  # Exemplo para Brasil
message_body = st.text_area("Digite sua mensagem")

if st.button("Enviar Mensagem"):
    if to_number and message_body:
        try:
            message_sid = send_whatsapp_message(to_number, message_body)
            st.success(f"Mensagem enviada com sucesso! SID: {message_sid}")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("Por favor, insira o número e a mensagem.")

