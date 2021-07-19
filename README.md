
The goal of this project was to create a bot for my Discord server. 

The programming language used in the development was **Python** along with its libraries,
the **Heroku** cloud application platform was used to remotely host the project, 
the **SQLite** relational database management system was used to keep track of various user data.

The following is meant to serve as an instruction for using the server:

Following the invite, the user is free to browse the #general and the #roles channel. The latter can be used to select which channel the user is willing to follow. To select a channel, the command
```
$follow <channel-name>
```
is used (where **$** can be replaced with any allowed command prefix).

Then the list of implemented commands (out of simplicity reasons **$** is used as a general symbol for command prefixes) is:
```
$pomoc, $helpplz, $manual, $napoveda - print the manual

$time <X>, $cas <X> - prints the time in city X, returns an error if the city hasn't been found or if the input is invalid

$weather <X>, $pocasi <X> - prints the weather report of the city X, returns an error if the city hasn't been found or if the input is invalid

$covid, $korona <X> - prints the covid report of the country X, returns an error if the country hasn't been found or if the input is invalid

$translate <X> <Y> <z>, $prelozit <X> <Y> <z> - prints the translation the word <z> from language X to language Y

$calculate <X> <Y> <z>, $spocitat <X> <Y> <z> - performs the <z> mathematical operation on numbers X and Y, returns errors if input is invalid

$compile <LANG> <CODE> - compilates the code written in the given language and prints the result of compilation. (Uses third party bot)
```

The application keeps track of information about each user entering the server, storing them in a database. The data stored are:
```
User Primary Key
User Discord ID
User Name
Channels the User Follows 
Date of First Session
Permissions
```

