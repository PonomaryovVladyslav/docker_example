FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /workdir
COPY requirements.txt /workdir/
RUN pip install -r requirements.txt
COPY . /workdir/