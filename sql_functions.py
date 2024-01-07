from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import ssl, time, datetime
sleep = time.sleep
import elements_address, settings
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import mysql.connector
from mysql.connector import errorcode
import random, os
from colorama import Fore, Style
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functions import *


def save_urls(All_urls, location): 
    for url in All_urls:
        id = url.split('/')[-1]
        data = {'id': id, 'url': url, 'location': location}
        insert_urls_into_table(data, settings.collected_urls_db)
        
        
def get_queue():
    scrape = connect_and_fetch_queue()

    if scrape is not None and len(scrape) != 0:
        scrape_entry = random.choice(scrape)
        return scrape_entry
    else:
        green('[*] NO SCRAPE IN SCRAPE QUEUE ....')
        os._exit(0)


def connect_and_fetch_queue():
    try:
        connection = mysql.connector.connect(
            user=settings.mysql_user,
            password=settings.mysql_passwd,
            host=settings.mysql_host,
            database=settings.mysql_db
        )

        if connection.is_connected():
            try:
                cursor = connection.cursor()
                query = f"SELECT done, location, date_start, date_end, scrape_profile FROM {settings.mysql_table}"
                cursor.execute(query)
                rows = cursor.fetchall()
                return tuple(rows)
            except mysql.connector.Error as err:
                log(err, 'sql connection')
                print(f"Error: {err}")
            finally:
                connection.close()
        else:
            print("Failed to connect to the database")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            log(err, 'sql connection')
            print(f"Error: {err}")
        
def insert_urls_into_table(data, table_name):
    try:
        connection = mysql.connector.connect(
            user=settings.mysql_user,
            password=settings.mysql_passwd,
            host=settings.mysql_host,
            database=settings.mysql_db
        )

        if connection.is_connected():
            try:
                cursor = connection.cursor()

                # Check if the URL already exists in the table
                query_check = f"SELECT COUNT(*) FROM {table_name} WHERE url = %(url)s"
                cursor.execute(query_check, {'url': data['url']})
                result = cursor.fetchone()

                if result[0] == 0:
                    # URL doesn't exist, insert the data
                    query_insert = f"INSERT INTO {table_name} (id, url, location) VALUES (%(id)s, %(url)s, %(location)s)"
                    cursor.execute(query_insert, data)
                    connection.commit()

            except mysql.connector.Error as err:
                log(err, 'sql insert')
                print(f"Error: {err}")
            finally:
                connection.close()
        else:
            print("Failed to connect to the database")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            log(err, 'sql insert')
            print(f"Error: {err}")



def insert_data(data, table_name):
    try:
        connection = mysql.connector.connect(
            user=settings.mysql_user,
            password=settings.mysql_passwd,
            host=settings.mysql_host,
            database=settings.mysql_db
        )

        cursor = connection.cursor()

        # Construct the SQL query for insertion using dynamic keys
        insert_query = f"""
        INSERT INTO {table_name} ({', '.join(data.keys())})
        VALUES ({', '.join(['%(' + key + ')s' for key in data.keys()])})
        ON DUPLICATE KEY UPDATE
        {', '.join([key + ' = %(' + key + ')s' for key in data.keys()])}
        """

        cursor.execute(insert_query, data)

        connection.commit()


    except Exception as e:
        print(f"Error insert_data: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

            
            
def insert_amenities_data(data, table_name):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            user=settings.mysql_user,
            password=settings.mysql_passwd,
            host=settings.mysql_host,
            database=settings.mysql_db
        )

        # Create a MySQL cursor to execute queries
        cursor = connection.cursor()

        # Check if the combination of id_of_location and description already exists
        select_query = f"SELECT * FROM {table_name} WHERE id_of_location = %s AND description = %s"
        select_values = (data['id_of_location'], data['description'])
        cursor.execute(select_query, select_values)

        # Fetch the result
        result = cursor.fetchone()

        if result is None:
            # Combination doesn't exist, so proceed with the insertion
            insert_query = f"INSERT INTO {table_name} (id_of_location, description) VALUES (%s, %s)"

            # Extract values from the 'data' dictionary
            insert_values = (data['id_of_location'], data['description'])

            # Execute the SQL query with the provided data
            cursor.execute(insert_query, insert_values)

            # Commit the changes to the database
            connection.commit()

    except Exception as e:
        print(f"insert_amenities_data Error: {e}")

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()