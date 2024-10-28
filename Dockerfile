FROM python:3.10

RUN mkdir /fastapi_rest

WORKDIR /fastapi_rest

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
