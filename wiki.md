# This is a documentation of web-api for this project.
## It consists of descriptions for ajax requests that server is listening to:

- Type - a type of request (GET, POST, DELETE, etc.).
- URL - a string like **/dir/dir/command/{argument}** with arguments being in curly braces.
- Arguments:
    - For GET-requests are written like **/getrequest/?argument={argument}**
    - For other request types are written simply like **/request/{argument}**
    - Arguments with ?-sign are optional - **/with-opt-arg/{optional?}**
- Request body (optional) - a JSON-formatted string:
```json
{
    "key" : "value"
}
```
- Response body (optional) - a JSON-formatted string:
```json
{
    "result" : "OK"
}
```

---


# Requests

## Login

| GET   	|       `/login/{password}`    	|
|-------	|:---------------------------:	|
| password 	| Admin identification word. 	|

Response body example:
```json
{
    "result": {
        "token": "sha1231241glibberish12332re2"
    }
}
```

## Users

### Get Users
Returns a list of users.

| GET   	|       `/{token}/users`      	|
|-------	|:---------------------------:	|
| token 	| Admin identification token. 	|

Response body example:
```json
{
    "result" : [
        {
            "id": 123,
            "name": "User Userovich"
        },
        {
            "id": 124,
            "name": "Other Otherovich"
        }
    ]
}
```


### Remove User

| DELETE 	|     `/{token}/users/{id}`    	|
|--------	|:----------------------------:	|
| token  	| Admin identification token.  	|
| id     	| An id of the user to remove. 	|

Response body example:
```json
{
    "result" : "success"
}
```
---
## Achievements

### Get Achievements
Returns a list of achievements (optionally for particular user).

| GET       	|  `/{token}/achievements/{id?}` 	|
|--------------	|:------------------------------:	|
| token     	| Admin identification token.    	|
| id (optional)	| Represents id_user in database 	|

Response body example:
```json
{
    "result" : [
        {
            "id": 123,
            "name": "Achievement name",
            "description": "Super-duper achievement description!"
        },
        {
            "id": 124,
            "name": "Other achievement name",
            "description": "Super-duper achievement description!"
        }
    ]
}
```

### Add Achievement
Returns an achievement id.

| POST  	|   `/{token}/achievement/`   	|
|-------	|:---------------------------:	|
| token 	| Admin identification token. 	|

Request body example:
```json
{
    "name": "New Achievement name",
    "description": "Super-duper achievement description!"
}
```

Response body example:
```json
{
    "result" : {
        "id": 125
    }
}
```

### Remove Achievement
Returns an achievement id.

| DELETE 	|        `/{token}/achievements/{id}`        	|
|--------	|:------------------------------------------:	|
| token  	| Admin identification token.                	|
| id     	| Id of achievement that needs to be removed 	|

Response body example:
```json
{
    "result" : "success"
}
```

### Add Achievement to user
Assigns an achievement to the user.

| POST             	|                `/{token}/achievements/{userId}`         	|
|------------------	|:---------------------------------------------------------:	|
| token            	| Admin identification token.                               	|
| userId            	| An id of the user.                                        	|
| achievementId    	| An id of achievement to assign                            	|

Request body example:
```json
{
    "achievementId": 125
}
```

Response body example:
```json
{
    "result" : "success"
}
```
---

## Schedule

### Get Schedule
Returns a schedule (global or optionally for particular user).
Returns today schedule if a date argument is not set.

| GET            	|     `/{token}/schedule/{userId}/date={date?}` 	|
|----------------	|:------------------------------------------------:	|
| token          	| Admin identification token.                      	|
| id               	| An id of the user.                               	|
| date (optional)	| A unix-format date string.                       	|

Response body example:
```json
{
    "result" : [
        {
            "id": 123,
            "start": 1414364400,
            "end": 1414364444,
            "name": "Event name",
            "description": "Super-duper event description!"
        },
        {
            "id": 124,
            "start": 1414364400,
            "end": 1414364444,
            "name": "Other event name",
            "description": "Super-duper event description!"
        }
    ]
}
```
---

## Groups

### Get Groups
Returns a list of groups (optionally for particular user).

| GET               	| `/{token}/groups/{userId?}` 	|
|-------------------	|:---------------------------:	|
| token             	| Admin identification token. 	|
| userId (optional) 	| An id of the user.          	|

Response body example:
```json
{
    "result" : [
        {
            "id": 1,
            "name": "Students"
        },
        {
            "id": 2,
            "name": "Karamba Team"
        }
    ]
}
```

### Add Group
Adds a group to the list of groups.

| POST  	|      `/{token}/groups/`     	|
|-------	|:---------------------------:	|
| token 	| Admin identification token. 	|

Request body example:
```json
{
    "name": "New Group name"
}
```

Response body example:
```json
{
    "result" : {
        "id": 125
    }
}
```

### Remove Group
Remove a group from the list of groups.

| DELETE 	|     `/{token}/groups/{id}`    	|
|--------	|:-----------------------------:	|
| token  	| Admin identification token.   	|
| id     	| An id of the group to remove. 	|

Response body example:
```json
{
    "result" : "success"
}
```

### Add users to the group
Adds users to the specific group.

| POST  	|    `/{token}/groups/{id}`   	|
|-------	|:---------------------------:	|
| token 	| Admin identification token. 	|
| id    	| An id of the group.         	|

Request body example:
```json
{
    "users": [ 250, 256, 953, 12, 42 ]
}
```

Response body example:
```json
{
    "result" : "success"
}
```
---
## Teams

### Add Team
Adds a team to the list of teams.

| POST    	|  `/{token}/teams/{groupId}` 	|
|---------	|:---------------------------:	|
| token   	| Admin identification token. 	|
| groupId 	| An id of the group.         	|

Request body example:
```json
{
    "codeword": "ufw9jewww9c8jwe"
}
```

Response body example:
```json
{
    "result" : "success"
}
```

### Remove Team
Remove a team from the list of teams.

| DELETE 	|    `/{token}/teams/{id}`    	|
|--------	|:---------------------------:	|
| token  	| Admin identification token. 	|
| id     	| An id of the team.          	|

Response body example:
```json
{
    "result" : "success"
}
```

### Get Teams
Returns a list of teams (optionally for particular user).

| GET               	|  `/{token}/teams/{userId?}` 	|
|-------------------	|:---------------------------:	|
| token             	| Admin identification token. 	|
| userId (optional) 	| An id of the user.          	|

Response body example:
```json
{
    "result" : [
        {
            "id": 2,
            "name": "Karamba Team"
        }
    ]
}
```
---
## Questions

### Get Questions
Returns a list of questions (optionally for particular team).

| GET               	| `/{token}/questions/{teamId?}` 	|
|-------------------	|:------------------------------:	|
| token             	| Admin identification token.    	|
| teamId (optional) 	| An id of the team.             	|

Response body example:
```json
{
    "result" : [
        {
            "id": 2,
            "num": 0,
            "description": "What is a bird?",
            "answer": "The word"
        }
    ]
}
```

### Add Question
Adds a question to the list (and bind it to the team).

| GET               	| `/{token}/questions/{teamId}` 	|
|-------------------	|:------------------------------:	|
| token             	| Admin identification token.    	|
| teamId             	| An id of the team (group).      	|

Request body example:
```json
{
    "description": "What is a bird?",
    "answer": "The word"
}
```

Response body example:
```json
{
    "result": {
        "id": 2
    }
}
```

### Remove Question
Remove a question from the list.

| DELETE 	|  `/{token}/questions/{id}`  	|
|--------	|:---------------------------:	|
| token  	| Admin identification token. 	|
| id     	| An id of the question.      	|

Response body example:
```json
{
    "result": "success"
}
```
---

## Events

### Get Events
Returns the list of events (optionally for group)

| GET           |    `/{token}/events/{id?}`    |
|-------------- |:----------------------------: |
| token         | Admin identification token.   |
| id (optional) | An id of the group.           |

Response body example:
```json
{
    "result": "success"
}
```

### Add Event
Adds and event to a certain group.
Responds with an event id.

| POST  |    `/{token}/events/{id}`   |
|-------|:---------------------------:|
| token | Admin identification token. |
| id    | An id of the group.         |

Request body example:
```json
{
    "start": 1414364400,
    "end": 1414364444,
    "name": "Event name",
    "description": "Super-duper event description!"
}
```

Response body example:
```json
{
    "result": {
        "id": 2
    }
}
```

### Remove Event
Removes an event completely.

| DELETE |    `/{token}/events/{id}`   |
|--------|:---------------------------:|
| token  | Admin identification token. |
| id     | An id of the group.         |

Response body example:
```json
{
    "result": "success"
}
```
---
