# Deployment

## Table of contents

1. [Milestones](#milestones)
2. [Walkthrough](#walkthrough)
    - [Create a database](#create-a-database)
    - [Create a new Heroku app](#create-a-new-Heroku-app)
    - [Project preparation in Gitpod](#project-preparation-in-gitpod)
    - [Confirming our database](#confirming-our-database)
    - [Deploying to Heroku](#deploying-to-Heroku)
    - [Creating an AWS Account](#creating-an-aws-account)
    - [Creating AWS Groups, Policies and Users](#creating-aws-groups-policies-and-users)
    - [Create a database](#create-a-database)
    - [Connecting Django to S3](#connecting-django-to-s3)
    - [Caching, Media Files & Stripe](#caching-media-files--stripe)


## Milestones:

1. Firstly, to start, we create a new project repository on Github. In this instance and to make it easier we used default Code institute's [gitpod-full-template](https://github.com/Code-Institute-Org/gitpod-full-template).
2. After repository has been created we then click green Gitpod button to open this repository in Gitpod. There we work on building project for majority of our time.
3. After project is done we can then continue with deployment to Heroku;
4. Creating external database on ElephantSQL - as the Heroku add-ons are not available on the Student Pack;
5. And setting up hosting for our static and media files with AWS. Specifically, we will use S3 ("Simple Storage Service") for this.

## Walkthrough:

The database we have been using while building our project in Gitpod is only accessible within Gitpod. Our deployed project on Heroku will not be able to access it. So, we need to create a new database that can be accessed by our Heroku app.  

*If you don't have an ElephantSQL.com account yet, the [steps to create one are here](https://code-institute-students.github.io/deployment-docs/02-elephantsql/elephantsql-01-sign-up).

### Create a database

1. **Log in** to ElephantSQL.com to access your dashboard
2. Click **“Create New Instance”**
3. Set up your plan
   - give your plan a **Name** (this is commonly the name of the project)
   - select the **Tiny Turtle (Free)** plan
   - you can leave the **Tags** field blank
4. Select **“Select Region”**
5. Select a data center near you
   - ❗ If you receive a message saying *"Error: No cluster available in your-chosen-data-center yet"*, choose another region.
   - Note: You're free to use any of the available free data centers, be it AWS, Azure or any of the other providers.
6. Then click **“Review”**
7. Check your details are correct and then click **“Create instance”**
8. Return to the ElephantSQL dashboard and click on the **database instance name** for this project
9. In the URL section, clicking the copy icon will copy the database URL to your clipboard

Now that we have a new database instance created, in the next step we’ll create a Heroku app to connect to.

### Create a new Heroku app

1. Click **New** to create a new app
2. Give your app a name and select the region closest to you. When you’re done, click **Create app** to confirm
   - ❗ Heroku app names must be unique.
3. Open the **Settings** tab
4. Add the config var **DATABASE_URL**, and for the value, copy in your database url from ElephantSQL.
   - 🛈 Do not add quotation marks around your database url string.

With our database created, and an app ready on Heroku, we need to configure some things within our project code. We head back to Gitpod next.

### Project preparation in Gitpod

Now we can set up our project to connect to our ElephantSQL database, create our database tables by running migrations, add our shops fixtures, and confirm that it all works by creating a superuser.

Open up your Gitpod tab and follow the steps below:

1. In the terminal, install **dj_database_url** and **psycopg2**, both of these are needed to connect to your external database.

        pip3 install dj_database_url==0.5.0 psycopg2
2. Update your **requirements.txt** file with the newly installed packages

        pip freeze > requirements.txt
3. In your **settings.py** file, import dj_database_url underneath the import for os

        import os
        import dj_database_url
4. Scroll to the **DATABASES** section and update it to the following code, so that the original connection to sqlite3 is commented out and we connect to the new ElephantSQL database instead. Paste in your ElephantSQL database URL in the position indicated

        # DATABASES = {
        #     'default': {
        #         'ENGINE': 'django.db.backends.sqlite3',
        #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #     }
        # }
        
        DATABASES = {
            'default': dj_database_url.parse('your-database-url-here')
        }
   - ❗ DO NOT commit this file with your database string in the code, this is temporary so that we can connect to the new database and make migrations. We will remove it in a moment.
5. In the terminal, run the **showmigrations** command to confirm you are connected to the external database

        python3 manage.py showmigrations
6. If you are, you should see a list of all migrations, but none of them are checked off
7. Migrate your database models to your new database

        python3 manage.py migrate
8. Load in the fixtures. Please note the order is very important here. **We need to load categories first**

        python3 manage.py loaddata categories
9. **Then products**, as the products require a category to be set

        python3 manage.py loaddata products
10. Create a superuser for your new database

        python3 manage.py createsuperuser
    - 🛈 Follow the steps to create a your superuser username and password. The email address can be left blank.
11. Finally, to prevent exposing our database when we push to GitHub, we will delete it again from our settings.py - we’ll set it up again using an environment variable in the next heroku section - and reconnect to our local sqlite database. For now, your DATABASE setting in the settings.py file should look like this

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }

With that done, a good idea is to check the migrations on ElephantSQL. Let’s take a look at that next. 

### Confirming our database

Let’s confirm that the data in your database on ElephantSQL has been created.

1. On the ElephantSQL page for your database, in the left side navigation, select **'BROWSER'**
2. Click the **Table queries** button, select **auth_user**
3. When you click **'Execute'**, you should see your newly created superuser details displayed. This confirms your tables have been created and you can add data to your database. Success!

### Deploying to Heroku

1. Go back to **settings.py** and update DATABASES section as follows:

        if 'DATABASE_URL' in os.environ:
        DATABASES = {
                'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
        else:
        DATABASES = {
                'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
                }
        }
   - *IF* our app is running on Heroku where the DATABASE_URL enviroment variable will be defined, we connect to **Postgres**. *ELSE* we connect to **SQLite**.
2. Next we will have to install package called **gunicorn**, which will act as our web server:

        pip3 install gunicorn
3. And **freeze** that into our requirements file.

        pip3 freeze > requirements.txt
4. Now we can create our **Procfile** to tell Heroku to create a web dyno. In our root directory lets create a file named 'Procfile' and inside insert the code: 

        web: gunicorn **project_name_here**.wsgi:application
5. Then, in heroku, navigate to **settings / config vars** and 'Add' new entry: **DISABLE_COLLECTSTATIC** with the value of **1**.
This is to stop heroku from collecting any static files when we deploy.
6. We'll need to add the **hostname** of our Heroku app to ALLOWED_HOSTS in **settings.py**. We'll also add **localhost** in here so that Gitpod can work too.


        ALLOWED_HOSTS = ['project-name.herokuapp.com', 'localhost']
7. Now lets **add, commit and push** these changes to Github, and then **deploy** to Heroku, either manually or trough CLI with commands:

        git add .
        git commit -m "Your commit"
        git push
        git push heroku main

   - NOTE: If you want your project to be automatically deployed to heroku when pushing your work to github you can. To do so, In heroku go to the deploy tab, and in the 'deployment method' section connect it to github. You will need to search for your repository and once found click 'connect'. Then scroll down and click 'Enable automatic deploys'. Now when you push to github your code will automatically deploy to Heroku as well.

- Your app will now be deployed, albeit without any static files, but this will be fixed when setting up AWS, documented below.
8. Lastly, generate new Django SECRET_KEY and add it to **Config Vars** in Heroku.
   - 🛈 Just google django secret key generator to find one  

   And then in **settings.py** replace the secret key setting with the call to get it from the enviroment and use an empty string as a default.

        SECRET_KEY = os.environ.get('SECRET_KEY', '')

### Creating an AWS Account

If you haven't, please create free [AWS account](https://portal.aws.amazon.com/billing/signup#/start/email) and enter billing information (you will not be charged for the purposes of this project).

1. Once you have created an account and logged in, under the All Services>Storage menu, click the link that says S3.
2. On the S3 page you will need to create a new bucket. To do this click the orange button that says 'Create Bucket'.
3. Name the bucket and select the closest region to you. To keep things simple I recommend naming the bucket after your project's name.
4. Under 'Object Ownership' select 'ACLs enabled' and leave the Object Ownership as Bucket owner preferred. 
5. Uncheck the 'Block all public access' checkbox and check the warning box to acknowledge that the bucket will be made public, then click create bucket. 
6. Once created, click the bucket's name and navigate to the properties tab. Scroll to the bottom and under 'Static website hosting' click 'edit' and change the Static website hosting option to 'enabled'. Copy the default values for the index and error documents and click 'save changes'.
7. Now navigate to the permissions tab, scroll down to the Cross-origin resource sharing (CORS) section, click edit and paste in the following code:

        [
          {
              "AllowedHeaders": [
                  "Authorization"
              ],
              "AllowedMethods": [
                  "GET"
              ],
              "AllowedOrigins": [
                  "*"
              ],
              "ExposeHeaders": []
          }
        ]
8. Then scroll back up to the 'Bucket Policy' section. Click 'edit' and then 'Policy generator'. This should open the AWS policy generator page.
9. From here under the 'select type of policy' dropdown menu, select 'S3 Bucket Policy'. Then inside 'Principle' allow all principals by typing a *.
10. From the 'Actions dropdown menu select 'Get object'. Then head back to the previous tab and locate the Bucket ARN number. Copy that, return to the policy generator and paste it in the field labelled Amazon Resource Name (ARN).
11. Once that's completed click 'Add statement', then 'Generate Policy'. Copy the policy that's been generated and paste it into the bucket policy editor.
12. Before you click save, add a '/*' at the end of your resource key. This is to allow access to all resources in this bucket.
13. Once those changes are saved, scroll down to the Access control list (ACL) section and click 'edit'.
14. Next to 'Everyone (public access)', check the 'list' checkbox. This will pop up a warning box that you will also have to check. Once that's done click 'save'.

### Creating AWS Groups, Policies and Users

1. Now that our bucket is ready we need to create a user to access it. In the search bar at the top of the window, search for IAM and select it.
2. Once on the IAM page, click 'User Groups' from the side bar, then click 'Create group'.
3. Name the group 'manage-*your-project-name*' and click 'Create group' at the bottom of the page. 
4. Then from the sidebar click 'Policies', then 'Create policy'.
5. Go to the JSON tab and click 'import managed policy'. Search for 'S3' and select 'AmazonS3FullAccess' and click import.
6. Once this is imported you will need to edit it slightly. Go back to your bucket and copy your ARN number. Head back to this policy and update the Resource key to include your ARN, and another line with your ARN followed by a /*. It should end up looking something like this: 
 
        {
                "Version": "2012-10-17",
                "Statement": [
                {
                        "Effect": "Allow",
                        "Action": [
                        "s3:*",
                        "s3-object-lambda:*"
                        ],
                        "Resource": [
                        "YOUR-ARN-NO-HERE",
                        "YOUR-ARN-NO-HERE/*"
                        ]
                }
                ]
        }

7. Click 'Next: Tags', 'Next: Review', and on this page give the policy a name. This could be something as simple as the project name followed by the word policy, and then a short description eg: Access to S3 bucket for 'YOUR PROJECT' static files. Then click 'Create policy'. 
8. This will take you back to the policy page where you should be able to see your newly created policy. Now we need to attach it to the group we created.  
9. Click 'User groups', and click the group you created earlier. Go to the permissions tab and click 'Add permission' and from the dropdown click 'Attach policies'. 
10. Find the policy you just created, select it and click 'Add permissions'.
11. Finally you need to create a user to put in the group. Select users from the sidebar and click 'Add user'.  
12. Give your user a user name, check 'Programmatic Access', then click 'Next: Permissions'. 
13. Select your group that has the policy attached and click 'Next: Tags', 'Next: Review', then 'Create user'.
14. On the next page, download the CSV file. This contains the user's access key and secret access key which you will need later. 

### Connecting Django to S3

Now that we have created a S3 bucket with its user group attached, we need to connect it to django.

1. First we will need to install two packages. Boto3 and Django storages. Do this by running these commands:  

        pip3 install boto3
        pip3 install django-storages

    And remember to freeze the requirements with:  

        pip3 freeze > requirements.txt

2. You will then need to add 'storages' to your installed apps section inside your settings.py file. Do that now. 
3. Next, we will need to add some additional settings to the same file to let django know what bucket it's communicating with. 
4. Somewhere near the bottom of the file you should write an if statement to check if there is an environment variable called USE_AWS. This variable does not exist yet but we will add it later. Inside the if statement, write the following settings so it looks like this:

        if 'USE_AWS' in os.environ:
                AWS_STORAGE_BUCKET_NAME = 'insert-your-bucket-name-here'
                AWS_S3_REGION_NAME = 'insert-your-region-here'
                AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
                AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

5. Next, hop back to heroku and in the settings tab, under config vars, you will need to add some keys with values that were downloaded earlier in the CSV file.
6. Add the key, AWS_ACCESS_KEY_ID with the value that was generated in the CSV file earlier. Then add the key AWS_SECRET_ACCESS_KEY, and again add the value that was generated in the CSV file. Once they have both been added, add the key USE_AWS, and set the value to True.
7. You can now also remove the DISABLE_COLLECTSTAIC variable, since django should now collect static files automatically and upload them to S3.
8. Now head back to the settings.py file in your django project and head back to the if statement we wrote earlier and inside the statement add this line setting:  

        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    This is to tell django where our static files will be coming from in production.
9. Next we need to create a file to tell django that we want to use S3 to store our static files whenever someone runs collectstatic and also that we want any uploaded product images to go there also.
10. In the root directory of your project create a file called 'custom_storages.py'. Inside this file you will need to import your settings as well as the s3boto3 storage class. So at the top of the file insert the code:  

        from django.conf import settings
        from storages.backends.s3boto3 import S3Boto3Storage

11. Then underneath the imports insert these two classes:  

        class StaticStorage(S3Boto3Storage):
                location = settings.STATICFILES_LOCATION


        class MediaStorage(S3Boto3Storage):
                location = settings.MEDIAFILES_LOCATION

    The STATICFILES_LOCATION and MEDIAFILES_LOCATION have yet to be defined, so lets do that now.
12. Back in the settings.py file, underneath the bucket config settings but still inside the if statement, add these lines:  

        STATICFILES_STORAGE = 'custom_storages.StaticStorage'
        STATICFILES_LOCATION = 'static'
        DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
        MEDIAFILES_LOCATION = 'media'

13. Next, you will also need to override and explicitly set the URLs for static and media files using your custom domain and new locations. To do this add these two lines inside the same if statement:  

        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

14. If you now save, add, commit and push your changes, you should see that your S3 bucket now has a static folder with all your static files inside. Next, we need to handle the Media files but first, inside the if statement add the following code. This helps to speed things up by letting the browser know that its ok to cache static files for a long time:    

        AWS_S3_OBJECT_PARAMETERS = {
                'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
                'CacheControl': 'max-age=94608000',
        }

### Caching, Media Files & Stripe

1. Back in S3, go to your bucket and click 'Create folder'. Name the folder 'media' and click 'Save'. 
2. Inside the new media folder you just created, click 'Upload', 'Add files', and then select all the images that you are using on your site.
3. Then under 'Permissions' select the option 'Grant public-read access' and click upload. You may need to also check an acknowledgment warning checkbox too. 
4. Once that is finished you're all set. All your static files and media files should be automatically linked from django to your S3 bucket.

**Stripe** is needed to handle the checkout process when a payment is made. You can sign up for account [here](https://stripe.com/en-gb). To set up stripe payments you can follow their guide [here](https://stripe.com/docs/payments/accept-a-payment#web-collect-card-details).

6. Now, we will set up a webhook, sign into your stripe account and click 'Developers' located in the top right of the navbar.
7. Then in the side-nav under the Developers title, click on 'Webhooks', then 'Add endpoint'.
8. On the next page you will need to input the link to your heroku app followed by /checkout/wh/. It should look something like this:  

        https://your-app-name.herokuapp.com/checkout/wh/

9. Then click '+ Select events' and check the 'Select all events' checkbox at the top before clicking 'Add events' at the bottom. Once this is done finish the form by clicking 'Add endpoint'.
10. Your webhook is now created and you should see that it has generated a secret key. You will need this to add to your heroku config vars.
6. Head over to your app in heroku and navigate to the config vars section under settings. You will need the secret key you just generated for your webhook, in addition to your Publishable key and secret key that you can find in the API keys section back in stripe.
7. Add these values under these keys:  

        STRIPE_PUBLIC_KEY = 'insert your stripe publishable key'
        STRIPE_SECRET_KEY = 'insert your secret key'
        STRIPE_WH_SECRET = 'insert your webhooks secret key'

8. Finally, back in your setting.py file in django, insert the following near the bottom of the file:  

        STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
        STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
        STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

[⮪ Return back to readme](README.md) | [Back to Top 🠕](#deployment)