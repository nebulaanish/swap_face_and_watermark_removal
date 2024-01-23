# Image API 
It is an image processing api which is made by combining the usage of several third party apis. The api has following features
- Swap the face of a person onto a different person's face.
- Remove watermark from the image. 
- Replace background (This logic is not implemented yet because of no pro account of the clipdrop api, which is essential to get this function up and running.)


## Local Deployment Steps
- Clone repository locally. 
- Create a virtual environment.
    - ``` python -m venv .venv ```
- Activate virtual environment.
    - Linux/Mac: `source .venv/bin/activate`
    - Windows: `.venv\Scripts\activate`
- Install dependencies.
    - `pip install -r requirements.txt`
- Run server.
    - `python manage.py runserver`

## Accessing swagger documentation.
- After running the server, go to the following url to access swagger documentation for the api.
`localhost:8000/docs/`

## Navigating the code base
There are separate apps for the tasks.
- `project` folder is the home, which contains settings.py and other necessary setups and boiler plate codes for the project to be up and running.
- `custom_user` folder is a separate app for defining the logics for authentication, including email login and all. 
- `image` folder is the place where core logic of the app resides. 
    - `urls.py` files defines which function written on `views.py` is called when hitting a certain url endpoint. 
    - `views.py` file contains the functions for related endpoints. It takes control of the user flow.
    - `utils.py` this is the most important file. All the core logic and behaviour is written in this file. The flow in `view.py` utilize functions written here to complete the action. 
    - `models.py` It is the folder containing entity definitions. The way in which data is stored in the database is stored here. 
- `media` folder contains the resulting image output from several apis. It also store the intermediate results in some cases. You can take a look at them after running an api to see the intermediate image, mask or the final output. 
    - `output` folder contains the final result.
    - `removebg_input` is a file setup for background task.
    - `results` folder contains the intermediate results of face swap without removing the watermark. 