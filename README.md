 
# glendid-app-users
:zap: Welcome to Glendid, a serverless app to administrate users of the application.
You can clone this repository to explore and scalate your application. 
We use AWS as cloud service and python to make 'The magic code' :sparkles: :snake:. 

## :magic_wand: How can install this repo?
1. Clone this repo: `git clone https://github.com/Glendid/glendid-app-users.git`.
2. Install virtualenv with: `pip install virtualenv`.
3. Create a virtual env in the root folder with command `virtualenv venv`. 
4. Activate the virtual environmnet with `source env/bin/activate`
5. Install Serverless framework with `npm` or binaries following the official guide https://www.serverless.com/framework/docs/getting-started.
6. Once you have your Glendid account, sing in locally and run the command  `serverless --org=glendid` to configure the local app.
7. Create an AWS account and set your locals credentials as describe the AWS docs.
8. Once you have you local repository and your virtual environment active, install the required dependencies of the projects with `make install`.
9. Deploy the app using the command `make deploy`

## :compass: Explore the endpoints:
Use the following link to import the postman collection and discover json schemas required for each endpoint.
https://www.getpostman.com/collections/cf41ccea7052c1ba000b

## :gear: How this app is distributed?
Glendid is divided in two services: users and reports, using AWS as a infrastructure, we create CRUD operation over each service. 

Check our app architecture:

![alt text](https://i.postimg.cc/6q1v1nST/Glendid-Arquitectura.png)

