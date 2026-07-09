import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mortgage Calculator", page_icon="🏠")

st.title("🏠 Simple Mortgage Calculator")
st.write("This app helps you understand basic mortgage repayments.")

# Inputs
house_price = st.number_input(
    "House price (£)",
    min_value=0,
    value=250000,
    step=1000
)

deposit = st.number_input(
    "Deposit (£)",
    min_value=0,
    value=25000,
    step=1000
)

interest_rate = st.number_input(
    "Annual interest rate (%)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

mortgage_years = st.slider(
    "Mortgage term (years)",
    min_value=1,
    max_value=40,
    value=25,
    step=1
)

# Calculations
loan_amount = house_price - deposit
monthly_interest_rate = interest_rate / 100 / 12
number_of_payments = mortgage_years * 12

if loan_amount <= 0:
    st.warning("Your deposit is equal to or greater than the house price.")
else:
    if monthly_interest_rate == 0:
        monthly_payment = loan_amount / number_of_payments
    else:
        monthly_payment = loan_amount * (
            monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments
        ) / (
            (1 + monthly_interest_rate) ** number_of_payments - 1
        )

    total_paid = monthly_payment * number_of_payments
    total_interest = total_paid - loan_amount

    st.subheader("Mortgage Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Loan amount", f"£{loan_amount:,.2f}")
    col2.metric("Monthly payment", f"£{monthly_payment:,.2f}")
    col3.metric("Total interest", f"£{total_interest:,.2f}")

    st.write(f"Total amount paid over {mortgage_years} years: **£{total_paid:,.2f}**")

    # Amortisation table
    balance = loan_amount
    data = []

    for month in range(1, number_of_payments + 1):
        interest_payment = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment

        if balance < 0:
            balance = 0

        data.append({
            "Month": month,
            "Year": (month - 1) // 12 + 1,
            "Monthly Payment (£)": monthly_payment,
            "Interest Paid (£)": interest_payment,
            "Principal Paid (£)": principal_payment,
            "Remaining Balance (£)": balance
        })

    df = pd.DataFrame(data)

    st.subheader("Remaining Mortgage Balance Over Time")
    yearly_df = df.groupby("Year")["Remaining Balance (£)"].last().reset_index()
    st.line_chart(yearly_df, x="Year", y="Remaining Balance (£)")

    st.subheader("Amortisation Table")
    st.dataframe(df.style.format({
        "Monthly Payment (£)": "£{:,.2f}",
        "Interest Paid (£)": "£{:,.2f}",
        "Principal Paid (£)": "£{:,.2f}",
        "Remaining Balance (£)": "£{:,.2f}"
    }))