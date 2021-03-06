# Collaborative list maker

https://github.com/KristianTan/listMaker

This project is a collaborative list making tool.  
Users can create lists which they can share with others using the list code.

## Running the application
The application is installed on the CS2S server.
The server application can be run by activating the virtual environment and running the `app.py` file found at the following location in my user area:

`kristian.tan/htdocs/listMaker/app.py`

commands to run the server application:

`source venv/bin/activate`

`python app.py`

The server application is provided by a database named kristiantan_RESTService hosted on the cs2s server.

Once the server application is running, the client can be found at the following link:
http://ysjcs.net/~kristian.tan/


## Usage
##### Creating a list
* To create a new list, select the `Create List` button from the home page.
* On the create list page enter a title and passphrase for your list, other users will need to know the passphrase to access your list.
* After filling in the information for your list, press the create list button
* After creating your list you will be redirected to the list viewing page
* The list code is displayed at the top of this screen, which can be used to access the list from the hope page

##### Accessing a list
* To access an existing list enter a list code into the text box on the home screen
* Press the `Join List` button to go to the specified list
* Enter the passphrase for the list in the text box and press `Enter`
* Once you have entered the passphrase you will not be asked for it again, unless you access another list
* List entries can be deleted by clicking on them
* List titles can be updated by clicking on them

##### Accounts
Logged in users can save lists to access in the future.  If they save the list, they can view it from the `Saved lists` page, and access and edit it without needing to enter the passphrase.

## Test data
For demonstration purposes a user account and a list have been created, the details are:

Username:  user

Password:  password

List code: 1234

List passphrase: passphrase

## API End points
This project contains API end points for the 4 CRUD operations as listed below.

### Create (POST)

#### `/createList`
Used to create a new list

`Method: POST`
##### URL params
| Parameter  |Description              |
| :----------| :-----------------------:|
|   title    | Title for new list |
|passphrase|Passphrase for new list|

##### Returns
```
success:
{
    code: {list code},
    jwt: {JWT token}
}

```

#### `/newEntry`
Used to create a new entry in a list

`Method: POST`
##### URL params
| Parameter  |Description              |
| :----------| :-----------------------:|
|     listid | Unique ID for list to add entry to|
| text       |  The text to be added to the list|


##### Returns
```
Returns empty json
{
}
```


#### `/checkPassphrase`
Used to check the passphrase entered by a user to authorise them to use a list

`Method: POST`
##### URL params
| Parameter |Description              |
| :---------| :-----------------------:|
|passphrase | Passphrase entered by the user|
|listid     | unique id of list|
|code       | Unique 4 digit list code|


##### Returns
```
success:
{
    message: "Correct passphrase",
    token: JWT token
}

failure:
{
    message: "Incorrect passphrase"
}

```
#### `/register`
Used to create a new account

`Method: POST`
##### URL params
| Parameter         |Description              |
| :----------       | :-----------------------:|
|   username        | account username |
|   password        | account password |
|   confirmPassword | account password confirmation|

##### Returns
```
success:
{
    jwt: {JWT token}
}

```

#### `/login`
Used to log in a user

`Method: POST`
##### URL params
| Parameter     |Description              |
| :----------   | :-----------------------:|
|   username    | account username |
|   password    | account password |

##### Returns
```
success:
{
    jwt: {JWT token}
}

```


### Read (GET)

#### `/getList`
Used to retrieve a list

`Method: GET`
##### URL params
| Parameter  |Description              |
| :----------| :-----------------------:|
| code       |Unique 4 digit list code |
| jwt        |JWT token|

##### Returns
```
success:
{
    message: "List found",
    id: {list ID},
    code: {list code},
    entries: {[List of items on list]},
    auth: True
}

failure:
{
    message: "No list found for that code",
    code: {list code}
}
```

#### `/getSavedLists`
Used to retrieve a list of the users saved lists

`Method: GET`
##### URL params
| Parameter  |Description              |
| :----------| :-----------------------:|
| jwt        |JWT token|

##### Returns
```
success:
{
    saveed_lists: {[List of a users saved on lists]}
}

```



### Update (PUT)
#### `/renameList`
Used to update a lists title

`Method: PUT`
##### URL params
| Parameter  |Description              |
| :---------:| :-----------------------:|
| id         |      list ID|
| newTitle   | New title of list|


##### Returns
```
nothing
```

### Delete (DELETE)
#### `/deleteEntry`
Used to delete an item from a list

`Method: DELETE`
##### URL params
| Parameter   |Description              |
| :----------:| :-----------------------:|
|   id        |  ID of the entry to delete    |


##### Returns
```
nothing
```



## JWT implementation
To implement JWT into this project, the server issues a token when a user registers a new account or logs in to an existing account.  Logged in users can edit and access their lists without the list passphrase, and save lists to their account.
