import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

st.title("💰 Personal Finance Tracker")

# --- Session State for persistent data ---
if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

# --- Add Transaction Form ---
with st.form("transaction_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date")
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
    with col3:
        amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")

    submitted = st.form_submit_button("➕ Add Transaction")
    if submitted and amount > 0:
        st.session_state["transactions"].append({"Date": date, "Category": category, "Amount": amount})
        st.success("Transaction added successfully ✅")

# --- Display Data ---
if st.session_state["transactions"]:
    df = pd.DataFrame(st.session_state["transactions"])
    st.subheader("📋 Transactions")
    st.dataframe(df, use_container_width=True)

    # --- Total Expenses ---
    total = df["Amount"].sum()
    st.metric("Total Expenses", f"₹{total:.2f}")

    # --- Category-wise Chart ---
    st.subheader("📊 Expenses by Category")
    category_totals = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    category_totals.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount (₹)")
    st.pyplot(fig)

else:
    st.info("No transactions yet. Add your first one above!")

