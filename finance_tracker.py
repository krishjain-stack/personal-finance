import streamlit as st
import pandas as pd

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

st.title("💰 Personal Finance Tracker")

# --- Session State for persistent data ---
if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

# --- Add Transaction Form ---
with st.form("transaction_form"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        date = st.date_input("Date")
    with col2:
        txn_type = st.selectbox("Type", ["Income", "Expense"])
    with col3:
        category = st.text_input("Category (e.g. Food, Salary, Rent, etc.)")
    with col4:
        amount = st.number_input("Amount (₹)", min_value=0, step=1)  # no decimal formatting

    submitted = st.form_submit_button("➕ Add Transaction")
    if submitted and amount > 0:
        st.session_state["transactions"].append({
            "Date": date,
            "Type": txn_type,
            "Category": category if category else "Other",
            "Amount": amount
        })
        st.success("Transaction added successfully ✅")

# --- Display Data ---
if st.session_state["transactions"]:
    df = pd.DataFrame(st.session_state["transactions"])
    st.subheader("📋 Transactions")
    st.dataframe(df, use_container_width=True)

    # --- Summary ---
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expenses = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{income}")
    col2.metric("Total Expenses", f"₹{expenses}")
    col3.metric("Balance", f"₹{balance}")

    # --- Charts ---
    st.subheader("📊 Expenses by Category")
    expense_data = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().reset_index()
    if not expense_data.empty:
        st.bar_chart(expense_data, x="Category", y="Amount")
    else:
        st.info("No expenses recorded yet.")

    st.subheader("📈 Income vs Expenses Over Time")
    time_data = df.groupby(["Date", "Type"])["Amount"].sum().reset_index()
    st.line_chart(time_data, x="Date", y="Amount", color="Type")

else:
    st.info("No transactions yet. Add your first one above!")

