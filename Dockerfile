FROM python:3

WORKDIR /opt/

COPY . /opt/

RUN pip install -r /opt/requirements.txt

ENV PYTHONPATH=/opt/

# setting up DB
RUN python /opt/manage.py makemigrations
RUN python /opt/manage.py migrate

# adding sample data to DB
RUN python /opt/load_data.py

# running webserver as process #1
CMD [ "python", "/opt/manage.py", "runserver", "0.0.0.0:8000" ]