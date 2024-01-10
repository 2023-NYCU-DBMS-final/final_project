import os
import sqlite3
import pandas as pd

# Connect to SQLite database (creates if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

#def updategraph(city, site_name):


def get_test_target():
    query='''SELECT DISTINCT TestTarget
        FROM my_table
        '''
    cursor.execute(query)
    site_names=cursor.fetchall()
    sites_list=[site[0] for site in site_names]
    #print(sites_list)
    conn.commit()
    return sites_list


def get_history_data(city, site_name):
    converted_site_name="'"+site_name+"'"
    targets=get_test_target()
    
    query='''CREATE TABLE a(SiteName varchar(20), Date varchar(20), TestTarget varchar(20), Test0 int)'''
    cursor.execute(query)
    conn.commit()
    
    query='''INSERT INTO a SELECT SiteName, Date, TestTarget, Test0 FROM my_table WHERE substr(SiteName, 1, ''' +str(len(site_name))+''')='''+converted_site_name
    cursor.execute(query)
    conn.commit()

    history_data=[]
    for target in targets:
        converted_target="'"+target+"'"
        query='''SELECT * FROM a WHERE substr(TestTarget, 1, ''' + str(len(target)) + ''')=''' + converted_target
        cursor.execute(query)
        data=cursor.fetchall()
        history_data.append({target: data})
        conn.commit()

    query='''DROP TABLE a'''
    cursor.execute(query)
    conn.commit()
    print(history_data)
    return history_data

def getcity():
    cursor.execute('''
        SELECT DISTINCT county 
        FROM current
    ''')
    counties=cursor.fetchall()
    counties_list = [county[0] for county in counties]
    conn.commit()
    return counties_list

#'屏東縣','新北市','臺中市','臺南市','高雄市','彰化縣',
#'雲林縣','臺東縣','澎湖縣','金門縣','連江縣','南投縣',
#'桃園市','宜蘭縣','臺北市','花蓮縣','嘉義市','苗栗縣','新竹市','新竹縣','基隆市'

def get_site_in_city(city):
    converted_string = "'" + city + "'"
    query='''SELECT DISTINCT sitename
        FROM current
        WHERE substr(county, 1, 2)='''+converted_string
    cursor.execute(query)
    site_names=cursor.fetchall()
    sites_list=[site[0] for site in site_names]
    conn.commit()
    return sites_list

def get_sites():
    query='''SELECT DISTINCT sitename
        FROM my_table
        '''
    cursor.execute(query)
    site_names=cursor.fetchall()
    sites_list=[site[0] for site in site_names]
    print(sites_list)
    conn.commit()
    return sites_list

get_history_data('新北市', '板橋')