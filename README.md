# Bank Loan Analysis

## Project Overview
This project involves analyzing bank loan data to extract insights and provide valuable visualizations for better understanding loan applications. The analysis includes data preprocessing, visualization, and reporting through a Power BI dashboard.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Dataset](#dataset)
- [Power BI Dashboard](#power-bi-dashboard)
- [Streamlit Web Application](#streamlit-web-application)

## Technologies Used
- Python
- Pandas
- Streamlit
- SQL Server Management Studio (SSMS)
- Power BI
- NumPy

## Dataset
The dataset used for this analysis includes various features related to bank loans, such as:

- **id**: Unique identifier for the loan
- **address_state**: State where the applicant resides
- **application_type**: Type of loan application (e.g., individual, joint)
- **emp_length**: Length of employment (in years)
- **emp_title**: Job title of the applicant
- **grade**: Loan grade assigned by the lender
- **home_ownership**: Home ownership status (e.g., own, mortgage, rent)
- **issue_date**: Date the loan was issued
- **last_credit_pull_date**: Date of the last credit report pull
- **last_payment_date**: Date of the last payment made
- **loan_status**: Current status of the loan (e.g., fully paid, charged off)
- **next_payment_date**: Date of the next payment due
- **member_id**: Unique identifier for the member
- **purpose**: Purpose of the loan (e.g., debt consolidation, home improvement)
- **sub_grade**: Sub-grade of the loan
- **term**: Term of the loan (e.g., 36 months, 60 months)
- **verification_status**: Status of income verification
- **annual_income**: Applicant's annual income
- **dti**: Debt-to-income ratio
- **installment**: Monthly installment amount
- **int_rate**: Interest rate of the loan
- **loan_amount**: Total loan amount
- **total_acc**: Total number of credit accounts
- **total_payment**: Total payment amount over the term of the loan

## Power BI Dashboard
In this project, I first uploaded the dataset into SQL Server Management Studio (SSMS). In Power BI, I connected to SSMS and imported the data, then created an interactive dashboard to visualize the loan data effectively. Below are screenshots of the Power BI dashboard:

![Dashboard Screenshot 1](PowerBi_screenshots/Dashboard_1(Summary).png)
![Dashboard Screenshot 2](PowerBi_screenshots/Dashboard_2(Overview).png)
![Dashboard Screenshot 3](PowerBi_screenshots/Dashboard_3(Details).png)

## Streamlit Web Application
The project also includes a Streamlit web application that allows users to interactively explore the loan data. Key features of the application include:
- Displaying loan data with relevant metrics.
- Visualizations of different aspects of the loan data.

