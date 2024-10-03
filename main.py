import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

# Load Data
df = pd.read_csv("S:/DS/projects/Bank_loan_analysis/financial_loan.csv")

# Streamlit setup
st.set_page_config(page_title="Bank Loan Analysis", layout="wide")
st.title("Bank Loan Analysis")
st.divider()

# Sidebar menu
with st.sidebar:
    selected_menu = option_menu("Menu", ["Home", "Analysis", "About"],
                                 icons=['house', 'activity', 'info-circle-fill'],
                                 menu_icon="cast", default_index=1)

def display_key_metrics():
    #Calculate and display key metrics related to loan applications.
    total_loan_applications = df['id'].count() / 1000  
    total_funded_amount = df['loan_amount'].sum() / 1000000
    total_amount_received = df['total_payment'].sum() / 1000000
    average_interest_rate = df['int_rate'].mean() * 100
    average_dti = df['dti'].mean() * 100

    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(":blue[Total Loan Applications]", f"{total_loan_applications:,.2f}K")
    col2.metric(":blue[Total Funded Amount]", f"${total_funded_amount:,.2f}M")
    col3.metric(":blue[Total Amount Received]", f"${total_amount_received:,.2f}M")
    col4.metric(":blue[Average Interest Rate]", f"{average_interest_rate:,.2f}%")
    col5.metric(":blue[Average DTI]", f"{average_dti:,.2f}%")
    st.divider()

def good_vs_bad_loans():
    #Display metrics and visualizations for good and bad loans.
    st.write("### Good Vs Bad Loan Issued") 
    good_loans = df[df['loan_status'].isin(['Fully Paid', 'Current'])]
    bad_loans = df[df['loan_status'] == 'Charged Off']

    # Good and Bad Loans breakdown
    good_loan_count = len(good_loans)
    bad_loan_count = len(bad_loans)

    good_loan_funded = good_loans['loan_amount'].sum()
    bad_loan_funded = bad_loans['loan_amount'].sum()

    good_total_received = good_loans['total_payment'].sum()
    bad_total_received = bad_loans['total_payment'].sum()

    # Donut chart for Good vs Bad Loan
    labels = ['Good Loans', 'Bad Loans']
    total_loans = df['id'].count()
    values = [good_loan_count / total_loans * 100, bad_loan_count / total_loans * 100]

    fig = px.pie(
        names=labels, 
        values=values, 
        hole=0.5, 
        color=labels, 
        color_discrete_map={'Good Loans':'#FFA500', 'Bad Loans':'#1f77b4'}
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(showlegend=False)

    # Display Donut Chart and Metrics
    col1, col2, col3 = st.columns([6, 3, 3])
    with col1:
        st.plotly_chart(fig, use_container_width=True)

    # Display Key Metrics for Good and Bad Loans
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.metric("Good Loan Applications", f"{good_loan_count:,}")
        st.metric("Good Loan Funded Amount", f"${good_loan_funded / 1_000_000:,.2f}M")
        st.metric("Good Loan Received Amount", f"${good_total_received / 1_000_000:,.2f}M")

    with col3:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.metric("Bad Loan Applications", f"{bad_loan_count:,}")
        st.metric("Bad Loan Funded Amount", f"${bad_loan_funded / 1_000_000:,.2f}M")
        st.metric("Bad Loan Received Amount", f"${bad_total_received / 1_000_000:,.2f}M")

    st.divider()

def display_loan_status_summary():
    #Display the loan status summary in an attractive format.
    loan_status_summary = df.groupby('loan_status').agg({
        'id': 'count',
        'loan_amount': 'sum',
        'total_payment': 'sum',
        'int_rate': 'mean',
        'dti': 'mean'
    }).reset_index()

    loan_status_summary.columns = ['Loan Status', 'Total Loan Applications', 'Total Funded Amount', 'Total Amount Received', 'Avg Interest Rate', 'Avg DTI']
    
    # Format the DataFrame for better presentation
    formatted_summary = loan_status_summary.style.format({
        'Total Loan Applications': '{:,.0f}',
        'Total Funded Amount': '${:,.2f}',
        'Total Amount Received': '${:,.2f}',
        'Avg Interest Rate': '{:.2f}%',  
        'Avg DTI': '{:.2f}%'  
    })


    loan_status_summary['Avg Interest Rate'] = loan_status_summary['Avg Interest Rate'] * 100
    loan_status_summary['Avg DTI'] = loan_status_summary['Avg DTI'] * 100

    st.subheader("Loan Status Summary")
    st.dataframe(formatted_summary, use_container_width=True)

    st.divider()

def monthly_trend_analysis():
    #Display analysis of loan applications over time.
    df['issue_date'] = pd.to_datetime(df['issue_date'], format='%d-%m-%Y', errors='coerce')
    df['Month'] = df['issue_date'].dt.to_period('M').astype(str)

    # Measure selection
    measure_options = ["Total Loan Applications", "Total Amount Received", "Total Funded Amount"]
    selected_measure = st.selectbox("Select Measure:", measure_options, key="monthly_trend_measure")

    # Calculate values based on selected measure
    if selected_measure == "Total Loan Applications":
        measure_values = df.groupby('Month')['id'].count().reset_index(name='Total Loan Applications')
    elif selected_measure == "Total Amount Received":
        measure_values = df.groupby('Month')['total_payment'].sum().reset_index(name='Total Amount Received')
    else:
        measure_values = df.groupby('Month')['loan_amount'].sum().reset_index(name='Total Funded Amount')

    # Area Chart for selected measure
    area_chart = px.area(
        measure_values,
        x='Month',
        y=measure_values.columns[1],
        title=f'{selected_measure} Over Time',
        labels={measure_values.columns[1]: selected_measure},
        markers=True
    )

    # Update x-axis to show abbreviated month names
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    tickvals = measure_values['Month'].unique()
    month_mapping = {f'{i:02d}': month_names[i - 1] for i in range(1, 13)}

    area_chart.update_xaxes(
        tickvals=tickvals,
        ticktext=[month_mapping.get(month.split('-')[1], month) for month in tickvals]
    )

    st.plotly_chart(area_chart)

    st.divider()

def employee_length_analysis(selected_measure):
    #Display analysis of loans based on employee length.
    if selected_measure == "Total Loan Applications":
        employee_length_values = df.groupby('emp_length')['id'].count().reset_index(name='Number of Applications')
    elif selected_measure == "Total Amount Received":
        employee_length_values = df.groupby('emp_length')['total_payment'].sum().reset_index(name='Total Amount Received')
    else:
        employee_length_values = df.groupby('emp_length')['loan_amount'].sum().reset_index(name='Total Funded Amount')

    # Sort the values in descending order
    employee_length_values = employee_length_values.sort_values(by=employee_length_values.columns[1])

    # Horizontal Bar Chart for Employee Length
    horizontal_bar_chart = px.bar(
        employee_length_values,
        x=employee_length_values.columns[1],
        y='emp_length',
        orientation='h',
        title=f'Employees by Length of Service ({employee_length_values.columns[1]})',
        labels={'emp_length': 'Length of Service (Years)', employee_length_values.columns[1]: employee_length_values.columns[1]},
    )

    st.plotly_chart(horizontal_bar_chart)

    st.divider()

def loan_purpose_analysis(selected_measure):
    #Display analysis of loans based on purpose.
    if selected_measure == "Total Loan Applications":
        purpose_values = df.groupby('purpose')['id'].count().reset_index(name='Number of Applications')
    elif selected_measure == "Total Amount Received":
        purpose_values = df.groupby('purpose')['total_payment'].sum().reset_index(name='Total Amount Received')
    else:
        purpose_values = df.groupby('purpose')['loan_amount'].sum().reset_index(name='Total Funded Amount')

    # Sort the values in descending order
    purpose_values = purpose_values.sort_values(by=purpose_values.columns[1])

    # Horizontal Bar Chart for Loan Purpose
    purpose_horizontal_bar_chart = px.bar(
        purpose_values,
        x=purpose_values.columns[1],
        y='purpose',
        orientation='h',
        title=f'Loan Purpose Analysis ({purpose_values.columns[1]})',
        labels={'purpose': 'Loan Purpose', purpose_values.columns[1]: purpose_values.columns[1]},
    )

    st.plotly_chart(purpose_horizontal_bar_chart)

    st.divider()

def loan_term_analysis_donut():
    #Display a donut chart for loan terms.
    term_counts = df['term'].value_counts().reset_index()
    term_counts.columns = ['Term', 'Count']

    # Donut chart
    donut_chart = px.pie(
        term_counts, 
        names='Term', 
        values='Count', 
        hole=0.5, 
        color=term_counts['Term'],
        color_discrete_sequence=px.colors.qualitative.Plotly  # Use a color sequence
    )
    donut_chart.update_traces(textinfo='percent+label')
    donut_chart.update_layout(title_text="Loan Term Distribution", title_x=0.5)

    st.plotly_chart(donut_chart)

    st.divider()



def loan_data_display():
    columns_to_display = ['id', 'purpose', 'home_ownership', 'grade', 'sub_grade', 'issue_date', 'loan_amount', 
                          'int_rate', 'installment', 'total_payment']
    
    # Select specific columns
    df_selected = df[columns_to_display].copy()
    
    # Convert issue_date to datetime and use .loc to avoid SettingWithCopyWarning
    df_selected.loc[:, 'issue_date'] = pd.to_datetime(df_selected['issue_date']).dt.date
    
    # Renaming columns
    df_selected.rename(columns={
        'id': 'Loan ID',
        'purpose': 'Loan Purpose',
        'home_ownership': 'Home Ownership',
        'grade': 'Loan Grade',
        'sub_grade': 'Sub Grade',
        'issue_date': 'Issue Date',
        'loan_amount': 'Loan Amount',
        'int_rate': 'Interest Rate',
        'installment': 'Installment Amount',
        'total_payment': 'Total Payment'
    }, inplace=True)

    # Displaying the dataframe attractively in Streamlit
    st.write("### Loan Data")
    st.dataframe(df_selected)

    st.divider()

# Render content based on selected menu
if selected_menu == "Home":
    st.subheader("Welcome to the Bank Loan Analysis App")
    st.write("""
        This application provides insights into loan data collected from various applicants.
        You can explore key metrics, analyze loan statuses, and view trends over time.
        
        Use the navigation menu to access different analyses and visualize the data.
    """)
    #st.image("path_to_image/logo.png", width=200)  # Add an image, if applicable

elif selected_menu == "Analysis":
    # Display Key Metrics
    display_key_metrics()

    # Good vs Bad Loans
    good_vs_bad_loans()
    display_loan_status_summary()
    # Monthly Trend Analysis
    st.subheader("Monthly Trend Analysis")
    monthly_trend_analysis()

    # Employee Length Analysis
    st.subheader("Employee Length Analysis")
    employee_length_measure = st.selectbox("Select Measure:", ["Total Loan Applications", "Total Amount Received", "Total Funded Amount"], key="employee_length_measure")
    employee_length_analysis(employee_length_measure)

    # Loan Purpose Analysis
    st.subheader("Loan Purpose Analysis")
    purpose_measure = st.selectbox("Select Measure:", ["Total Loan Applications", "Total Amount Received", "Total Funded Amount"], key="loan_purpose_measure")
    loan_purpose_analysis(purpose_measure)

    # Loan Term Analysis
    st.subheader("Loan Term Analysis")
    loan_term_analysis_donut()  # Display the donut chart for loan terms

    # Display Loan Status Summary Attractively
    

    loan_data_display()

elif selected_menu == "About":
    st.write("### About the Project")

    st.write("""
    This project provides a comprehensive analysis of bank loan data, focusing on key attributes such as loan purpose, home ownership,
    loan grades, issue dates, interest rates, and payment amounts. The objective is to identify trends, correlations, and insights
    that can aid in loan decision-making.
    
    In addition to the analysis presented here, a detailed Power BI dashboard has been created to visualize the bank loan data, 
    offering interactive insights into various loan categories, payments, and other financial metrics.
    """)

    st.write("### Power BI Dashboard Screenshots")
    
    # Displaying the screenshots
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("S:/DS/projects/Bank_loan_analysis/PowerBi/Summary.png", caption="Summary", use_column_width=True)

    with col2:
        st.image("S:/DS/projects/Bank_loan_analysis/PowerBi/Overview.png", caption="Overview", use_column_width=True)

    with col3:
        st.image("S:/DS/projects/Bank_loan_analysis/PowerBi/Details.png", caption="Details", use_column_width=True)
