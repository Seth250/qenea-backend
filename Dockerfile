# pull the official base image
FROM python:3.10-bullseye

LABEL maintainer="ayowaleakintayo@gmail.com"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# non-empty value ensures python output (stdout, stderr) is sent to the terminal without buffering
ENV PYTHONUNBUFFERED 1
# tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT 1

# set working directory
WORKDIR /app

# copy pipfiles first to working directory (helps cache the layer)
COPY Pipfile Pipfile.lock ./

# install dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy

# copy project to working directory
COPY . ./

# collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# create custom non-root user and group
RUN useradd -U --no-create-home app
# change the project owner and group to the one created (helps prevent permission errors)
RUN chown -R app:app ./

USER app

# chmod +x changes file mode to executable (the -R flag makes it run recursively on a directory)
RUN chmod -R +x ./scripts

CMD ["./scripts/run.sh"]
