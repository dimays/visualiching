# VisualIChing

An open-source Django application created by David Mays, 2023


## About
[VisualIChing](https://www.visualiching.com) is a web application dedicated to providing an immersive and enlightening experience with the ancient oracle known as the I Ching. This interactive website offers a visually engaging exploration of this profound divination tool, empowering individuals to gain insights and guidance for their life's journey.


## Features
VisualIChing offers the following features:

| Feature | Description |
| -- | -- |
| Visual Hexagrams | Experience the beauty of unique watercolor paintings associated with each hexagram -- each hexagram is visually represented, providing a captivating and engaging experience |
| Create Readings | Enter your prompt or question, then virtually toss a coin or manually enter a hexagram resulting from a physical process like tossing coins or dividing yarrow stalks |
| Save Readings | Readings are automatically saved, including any of your own notes you want to keep alongside the I Ching text and hexagram paintings |
| Review Readings | Review your past readings at any time, gain insights from your former self |
| Free Account Forever | Accounts on Visual I Ching will be free forever, allowing you to freely enjoy the site without any paywall |
| Premium AI Technology | Purchase credits to access AI-assisted interpretations of your saved readings |
| Flexible Pricing | We offer a flexible credit system for accessing AI interpretations; choose from different credit bundles based on your needs and budget |


## Tech Stack
This application is built on the following tech stack:

| Technology | Role in this Project |
| -- | -- |
| Python 3.9.6 | Back-End Language |
| Django 4.2.1 | Full Stack Web Framework |
| Bootstrap 5.0.2 | Front-End CSS Framework |
| Postgres 15.3 | Database |
| Github | Continuous Deployment and Version Control |
| Heroku | Cloud Application Platform |
| Cloudflare | DNS Management and URL Forwarding |
| Sendgrid | Integrated Email Provider |
| Stripe | Integrated Credit Card Processor and Hosted Checkout Provider |
| OpenAI gpt-3.5-turbo Model | AI Model Powering AI-Assisted Interpretations |
| OpenAI Dall·E 2 | Text-to-Image AI for All Visual Content on Site |


## Installation and Local Dev Setup
To run VisualIChing locally, follow these steps:


### 1. Clone the repository

Open your terminal and navigate to whatever parent directory you'd like to clone this Git repo into.
This example assumes you will add this repo directly to your Desktop.

```
cd ~/Desktop
git clone https://github.com/yourusername/visualiching.git
```


### 2. Change into the project directory

```
cd visualiching
```


### 3. Create and activate a virtual environment

You can use any environment manager you prefer (conda, pyenv, etc.), and name the environemnt anything you'd like. For simplicity, this example uses the Python-native venv environment manager.

```
python -m venv visualiching_env
source visualiching_env/bin/activate
```


### 4. Upgrade pip and install the required dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```


### 5. Create a .env file to store your dev environment variables

Your .env file should live in the top-level directory of the project (same as the manage.py file) and must include the following variables:

| Environment Variable | API Provider | Which Services/Features This Variable is Required For |
| -- | -- | -- |
| SECRET_KEY | N/A | REQUIRED: for local hosting; you can generate one easily at [Djecrety](https://djecrety.ir/) |
| DEBUG_FLAG | N/A | REQUIRED: for `settings.py` config handling, should be set to `True` |
| WORKING_ENV | N/A | REQUIRED: for `settings.py` config handling, should be set to `dev` |
| OPENAI_API_KEY | [OpenAI](https://platform.openai.com/docs/) | OPTIONAL: AIService (AI-Assisted Interpretations), any net-new AI feature |
| VISUALICHING_SENDGRID_API_KEY | [Sendgrid](https://docs.sendgrid.com/) | OPTIONAL: Reset Password, any net-new email notification feature |
| STRIPE_SECRET_KEY | [Stripe](https://stripe.com/docs/) | OPTIONAL: Stripe Checkout inegration |
| STRIPE_PUBLISHABLE_KEY | [Stripe](https://stripe.com/docs/) | OPTIONAL: Stripe Checkout integration |
| STRIPE_WEBHOOK_SECRET | [Stripe](https://stripe.com/docs/) | OPTIONAL: Stripe Checkout integration |
| STRIPE_LOCAL_LISTENER_SECRET | [Stripe](https://stripe.com/docs/) | OPTIONAL: Stripe Checkout integration |

You can use the .envexample file in this repo as a template.

*Note: You are responsible for creating and configuring any accounts and API keys for local use and/or development on the features you wish to modify.*


### 6. Set up a local 'dev' database

This automatically creates a sqlite database in the top-level directory of the project and creates all of the models necessary for running VisualIChing.

```
python manage.py makemigrations
python manage.py migrate
```

*Note: If you would prefer using your own Postgres database instead, you can first add a record in the .env file for the DATABASE_URL variable, set to the database connection URL for your pgdb, and VisualIChing will automatically use that connection instead of creating a local sqlite database. This is the type of database connection used in production.*


### 7. Create a superuser for admin control over your local database:

```
python manage.py createsuperuser
```


### 8. Pre-populate your dev database with dev dummy data, including Users, Credits, Readings, and all the core data models (Hexagrams, HexagramLines, Trigrams, Line Types)

```
python visual_i_ching_app/devtools/add_dummy_data.py
```


### 9. Collect static files to serve up locally

```
python manage.py collectstatic
```


### 10. Start the development server

```
python manage.py runserver
```

See [this Django documentation](https://docs.djangoproject.com/en/4.2/ref/django-admin/#runserver) for more information on running a local server.

### 11. Open VisualIChing locally

Open your browser and navigate to http://localhost:8000 to access VisualIChing locally. You can login using the superuser credentials you created in step 7.


## Contributing
Contributions are welcome! If you find a bug or have a suggestion for improvement, please [open an issue](https://github.com/dimays/visualiching/issues) on the GitHub repository.

To contribute code, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.
6. Please ensure that your code follows the project's coding conventions.


## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/dimays/visualiching/blob/main/LICENSE) file for more details.


## Acknowledgements
- The renowned Wilhelm/Baynes translation of the I Ching, an ancient Chinese divination text
- The third-party service providers without whom this project would not have been possible


## Contact
If you have any questions or inquiries about VisualIChing, please contact us at visualiching@gmail.com.