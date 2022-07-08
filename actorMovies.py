import requests
from bs4 import BeautifulSoup as soup
import json # The program does not use it yet
import sys
from getpass import getpass
from mysql.connector import connect, Error
import mysql.connector

#*************************************
#                                    #
# The database info:                 #
# Database name: actors_movies       #
# Table name: actordata              #
#                                    #
# Feel free the modify these names   #
#                                    #
#*************************************

# Check the given movie title is allready in the database or not
def checkMovie(movieTitle):
    try:
        with connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "actors_movies"
        ) as connection:
            cursor = connection.cursor()
            sql_select_query = """select * from actordata where movieName = %s"""
            cursor.execute(sql_select_query, (movieTitle,))
            record = cursor.fetchall()
            if record:
                return True
            else:
                return False
    except Error as e:
        print(e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# Write the movie data into the database
def writeDatabase(data):
    insert_movies_query = """
    INSERT INTO actordata (actorName, actorLink, movieName, movieLink)
    VALUES(%s, %s, %s, %s)"""

    try:
        with connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "actors_movies"
        ) as connection:
            print("MySQL connection is opened. Writing data into the database...")
            with connection.cursor() as cursor:
                cursor.executemany(insert_movies_query, data)
                connection.commit()
    except Error as e:
        print(e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def main():
    # Check the user given any name. If not, ask the user  
    if len(sys.argv) > 1:
        actorName = sys.argv[1]
    else:
        actorName = input("Name: ")
    baseURL = 'https://www.imdb.com/find?q='
    searchReq = requests.get(baseURL + actorName)
    print(f"[-] Status: {searchReq.status_code}")

    # Find the link to the actor
    searchSoup = soup(searchReq.text, 'html.parser')
    parent = searchSoup.find('td', class_='result_text')
    child = parent.find('a')['href']

    # Set the full link to the actor`s page
    actorLink = 'https://www.imdb.com' + child
    print(f'[-] Actor link: {actorLink}')

    actorPage = requests.get(actorLink)
    actorSoup = soup(actorPage.text, 'html.parser')

    # Find the movie list on the page
    actorTable = actorSoup.find('div', class_='filmo-category-section')
    movies = actorTable.find_all('b')
    
    #Set the basic data
    actorData = {}
    actorData["name"] = actorName
    actorData["link"] = actorLink
    actorData["movies"] = []
    databaseData = []
    i = 0

    # Check each movie from the movie list
    for movie in movies:
        movieTitle = movie.find('a').text
        movieLink = movie.find('a')['href']
        fullMovieLink = 'https://www.imdb.com'+movieLink

        # Prepare the data to JSON format. The program does not use it, just prepare
        movieData = {'title': movieTitle, 'link': fullMovieLink}
        actorData["movies"].append(movieData)
        i += 1

        # Check the movie is allready in the database or not
        if checkMovie(movieTitle) == False:      
            databaseChunk = [actorName, actorLink, movieTitle, fullMovieLink]
            databaseData.append(databaseChunk)

    # Write out some info
    print(f'[-] {i} new movies found...')
    print("[-] Writing the database...")

    # Send the data to a function for write into the database
    writeDatabase(databaseData)
    
    return

if __name__ == '__main__':
    main()