# Indian Flight Dashboard — Python, SQL & Streamlit

An interactive data analytics dashboard for visualizing **domestic flight operations** between **Indian international airports**. Built with **Python**, **SQL**, and **Streamlit**, this web app provides rich insights into airline routes, airport ownership, fare trends, and flight frequencies.

---

##  Features

### Check Flights
- Select source and destination airports
- View available flights with airline, cabin class, timings, fare, and stops

###  Analytics Section
Includes multiple interactive visualizations:
- **Airline-wise Analysis of Flights**
- **Airline-wise Analysis Between Two Airports**
- **Busiest International Airports in India**
- **Hourly Flight Departures from Airports**
- **Average Fare Analysis Between Two Airports**
- **Ownership Details of Airports**

###  Name and Ownership of Airports
- View a DataFrame of all Indian international airports and their managing authorities (e.g., AAI, Adani Group, GMR)
- Search ownership of a specific airport

---

## Dataset

**Source:** [Kaggle - Flights Between Indian International Airports](https://www.kaggle.com/datasets/karanveer59/flights-between-indian-international-airports)  
**Description:**  
> This dataset contains domestic flights operating between Indian international airports on **16th July 2025**, scraped from [EaseMyTrip.com](https://www.easemytrip.com). It includes flight numbers, airlines, cabin class, departure/arrival times, duration, fare, and airport ownership info.

---

## 💻 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python
- **Database**: MySQL (via Pandas + pymysql)
- **Visualization**: [Plotly](https://plotly.com/)
