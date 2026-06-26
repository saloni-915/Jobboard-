# Base image - Python 3.13

FROM python:3.13-slim
# working directory set karo
WORKDIR /app 

# System dependecies (MySQL client ke liye)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# requarement.txt copy
COPY requarements.txt .

# Python packages install karo
RUN pip install --no-cache-dir -r requarements.txt

# project code copy karo
COPY . .

# static files collect 
#RUN python manage.py collectstatic --noinput 

# port exxpose karo
EXPOSE 8000

# server start 
#CMD ["python","manage.py","runserver","0.0.0.0:8000"]
