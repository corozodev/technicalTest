# Test QA Suite
Demo test for new QA's.

## Getting started

Use this project to run the automated test in docker.
Commands:

### example command
docker compose exec app python3 -m pytest -rP test/test_demo.py

## Test Cases
Test website: https://demoqa.com/

- Case 1: Fill out all fields of the "Practice Form" with random values.  

- Case 2: Create a new user with random values.  

- Case 3: In the section Widgets/Select Menu, select the next values:  
    - Option Select Value: A root option  
    - Option Select One:  Ms.  
    - Option Old Style Select Menu: Indigo  
    - Option Multiselect drop down: Blue and Red,   
    - Option Standard multi select: Volvo and Opel.  

- Case 4: In the section Elements/Web Tables:  
    - Add a new element with random values.  
    - Edit the new element.  
    - Delete the new element.  

- Case 5: In the section Elements/Web Tables fill the new element form with incorrect format and empty fields.  

## Points to consider in the evaluation:
- It'll be considered to use page object model pattern.
- It's recomended to validate error cases, for example: wrong Login, field with specific formats entered wrongly.
- test's segmentation.
- The project is initially configured to be executed using Selenium. However, candidates are free to use any automation testing tool or framework they are more familiar with, as long as the proposed solution allows the assigned test cases to be executed and properly validated.   

## BONUS
As an additional bonus, candidates may perform performance tests on one or more of the application's available flows.

The candidate is free to use any performance testing tool or framework they are familiar with, such as k6, JMeter, Gatling, Locust, or any other suitable tool.

For the performance testing bonus, use the ReqRes API:

Base URL: https://reqres.in/

ReqRes requires an API key for API requests. 

Before executing the performance test:

- Create a free account in ReqRes.
- Generate an API key from the ReqRes dashboard.
- Include the following header in your requests: x-api-key: YOUR_API_KEY

Available endpoints:

GET https://reqres.in/api/users?page=2  : Retrieve a list of users.  
GET https://reqres.in/api/users/2  : Retrieve a specific user.  
POST https://reqres.in/api/users  : Create a new user.  
PUT https://reqres.in/api/users/2  : Update an existing user.  
DELETE https://reqres.in/api/users/2 : Delete an existing user.  