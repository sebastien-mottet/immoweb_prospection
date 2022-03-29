FROM python:3.8-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY . /code/

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get update && apt-get -y install cron python3-pip python3-dev wget xvfb unzip

RUN apt-get install -y libgconf-2-4

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update && apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 99.0.4844.51
ENV CHROMEDRIVER_DIR /usr/local/bin

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN pip3 install -r requirements.txt

# Copy scrapper-cron file to the cron.d directory
COPY scrapper-cron /etc/cron.d/scrapper-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/scrapper-cron

RUN chmod 0744 /code/scrapper.py

# Apply cron job
RUN crontab /etc/cron.d/scrapper-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
