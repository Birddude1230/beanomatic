FROM python:3.9-slim as base

########## FROM
# https://sourcery.ai/blog/python-docker/

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV DISCORD_TOKEN_FILE /home/appuser/normal_file.txt

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Get nltk corpus bits (not working)
#RUN python -m nltk.downloader stopwords

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY ./*.py ./
COPY ./Pipfile ./
COPY ./config.json ./
COPY ./normal_file.txt ./

CMD [ "python", "./main.py" ]