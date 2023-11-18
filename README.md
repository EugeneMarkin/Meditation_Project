### Installatiton

1. Copy the mp3 files to `meditation_project/input` directory

2. Go into the project directory

`cd meditation_prject`

3. Install required dependencies

`pip install -r requirements.txt`

4. Prepare the collection of files for generation

`python local.py prepare`



### Local use

From the 'meditation_project' run:

`python local.py generate`

Find the resulting file at: 

`meditation_project/output/out.mp3`



### Run server on localhost

1. Start the server 

​		`python manage.py runserver`

2. Access the api endpoint at:

   `http://127.0.0.1:8000/mserver/stream-audio/`

