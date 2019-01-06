# Log-Analysis
A web application that provides a list of items within a variety of categories and integrates third party user registration and authentication. Authenticated users have the ability to create, edit, and delete their own items.

# Features available
1. Users can sign-in or sign up
2. There are two types of users - admin and normal users
3. Admin users can see all items, whereas normal users can see items pertaining to them
4. Users can sign in using google oauth2, using their own google email
5. Images can be uploaded for respective catalogs
6. Each page is authenticated using csrf token

# Technology Used
1. Docker
2. SQLLite
3. Python 3
4. Flask
5. HTML and CSS

# Pre-requisites
1. Have [docker](https://www.docker.com/get-started) installed in your system
2. Make sure the http://localhost:8000 is available, since the app and third party authentication is enabled only for port 8000.
3. Installation of docker provides you with `docker-compose`
4. Please have `docker-compose` version 1.22 or greater, to check
```
$ docker-compose version
docker-compose version 1.22.0, build f46880f
```
# How to run?
1. Clone the repository first
 2. ```
    $ git clone git@github.com:debatanu-thakur/item-catalog.git && cd item-catalog
    ```
3.  ``` 
    $ docker-compose up
    ```
4. The app should be now available in http://localhost:8000

# Some login details
1. Admin
   *  username - admin@example.com
   * password - admin123
2. Normal user1
   *  username - user1@example.com
   * password - norm123
3. Normal user1
   *  username - user2@example.com
   * password - user123

License
----

MIT