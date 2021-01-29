FROM python:3.8
WORKDIR /app
COPY simulate.py simulate.py
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip -r requirements.txt
ENTRYPOINT ["sh", "-c","python simulate.py --project $project --topic $topic --interval $interval"]