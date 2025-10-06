# base operating system and python version
FROM python:3.11-slim


# setting up clean folder inside Container - workspace
WORKDIR /app

# install python packages first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of our app code
COPY . .

# start button - tells the container what command to RUN
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]