FROM python:3.11-bullseye

# Create app directory
WORKDIR /app

# workaround to be able to install postgresql-client in slim version
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man7

# Install system libraries, libxrender1 libfontconfig libxtst6 are required for wkhtmltopdf
RUN apt update && apt install python-dev postgresql-client libxslt-dev libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev wget libxrender1 libfontconfig libxtst6 -y

# Install patched version of wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz \
    && tar xf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz \
    && mv ./wkhtmltox/bin/* /usr/bin/

# Install poetry so we can use it to install all the dependencies
RUN pip install poetry

# Install dependencies
ADD pyproject.toml .
ADD poetry.lock .

# install dependencies with poetry and avoid to create a virtualenv
RUN poetry config virtualenvs.create false && poetry install

# Bundle app source
COPY . /app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
