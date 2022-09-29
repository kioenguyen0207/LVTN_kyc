FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
EXPOSE 443
# CMD [ "python", "app.py" ]
# ENTRYPOINT ["./gunicorn.sh"]
CMD [ "gunicorn", "app:app", "-w", "1", "--threads", "1", "-b", "0.0.0.0:443" ]