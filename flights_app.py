import streamlit as st 
from database_helper import DB
import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd
import numpy as np


connection = DB()

st.set_page_config(layout='wide',page_title="Indian International Airport Analytics Dashboard")

class Main:
    def __init__(self):
        st.sidebar.title('Flights Analysis')
        
        
    def main_page(self):
        menu = st.sidebar.selectbox('Menu',['About','Check Flights','Analytics','Name and Ownership of Airport'])

        if menu == 'About':
            self.about()
        elif menu == 'Check Flights':
            self.check_flights()
        elif menu == 'Analytics':
            self.analysis()
        elif menu == 'Name and Ownership of Airport':
            self.about_airport()
            
            
    def check_flights(self):
        st.title("Check Flights")
        city = connection.name_of_cities()
        col1,col2 = st.columns(2)
        with col1:
            source = st.selectbox('Source', sorted(city))
        
        with col2:
            destination = st.selectbox('Destination',sorted(city))
            
        if st.button('Search Flights'):
            if source != destination:
                flights = connection.show_flights(source, destination)
                st.dataframe(flights, height=600, use_container_width=True)
            else:
                st.write('Source and Destionation can not be same')
    
    def analysis(self):
        
        analysis_select = st.sidebar.selectbox("Analysis Menu",["Airline-wise Analysis of Flights", "Airline-wise Analysis of Flights Between Two Airports", "Busiest International Airports in India","Hourly Flight Departures from Airports","Average Fare Analysis Between Two Airports","Check Airport Ownership Details"])
        st.title("Analytics")
        if analysis_select == 'Airline-wise Analysis of Flights':
            self.airline_wise()
        elif analysis_select == 'Airline-wise Analysis of Flights Between Two Airports':
            self.airline_wise_analysis_two()
        elif analysis_select == 'Busiest International Airports in India':
            self.busiest_airport()
        elif analysis_select == 'Hourly Flight Departures from Airports':
            self.hourly_departure()
        elif analysis_select == 'Average Fare Analysis Between Two Airports':
            self.average_fair()
        elif analysis_select == "Check Airport Ownership Details":
            self.airport_owned()
    
    def airline_wise(self):
        st.subheader('Airline-wise Flight Distribution Across Indian International Airports')
        airline, count = connection.flights_pie()
        # fig = px.pie(values=count, labels=airline, hover_name=airline, title='Airline-wise Distribution of Flights Between Two Airports')
        fig = go.Figure(go.Pie(values=count, labels=airline))
        st.plotly_chart(fig)

  
      
    def airline_wise_analysis_two(self):
        st.subheader("Airline-wise Analysis of Flights Between Two Airports")
        city = connection.name_of_cities()
        col1, col2 = st.columns(2)
        with col1:
            source= st.selectbox('Source', sorted(city))
        
        with col2:
            destination= st.selectbox('Destination',sorted(city))
            
        if st.button("Perform Analysis"):
            if source != destination:
                airline, count = connection.flights_pies(source, destination)
                # fig = px.pie(values=count, labels=airline, hover_name=airline, title=f'Airline Analysis Between ')
                fig = go.Figure(go.Pie(values= count , labels= airline,title=f'Airline-wise Analysis of Flights {source} and {destination}'))
                st.plotly_chart(fig)

            else:
                st.write('Source and Destionation can not be same')

    
    def busiest_airport(self): 
        st.subheader("Busiest International Airports in India")
        airports, frequency1 = connection.bussiest_airport()
        fig1 = px.bar(x=airports, y=frequency1,labels={'x':"Airport Name",'y':"Number of Flights"})
        st.plotly_chart(fig1)
          
    def hourly_departure(self):  
        st.subheader("Hourly Flights Departures from Airports")
        hour, frequency2 = connection.hourly_departure()
        fig2 = px.line(x=hour, y=frequency2,text=frequency2,labels={'x':"Hours",'y':"Number of Flights"})
        st.plotly_chart(fig2)
            
        st.subheader("Hourly Flight Departures from Particular Airport")
        if 'hourly_dep' not in st.session_state:
            st.session_state.hourly_dep = False
        if st.button("View "):
            st.session_state.hourly_dep = True
        if st.session_state.hourly_dep:
            city = connection.name_of_cities()
            col1, col2 = st.columns(2)
            with col1:
                source1 = st.selectbox('Source', sorted(city))
                if st.button("View Hourly Details for Selected Airport"):
                    hours_particalar, frequency3 = connection.hourly_departure_for_particular(source1)
                    fig3 = px.line(x=hours_particalar, y=frequency3, text=frequency3, labels={'x':"Hours",'y':"Number of Flights"})   
                    st.plotly_chart(fig3)
     
    def average_fair(self):
        st.subheader("Average Fare Analysis Between Two Airports")
        city = connection.name_of_cities()
        # city.insert(0,'Select One')
        col1,col2 = st.columns(2)
        with col1:
            source = st.selectbox('Source', sorted(city))
        
        with col2:
            destination = st.selectbox('Destination',sorted(city))
        # def avg(*values)::
                
        if st.button('View'):
            if source != destination:
                flights = connection.average_fare(source, destination)
                fig4 = (px.sunburst(flights, path=['Airline', 'Cabin_Class', 'Fare'], values='Fare', title=f'Average Fare by Airline and Cabin Class Between {source} and {destination}'))
                st.plotly_chart(fig4)
            else:
                st.write('Source and Destionation can not be same')
    
    def airport_owned(self):
        st.subheader("Ownership of International Airports in India")
        owners = connection.airport_owners()
        fig5 = px.pie(owners, values='Total_Ports', names='Managing_Authority')
        fig5.update_layout(showlegend=True)
        st.plotly_chart(fig5)


    def about_airport(self):
        data = connection.about_airports()
        st.dataframe(data, height=600, use_container_width=True)
        
        st.subheader("Check For Particular Airport")
        city1 = connection.name_of_cities()
        col1 = st.columns(1)[0]
        with col1:
            source = st.selectbox('Source', (city1))
        if st.button('Check'):  
            data1 = connection.check_about(source)
            airport = data1['Departure_Port'].values[0]
            name = data1['Dep_Port_Name'].values[0]
            managment = data1['Dep_Port_Owned_by'].values[0]
            st.subheader(f"Airport \u27A1 {airport}")
            st.subheader(f'Name \u27A1 {name}')
            st.subheader(f'Managing_Authority \u27A1 {managment}')
            
    def about(self):
        st.header("About the Website")
        st.write("""This website is an interactive data visualization platform built using Streamlit and SQL
                 to analyze and explore flight operations between Indian international airports.
                 The core data powering this application comes from the Kaggle dataset:
                "https://www.kaggle.com/datasets/karanveer59/flights-between-indian-international-airports"
                This dataset provides detailed information about domestic flights operating 
                between India's international airports on 16th July 2025, originally scraped from
                "https://www.easemytrip.com" for educational and research purposes. 
                It offers a comprehensive snapshot of scheduled flight activity for that specific day""")
        st.header("Website Features")
        st.subheader("Check Flights")
        st.write("""\u27A1Select two airports (source and destination) to view all flights operating between them.""")
        st.write('\u27A1Displays details such as airline name, cabin class, departure and arrival times, flight duration, stops, and fare.')
        st.subheader("Analytics")
        st.write("This section provides insightful visualizations based on multiple criteria:")
        st.write("\u27A1Airline-wise Analysis of Flights")
        st.write('\u27A1Airline-wise Analysis Between Two Airports')
        st.write('\u27A1Busiest International Airports in India')
        st.write('\u27A1Hourly Flight Departures from Airports')
        st.write('\u27A1Average Fare Analysis Between Two Airports')
        st.write("\u27A1Check Airport Ownership Details")  
        st.write("Each visualization is generated from the SQL-stored data and rendered using interactive charts (Plotly).")
        st.subheader("Name and Ownership of Airport")
        st.write("""\u27A1Displays a searchable DataFrame listing all Indian international airports along with their respective
                 managing authorities (e.g., AAI, Adani Group, GMR).""")
        st.write("\u27A1Users can also search ownership details for a specific airport.")
        
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write('''This tool serves as an educational project to demonstrate how real-world flight data can be transformed into meaningful insights using modern data analytics tools.''')
               
flight= Main()
flight.main_page()