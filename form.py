import streamlit as st
with st.form("registration_form"):
    st.title("Registration Form")
    c1,c2=st.columns(2)
    with c1:
        n1=st.text_input("Enter your first name")
    with c2:
        n2=st.text_input("Enter your last name")
    em=st.text_input("Enter your Email")
    p=st.text_input("Password", type="password")
    c=st.text_input("Confirm Password", type="password")
    ad=st.text_area("Enter address")
    submit=st.form_submit_button("Submit")
    if submit:
        if p==c:
            st.write(n1)
            st.write(n2)
            st.write(em)
            st.write(ad)
        else:
            st.error("Passwords do not match!")
