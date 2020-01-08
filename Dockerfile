FROM python:3.6-slim
ARG user
ARG password
ADD requirements.txt /
RUN pip install --upgrade --extra-index-url https://$user:$password@distribution.livetech.site -r /requirements.txt
ADD . /innolva-spider
ENV PYTHONPATH=$PYTHONPATH:/innolva-spider
WORKDIR /innolva-spider/innolva_spider/services
CMD python services.py
