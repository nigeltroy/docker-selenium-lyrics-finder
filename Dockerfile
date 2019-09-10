FROM joyzoursky/python-chromedriver:3.6-xvfb-selenium

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV NAME World

ENTRYPOINT ["python3", "lyricsFinder.py"]
CMD ["all star"]