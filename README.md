# Collaborative list maker

This project is a collaborative list making tool.  
Users can create lists which they can share with others using the list code.

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

## API End points
This project contains API end points for the 4 CRUD operations as listed below.

### Create

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
| Parameter |Description              |
| :----------| :-----------------------:|
|     listid | Unique ID for list to add entry to|
| text|  The text to be added to the list|


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
| :----------| :-----------------------:|
|     passphrase  | Passphrase entered by the user|
|listid| unique id of list| 
|code| Unique 4 digit list code|


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

### Read

#### `/getList`
Used to retrieve a list

`Method: GET` 
##### URL params
| Parameter  |Description              |
| :----------| :-----------------------:|
| code        |Unique 4 digit list code |
|jwt |JWT token|

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
### Update

### Delete


## JWT implementation
To implement JWT into this project, the server issues a token when a list is created or a user enters the correct code and passphrase for a list.
The server checks to see if a JWT exists when a user accesses a list, if their is an existing JWT for the list being accessed, the user will not be prompted for the passphrase and can access the list immediately after entering the code.



# Template
#### `/`
description

`Method: ` 
##### URL params
| Parameter  |Description              |
| :----------:| :-----------------------:|
|       |      | 


##### Returns
```
success: 
{

}

failure:
{

}
```