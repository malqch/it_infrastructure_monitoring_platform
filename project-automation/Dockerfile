FROM centos-python3:latest
MAINTAINER malq
#RUN yum update -y && \
#yum install -y python3-pip python3-dev
#RUN yum install mysql-devel -y
#COPY ./requirements.txt /requirements.txt
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
#COPY . /
#ENTRYPOINT [ "python3" ]
#CMD [ "manage.py", "runserver", "0.0.0.0:8001" ]
#CMD [ "gunicorn", "-b", "0.0.0.0:8001", "--worker-class=gevent", "project-asset.wsgi:application" ]
RUN chmod -R +x gunicorn_automation_run.sh
ENTRYPOINT ["/bin/bash"]
CMD [ "gunicorn_automation_run.sh" ]
