FROM python:3.7

# Copy requirements.txt to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

# Copy backend app code
COPY ./ /app

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]