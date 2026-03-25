import streamlit as st
from datetime import date

st.set_page_config(page_title="Event Booking", layout="wide")

# 🎯 SESSION STATES
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "show_events" not in st.session_state:
    st.session_state.show_events = False

if "ticket" not in st.session_state:
    st.session_state.ticket = None

# 🔐 LOGIN PAGE
if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Simple validation (you can improve later)
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login Successful 🎉")
            st.rerun()
        else:
            st.error("Enter username & password")

# 🎉 MAIN APP AFTER LOGIN
else:
    st.title("🎉 Event Booking System")
    st.write(f"Welcome, {st.session_state.username} 💖")

    # 📅 Select Date
    selected_date = st.date_input("Select Date")

    if st.button("Show Available Events"):
        st.session_state.show_events = True

    # 🎉 Events
    events = [
        {"id":1,"title":"Music Concert","location":"Hyderabad","date":"2026-04-01","price":500,"availableSeats":100},
        {"id":2,"title":"Tech Workshop","location":"Bangalore","date":"2026-04-05","price":999,"availableSeats":50},
        {"id":3,"title":"Startup Meetup","location":"Chennai","date":"2026-04-10","price":300,"availableSeats":80},
        {"id":4,"title":"Food Festival","location":"Delhi","date":"2026-04-15","price":200,"availableSeats":150},
        {"id":5,"title":"Coding Hackathon","location":"Mumbai","date":"2026-04-20","price":0,"availableSeats":200},

        # Festivals
        {"id":6,"title":"Diwali Festival","location":"Delhi","date":"2026-11-01","price":100,"availableSeats":300},
        {"id":7,"title":"Holi Festival","location":"Mathura","date":"2026-03-10","price":200,"availableSeats":250},
        {"id":8,"title":"Christmas Carnival","location":"Goa","date":"2026-12-25","price":400,"availableSeats":180},
        {"id":7,"title":"Diwali Festival","location":"Delhi","date":"2026-11-01","price":100,"availableSeats":300},
        {"id":9,"title":"Ganesh Chaturthi","location":"Mumbai","date":"2026-09-07","price":50,"availableSeats":500},
        {"id":11,"title":"New Year Party","location":"Bangalore","date":"2026-12-31","price":800,"availableSeats":120}
    ]
    selected_date_str = str(selected_date)

    if st.session_state.show_events:
        filtered = [e for e in events if e["date"] == selected_date_str]

        if not filtered:
            st.warning("No events available on this date ❗")
        else:
            cols = st.columns(3)

            for i, e in enumerate(filtered):
                with cols[i % 3]:

                    st.markdown(f"""
                    ### {e['title']}
                    📍 {e['location']}  
                    📅 {e['date']}  
                    💰 ₹{e['price']}  
                    🎟 Seats: {e['availableSeats']}
                    """)

                    tickets = st.number_input(
                        "Tickets",
                        min_value=1,
                        step=1,
                        key=f"ticket_{e['id']}"
                    )

                    if st.button("Book Now 💖", key=e['id']):

                        if tickets > e["availableSeats"]:
                            st.error("❌ Not enough seats available!")
                        else:
                            e["availableSeats"] -= tickets

                            # 🎟 Generate Ticket
                            ticket_data = {
                                "User": st.session_state.username,
                                "Event": e["title"],
                                "Location": e["location"],
                                "Date": e["date"],
                                "Tickets": tickets,
                                "Booking ID": f"EVT{e['id']}{tickets}{selected_date.day}"
                            }

                            st.session_state.ticket = ticket_data
                            st.success("🎉 Booking Successful!")

    # 🎟 SHOW TICKET
    if st.session_state.ticket:
        st.subheader("🎟 Your Virtual Ticket")

        ticket = st.session_state.ticket

        st.markdown(f"""
        🧑 Name: {ticket['User']}  
        🎉 Event: {ticket['Event']}  
        📍 Location: {ticket['Location']}  
        📅 Date: {ticket['Date']}  
        🎟 Tickets: {ticket['Tickets']}  
        🆔 Booking ID: {ticket['Booking ID']}
        """)