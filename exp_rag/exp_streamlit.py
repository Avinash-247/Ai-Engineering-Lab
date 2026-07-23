import streamlit as st
st.header("Welcome")
st.title("Hello World")
name=st.text_input("your name")
st.write(f"Hello {name}")

st.checkbox(f"{name} please tick here ")

person = {
    "Name":"Avinash",
    "Age":21
}

st.write(person)