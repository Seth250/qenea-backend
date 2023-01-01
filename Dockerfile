# pull the official base image
FROM python:3.10-bullseye

LABEL maintainer="ayowaleakintayo@gmail.com"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# non-empty value ensures python output (stdout, stderr) is sent to the terminal without buffering
ENV PYTHONUNBUFFERED 1
# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT 1

# set working directory
WORKDIR /app

# copy pipfiles first to working directory (also helps cache the layer)
COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

# install dependencies
RUN pipenv install --system --deploy

# copy project to working directory
COPY . ./

# collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# chmod +x changes a file mode to executable
RUN chmod +x ./run.sh

CMD ["./run.sh"]