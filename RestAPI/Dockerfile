FROM python:3.7

WORKDIR /home/RestAPI

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python","searchNews.py"]
