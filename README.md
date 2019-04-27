# Yelp_Analysis
ECE 656 - University of Waterloo (Final Project)
Harshitkumar Patel (20777748)
Mohit Gupta (20754709)
Sneh Patel (20525801)

YELP - Dataset

The data for the project can be downloaded from: https://www.kaggle.com/yelp-dataset/yelp-dataset or the marmoset database can be used. Note the dataset must be downloaded and must be loaded into the local machine's database in order for the application to run.

Step 0:
Download and install Django on your local machine if it is not already installed.

Step 1:
Go into settings.py and look for the DATABASES dictionary. In this dictionary, modify the 'NAME', 'USER', 'PASSWORD', and/or 'HOST' and 'PORT' fields according to the database (containing the Yelp data) on your local machine. Note: This information must be changed according to your local machine's database in order for this application to run.

Step 2:
Change the directory to the project folder and make sure that 'manage.py' is in this folder. Then run the following commands:
 - python3 manage.py makemigrations
 - python3 manage.py migrate
 - python3 manage.py runserver 8000 (Note: This may not run because this port might be in use, if so, stop the process that is running on the port and run this command again)  

 Step 3:
 Open your browser and enter this address: http://localhost:8000/home/homepage.
