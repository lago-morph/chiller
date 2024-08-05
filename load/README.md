The idea behind this section of the application is to provide simulated
user load for the Watch and Chill application.  Since the application is
very simple, the load testing will also be simple.

A secondary objective is to reuse some of the work being done for the browser
test with Selenium, and turn the browser testing into an instance of load
testing.  This is probably not what you would do in a real application, 
but may be a convenient simplification for this demo application.

The end use of this will be to have one or more docker containers generating
usage on the application.

As a rough guide, maybe break it down by transaction:
- Normal processing
  1. Create user        1%
  2. Login successfully 9%
  3. List movies        38%
  4. Add movies         38%
  5. Logout             10%
- Exception processing
  6. Create user - duplicate name 1%
  7. Login - user does not exist 1%
  8. List movies, not logged in 1%
  9. List movies for user that does not exist, logged in 1%
This is not an exhaustive list.
I think I want about 95% normal processing and 5% exception processing.
Every login or create user will result in one list movies.

Probably the best way to do this is to have one script that has this 
distribution of events, and have it run over and over again with some 
random delays so that multiple runners will not be in phase.

So each run do:
wait 0-10 seconds
generate username
List movies for userid 1, not logged in (the first time this will take a different path than after the first user is created)
Login with generated username - user does not exist
Create user       
Add 4 movies (will list movies 5 times)
List movies for user that does not exist (99999), logged in
Logout
(do 9 times)
  Login
  Add 4 movies
  Logout
Create user with generated username (duplicate username)
loop
