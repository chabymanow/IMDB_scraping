Actor finder on IMDB
---

This program searches for the given actor or actress on **IMDB** and finds all his films registered there. The found movies are saved in the database specified in the code.

The name of the actor or actress can be specified as an  (`sys.argv`) when starting the program. If nothing is entered, the program asks for the name and starts the search.

The database strucure is
* **ID**: the ID of the data
* **actorName**: the name of the actor or actress
* **actorLink**: link to the actor/actress IMDB page
* **movieName**: the name of the movie
* **movieLink**: link to the page of the movie

The program is prepared to save the data into a **JSON** file but it is not write the file. Feel free to implement this function!