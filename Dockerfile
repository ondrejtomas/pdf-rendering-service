FROM python:3.6

WORKDIR /opt/app/

COPY . /opt/app/

RUN pip3 install --upgrade pip && pip3 install -I -r ./requirements/base.txt

ENV PYTHONPATH "."

ENTRYPOINT ["python", "./src/app.py"]
