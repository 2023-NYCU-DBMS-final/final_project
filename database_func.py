import os
import sqlite3

def get_test_target():
    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect('airData.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    query='''SELECT DISTINCT TestTarget
        FROM cumulateData
        '''
    cursor.execute(query)
    site_names=cursor.fetchall()
    sites_list=[site[0] for site in site_names]
    #print(sites_list)
    conn.commit()
    return sites_list

def get_history_data(city, site_name):
    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect('airData.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    converted_site_name="'"+site_name+"'"
    targets=get_test_target()
    
    query='''CREATE TABLE a(SiteName varchar(20), Year varchar(20), TestTarget varchar(20), Test0 int)'''
    cursor.execute(query)
    conn.commit()
    
    query='''INSERT INTO a SELECT SiteName, YEAR(STR_TO_DATE(Date, '%Y/%m/%d %H:%i:s')) AS Year, TestTarget, Test0 FROM cumulateData WHERE substr(SiteName, 1, ''' +str(len(site_name))+''')='''+converted_site_name
    cursor.execute(query)
    conn.commit()

    history_data=[]
    for target in targets:
        converted_target="'"+target+"'"
        query='''SELECT SiteName, TestTaret, Year, AVG(Test0),  FROM a WHERE substr(TestTarget, 1, ''' + str(len(target)) + ''')=''' + converted_target +'''GROUP BY TestTarget, Year ORDER BY YEAR'''
        cursor.execute(query)
        data=cursor.fetchall()
        history_data.append({target: data})
        conn.commit()

    query='''DROP TABLE a'''
    cursor.execute(query)
    conn.commit()
    print(history_data)
    return history_data

def get_current_data(city, site_name):
    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect('airData.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    converted_site_name="'"+site_name+"'"
    converted_city="'"+city+"'"
    history_data=[]
    query='''CREATE TABLE a(
            SiteName TEXT,
            County	TEXT,
            AQI	samllint,
            status TEXT,
            pm2_5 smallint,
            wind_speed decimal(4,1),
            wind_direc smallint,
            publishtime timestamp,
            pm2_5_avg decimal(4,1)
        )'''
    cursor.execute(query)
    conn.commit()
    
    query='''INSERT INTO a SELECT SiteName, County, AQI, status, pm2_5, wind_speed, wind_direc, publishtime, pm2_5_avg FROM currentData WHERE substr(SiteName, 1, ''' +str(len(site_name))+''')='''+converted_site_name+''' AND substr(County, 1, ''' + str(len(city))+''')='''+converted_city
    cursor.execute(query)
    conn.commit()

    current_data=[]

    query='''SELECT * FROM a'''
    cursor.execute(query)
    rows=cursor.fetchall()
    for row in rows:
        i=0
        for data in row:
            if(i==0):
                current_data.append({"SiteName" : data})
            elif(i==1):
                current_data.append({"County" :data})
            elif(i==2):
                current_data.append({"AQI" :data})
            elif(i==3):
                current_data.append({"status" :data})
            elif(i==4):
                current_data.append({"pm2_5" :data})
            elif(i==5):
                current_data.append({"wind_speed" :data})
            elif(i==6):
                current_data.append({"wind_direc" :data})
            elif(i==7):
                current_data.append({"publishtime" :data})
            elif(i==8):
                current_data.append({"pm2_5_avg" :data})
            i=i+1
    conn.commit()

    query='''DROP TABLE a'''
    cursor.execute(query)
    conn.commit()
    return current_data

def getcity():
    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect('airData.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT county 
        FROM currentData
    ''')
    counties=cursor.fetchall()
    counties_list = [county[0] for county in counties]
    conn.commit()
    return counties_list

#'屏東縣','新北市','臺中市','臺南市','高雄市','彰化縣',
#'雲林縣','臺東縣','澎湖縣','金門縣','連江縣','南投縣',
#'桃園市','宜蘭縣','臺北市','花蓮縣','嘉義市','苗栗縣','新竹市','新竹縣','基隆市'

def get_site_in_city(city):
    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect('airData.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    query='''SELECT DISTINCT sitename
        FROM currentData
        WHERE substr(county, 1, {})="{}"'''.format(len(city),city)
    print(query)
    cursor.execute(query)
    site_names=cursor.fetchall()
    print(site_names)
    sites_list=[site[0] for site in site_names]
    print(sites_list)
    conn.commit()
    return sites_list

def get_sites():
    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect('airData.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    query='''SELECT DISTINCT sitename
        FROM cumulateData
        '''
    cursor.execute(query)
    site_names=cursor.fetchall()
    sites_list=[site[0] for site in site_names]
    print(sites_list)
    conn.commit()
    return sites_list
