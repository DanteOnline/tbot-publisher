from python

COPY ./bot/ ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt