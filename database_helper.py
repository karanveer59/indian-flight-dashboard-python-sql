import pymysql as sql
import os 
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

class DB:
    def __init__(self):
        # self.conn = None
        # self.mycursor = None
        try:
            self.conn = sql.connect(host= '127.0.0.1', user= os.environ['USER'], password= os.environ['PASSWORD'] , database= 'flight', cursorclass=pymysql.cursors.DictCursor)     
            
            print("Connection established")
        except Exception as e:
            print("Connection Failed! ", e)
        self.mycursor= self.conn.cursor()
    def name_of_cities(self):
        self.mycursor.execute("""
                              SELECT DISTINCT(Departure_Port) from flights
                                UNION
                                SELECT DISTINCT(Arrival_Port) from flights;
                              """)
        data = self.mycursor.fetchall()
        
        list_ = []
        for i in data:
            for item in i:
                list_.append(item)
        
        return list_
    
    def show_flights(self, source, destination):
        # self.mycursor.execute("""
        #         SELECT Airline,Airline_Code,Flight_Number,Cabin_Class,Departure_Time, Departure_Port,Arrival_Time,Arrival_Port,Duration_Time, `Stop` ,Fare, `Enjoy Free Meals`
        #         FROM flights
        #         WHERE Departure_Port = '{}' AND Arrival_Port = '{}'  
        #         """.format(source, destination))
        query = """
                SELECT Airline,Airline_Code,Flight_Number,Cabin_Class,Departure_Time, Departure_Port,Arrival_Time,Arrival_Port,Duration_Time, `Stop` ,Fare, `Enjoy Free Meals`
                FROM flights
                WHERE Departure_Port = '{}' AND Arrival_Port = '{}'
        """.format(source, destination)
        data = pd.read_sql(query, self.conn)
        for col in ['Departure_Time', 'Arrival_Time', 'Duration_Time']:
            if pd.api.types.is_timedelta64_dtype(data[col]):
                data[col] = data[col].apply(lambda x: str(x).split()[-1]) 
            elif pd.api.types.is_object_dtype(data[col]):
                try:
                    data[col] = pd.to_datetime(data[col]).dt.time
                except Exception:
                    pass
        # data = self.mycursor.fetchall()
        return data

    def flights_pie(self):
        airline = []
        count = []
        self.mycursor.execute("""
                                SELECT Airline, count(*) AS count 
                                FROM flights
                                GROUP BY Airline
                                """)
        
        data = self.mycursor.fetchall()
        
        for item in data:
            airline.append(item[0])
            count.append(item[1])
            
        return airline, count
    
    def flights_pies(self,source,destination):
        airline = []
        frequency = []
        self.mycursor.execute('''
                              SELECT airline,count(*) as count FROM flights
                              WHERE Departure_Port = '{}' AND Arrival_Port = '{}'
                              GROUP BY Airline
                              '''.format(source, destination))            
        data = self.mycursor.fetchall()
        
        for item in data:
            airline.append(item[0])
            frequency.append(item[1])
        
        return airline, frequency
    
    def bussiest_airport(self):
        airports = []
        frequency = []
        self.mycursor.execute("""
                            SELECT Departure_Port,COUNT(*) FROM (SELECT Departure_Port FROM flights
                            UNION ALL
                            SELECT Arrival_Port FROM flights) t
                            GROUP BY Departure_Port
                            ORDER BY COUNT(*) DESC
                            """)
        data = self.mycursor.fetchall()
        
        for item in data:
            airports.append(item[0])
            frequency.append(item[1])
            
        return airports, frequency
    
    def hourly_departure(self):
        hour = []
        frequency = []
        self.mycursor.execute("""
                                SELECT HOUR(Departure_Time) AS Per_Hour, count(*) FROM flights
                                GROUP BY Per_Hour
                                ORDER BY Per_Hour
                            """)
        data = self.mycursor.fetchall()
        
        for item in data:
            hour.append(item[0])
            frequency.append(item[1])
            
        return hour, frequency
    
    def hourly_departure_for_particular(self,source):
        hour = []
        frequency = []
        self.mycursor.execute("""
                            SELECT HOUR(Departure_Time) AS Per_Hour, count(*) FROM flights
                            WHERE Departure_Port = '{}'
                            GROUP BY Per_Hour
                            ORDER BY Per_Hour
                            """.format(source))
        data = self.mycursor.fetchall()
        
        for item in data:
            hour.append(item[0])
            frequency.append(item[1])
            
        return hour, frequency
    
    def average_fare(self, source, destination):
        query = """
            SELECT Airline, Cabin_Class, AVG(Fare) as Fare FROM flights
            WHERE Departure_Port = '{}' AND Arrival_Port = '{}'
            GROUP BY Airline, Cabin_Class
        """.format(source, destination)
        
        data = pd.read_sql(query, self.conn)
        return data
    
    def airport_owners(self):
        query = """
                WITH RANKED AS (SELECT Departure_Port ,Dep_Port_Owned_by,row_number()
                OVER (PARTITION BY Dep_Port_Owned_by) AS 'Total'
                FROM flights
                GROUP BY Departure_Port ,Dep_Port_Owned_by)
                SELECT Dep_Port_Owned_by as Managing_Authority ,max(Total) AS Total_Ports
                FROM RANKED 
                GROUP BY Dep_Port_Owned_by
        """
        
        data = pd.read_sql(query, self.conn)
        return data
    
    def airport_owners_particular(self,airport):
        query = """
                SELECT DISTINCT Dep_Port_Owned_by AS 'Managing_Authority'
                FROM flights
                WHERE Departure_Port = '{}'
        """.format(airport)
        data = pd.read_sql(query, self.conn)
        return data
    
    def about_airports(self):
        query = ("""
              SELECT DISTINCT Departure_Port AS 'Airport' ,Dep_Port_Name AS 'Airport Name',Dep_Port_Owned_by AS 'Managing_Authority' FROM flights
              ORDER BY Airport
              """)
        data = pd.read_sql(query, self.conn)
        return data
    
    def check_about(self,airport):
        query = """
                SELECT DISTINCT Departure_Port,Dep_Port_Name,Dep_Port_Owned_by FROM flights
                WHERE  Departure_Port= "{}"
                ORDER BY Departure_Port
        """.format(airport)
        data = pd.read_sql(query, self.conn)
        return data
        
