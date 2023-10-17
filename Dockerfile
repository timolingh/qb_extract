# Use a base image with Python 3.10 and cron
FROM python:3.10-slim

# Copy the shell script and Python programs into the container
COPY script.sh /app/
COPY etl_utils.py /app/
COPY tables.py /app/
COPY main.py /app/
# COPY source_to_landing.py /app/
# COPY landing_to_staging.py /app/
# COPY staging_to_prod.py /app/
COPY .env /app/

# Copy the requirements.txt file and install dependencies
COPY cdata-quickbooks-connector-23.0.8669-python3.tar.gz /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set up cron job
RUN apt-get update && apt-get -y install cron
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob
RUN touch /var/log/cron.log

# Run the cron job and keep the container running
CMD cron && tail -f /var/log/cron.log