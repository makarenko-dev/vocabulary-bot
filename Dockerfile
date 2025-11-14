FROM python:3.13-slim
WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
