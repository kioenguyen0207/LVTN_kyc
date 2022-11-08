FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y cmake 
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 443
# CMD [ "python", "app.py" ]
# ENTRYPOINT ["./gunicorn.sh"]
CMD [ "gunicorn", "app:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:443" ]