FROM  python:3.8
ENV PYTHONBUFFFERED 1
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app/
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "initadmin"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

COPY entrypoint ./entrypoint
RUN sed -i 's/\r$//g' ./entrypoint
RUN chmod +x ./entrypoint

COPY start ./start
RUN sed -i 's/\r$//g' ./start
RUN chmod +x ./start

ENTRYPOINT ["sh","./entrypoint"]
#CMD ["sh","./start"]
#RUN chown root /app/start


