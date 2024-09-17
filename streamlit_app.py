import streamlit as st
import datetime
import pywhatkit as py

phonelist = st.text_input("Please input numbers you want to automate with seperated by ,")
message = st.text_area("Enter your Message")
submit = st.button("Enter")

i=1
if submit:
phone = phonelist.split(',')
for each in phone:
py.sendwhatmsg("+55"+each,message,time.hour,(time.minute+i),10)
i=i+1
st.success("Message Sent!")
