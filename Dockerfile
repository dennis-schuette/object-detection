from python:3.9-slim

# RUN apt update && \
#     apt install --no-install-recommends -y build-essential gcc && \
#     apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# RUN pip3 install --no-cache-dir -r requirements.txt

RUN chgrp -R 0 /app/wsgi.py \
    && chmod -R g=u /app/wsgi.py \
    && pip3 install pip --upgrade \
    && pip3 install -r requirements.txt

EXPOSE $PORT

#CMD gunicorn app:server --bind 0.0.0.0:8080 --preload
ENTRYPOINT ["python3"]
CMD ["wsgi.py"]