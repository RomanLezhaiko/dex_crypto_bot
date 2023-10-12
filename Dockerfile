FROM python:3.11.6-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV NODERPC https://bsc-dataseed4.bnbchain.org
ENV API_KEY_BSC_SCAN 8T1Y4NY8CPPY5KVPNZ65MZ7HAMMYGSUZ83

RUN apk update && apk add bash 

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
EXPOSE 8000