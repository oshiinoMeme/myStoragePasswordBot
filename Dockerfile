
FROM python:3.9-slim-buster

# set environment variables
ENV PYTHONUNBUFFERED=1

# create a working directory
WORKDIR /passwordBot

# copy the requirements file
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the source code
COPY . .

# start the bot
CMD ["python", "ftgb.py"]



