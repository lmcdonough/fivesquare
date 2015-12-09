# FiveSquare
###Fivesquare Django REST API

This is a service similar to Foursquare, that is centered around users, businesses, and reviews. It allows users to write reviews of businesses, and other users to use those reviews to help them decide which businesses to patronize. It is implemented using Django and Django REST. I’ve currently deployed it to Heroku, using MongoDB as the database. I’ve also written some basic tests for the application.

The API allows a user to post a review for a business.  The reviews consist of the following: 1-5 star rating, review text, and free-form "tags".  The API also includes an endpoint displaying the reviews in chronological order, its overall rating, and a summary of its tags from reviews.  The API also includes an endpoint that returns all businesses within a user-specified distance of a given point (e.g within 1000 meters of 40.739739, -73.990557).  

####Below I will be using CURL in my examples.

**To see a JSON output of the schema**
- curl http://domain.com/

**To output a list of all establishments**
- curl http://domain.com/establishments/

**To output details of a particular establishment (where pk is the id of the establishment)**
- curl http://domain.com/establishment/pk/

**To create a new establishment (below is an example creating the Empire State Building)**
- curl -X POST -d '{"name": "Empire State Building", "city": "New York City",	"state": "New York", "country": "USA", "location": {"longitude": 73.9857, "latitude": 40.7484}}' http://domain.com/establishments/ -u user:pass --header "Content-Type:application/json"

**To update an establishment (below is an example updating the Empire State Building changing it's name)**
- curl -X PUT -d '{"name": "Empire Strikes Back State Building", "city": "New York City",	"state": "New York", "country": "USA", "location": {"longitude": 73.9857, "latitude": 40.7484}}' http://domain.com/establishment/56689ed3077e240003d7ab34/ -u user:pass --header "Content-Type:application/json"

**To delete an establishment (below is an example deleting the Empire State Building I created)**
- curl -X DELETE http://domain.com/establishment/56689ed3077e240003d7ab34/ -u user:pass

**To get a list of all establishments within a certain distance (meters) of a latitude and longitude**
- curl http://domain.com/establishments/?latitude=40.7484&longitude=73.9857&distance=1000

**To output a list of all reviews**
- curl http://domain.com/reviews/

**To output details of a particular review (where pk is the id of the review)**
 - curl http://domain.com/review/pk/

**To create a review for an establishment (below I create a review for the Empire State Building I created above)**
 - curl -X POST -d  '{"establishment": "56689ed3077e240003d7ab34", "title": "My day at the Empire State Building", "text": "This place has an amazing view!", "stars": 5, "tags": ["Romantic", "First Date"]}' http://domain.com/reviews/ -u user:password --header "Content-Type:application/json"

**To update a review (below is an example updating the Empire State Building changing it's name)**
 - curl -X PUT -d  '{"establishment": "56689ed3077e240003d7ab34", "title": "My day at the Empire State Building", "text": "I changed my mind, this place is just ok.", "stars": 3, "tags": ["Romantic", "First Date"]}' http://domain.com/review/5668a0c7077e240003d7ab35/ -u user:password --header "Content-Type:application/json"

**To delete a review (below is an example deleting the review for the Empire State Building I created)**
- curl -X DELETE http://domain.com/review/5668a0c7077e240003d7ab35/ -u user:pass

**To list all reviews for an establishment (default ordered by date in descending order)**
- curl http://domain.com/reviews/?establishment=56689ed3077e240003d7ab34

**To output a list of all categories (only staff can view/create catgories)**
- curl http://domain.com/categories/

**To output details of a particular category (where pk is the id of the category)**
- curl http://domain.com/category/pk/

**To create a category**
 - curl -X POST -d  '{"name": "Landmark"}' http://domain.com/categories/ -u user:password --header "Content-Type:application/json"

**To output a list of all users**
- curl http://domain.com/users/

**To output details of a particular user (where pk is the id of the user)**
- curl http://domain.com/user/pk/



