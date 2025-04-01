# Face Swap and Watermark Removal 
It is an api that allows swapping of faces to the target face while also removing any logo/watermark in the image. The current build only supports removal of any one most prominent logo, it can be improvised to remove every logo present in an image. The process is explained below.

1. Pass image and face url to Faceswap api.
2. Detect logo with google's vision api.
3. Create a mask of the image where logo is to be removed.
4. Pass it to inpainting api at clipdrop.

**Examples**

<table>
    <thead>
        <tr>
            <th>Image</th>
            <th>Face</th>
            <th>Face Swap Result</th>
            <th>Final Result</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><img src="samples/input/image1.png" alt="Image 1"></td>
            <td><img src="samples/input/face.png" alt="Image 1">  </td>
            <td><img src="samples/faceswap_result/face1.jpg" alt="Image 1"></td>
            <td><img src="samples/final/final1.jpg" alt="Image 1"></td>
        </tr>
        <tr>
            <td><img src="samples/input/image2.png" alt="Image 1"></td>
            <td><img src="samples/input/face.png" alt="Image 1">  </td>
            <td><img src="samples/faceswap_result/face2.jpg" alt="Image 1"></td>
            <td><img src="samples/final/final2.jpg" alt="Image 1"></td>
        </tr>
        
   
</table>

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