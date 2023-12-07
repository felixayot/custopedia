# Project Custopedia
## Background information
This project is my portfolio project built during my learning journey in the [ALX](https://www.alxafrica.com) Software Engineering programme to showcase my skills gained thus far. This project summarizes my ability to execute a complete Software Development Cycle stages. I handled the Planning, Development/Building, Testing, Deployment, Testing and Production as well as future Maintenance of this awesome software application.

[Custopedia](https://www.custopedia.tech) is a customer online support tool for users that consume a given organization's products and services. It's core features include:
  - Knowledge base in a Q & A manner
  - Raise an issue with a ticket custom-tailored to the concerned department of that institution as opposed to the usual  general customer care desk.
  - Live chat bot with realtime responses(Still a WIP).

![Custopedia home page](home_page.png)

More details on the inspiration to this project as well as a detailed tech stack leveraged, visit the below links where I wrote a blog on my journey and experience on this project.
- [Project proposal](https://github.com/felixayot/ALX_SE_important_concepts/blob/master/custopedia.md)
- [MVP Specification](https://github.com/felixayot/ALX_SE_important_concepts/blob/master/custopedia_mvp_specification.md)

## Tech stack overview
Below is a brief overview of the tech stack levereged to bring [Custopedia](https://custopedia.tech) to life.
### Frontend

- `Jinja2` templating
- `Bootstrap` CSS styling
- `SASS`(Syntactically Awesome Style Sheets)

### Backend

- `Flask-Python3`
- `SQLite` for development and `MySQL` for production.
- `nginx` webserver for static data and `gunicorn` for the serving the dynamic application contents.


# Installation
### Prerequisites
- Ubuntu 20.04 LTS - Operating system required.

This project was developed and tested on an `Ubuntu 20.04 LTS` terminal. Using other Ubuntu versions may result in some
incompatibility issues. If you're not on an Ubuntu 20.04 LTS terminal/os/VM, I'd suggest using a `docker` container spinning the Ubuntu 20.04 LTS image for full functionality of the app.

- Python3 - Installed in your local terminal/vagrant/VM/docker container

### Getting started
Clone the repository to your local terminal, Ubuntu 20.04 LTS remember, then create a virtual environment using:
`Python3 -m venv venv` then launch that virtual environment while you're in the repo's root directory with this command:
`source venv/bin/activate`. You'll need this virtual environment to run the application successfully with all it's required packages without affecting any of your previously globally installed packages in your local machine.
#### NOTE:
You will have have to configure the environment variables with your own values in order to run the application. 

Once you're in the virtual environment, you can install the rest of the packages required to run the application located in the `requirements.txt` file. Use this command:
`pip install -r requirements.txt` 


# Usage

Now you're ready to start running the application locally(in the development server) in your machine.
You can run it using either of these two commands:
  - `Python run.py` or
  - `flask run`
It'll be listening on port 5000 by default. You can browse it in your browser and test out it's awesome features and functionalities.


# Contribution

All contributions to help improve the application's features and functionalities are welcome. Fork the repository and create a pull request with your modifications. I'll be sure to review them.


# Authors

- Felix Ayot - [Github](https://github.com/felixayot) / [LinkedIn](https://www.linkedin.com/in/felix-ayot-51a006124) / [X](https://twitter.com/felix_ayot)  


# License🧾📜

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
