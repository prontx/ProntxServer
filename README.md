The goal of this project was to create a bot for my Discord server. 

The programming language used in the development was **Python** along with its libraries,
the **Heroku** cloud application platform was used to remotely host the project, 
the **SQLite** relational database management system was used to keep track of various user data.

The following is meant to serve as an instruction for using the server:

Following the invite, the user is free to browse the #general and the #roles channel. The latter can be used to select which channel the user is willing to follow. All it takes to obtain a role for a certain channel is a reaction in the #roles.

The list of implemented commands (out of simplicity reasons **$** is used as a general symbol for command prefixes) is:
```
$manual - print the manual

$weather city - prints the weather report of the city, returns an error if the city hasn't been found or if the input is invalid

$translate firstlang secondlang expression - prints the translation of the expression from language firstlang to language secondlang

$calculate num1 num2 op - performs the op mathematical operation on numbers num1 and num2, returns errors if input is invalid

;compile LANG CODE - compilates the code written in the given language and prints the result of compilation (Uses third party bot)

$vote question choice1 choice2 - starts a vote with two options given as arguments, over after 10 seconds
```

The application keeps track of information about each user entering the server, storing them in a database. The data stored are:
```
User Discord ID
User Name
Channels the User Follows 
Date of First Session
```
Those are printed by the 
```
$me
```
command.
