#
FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#un
COPY . /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080" , "&", "streamlit", "run", "appui.py". "--server.port", "80", "--server.address", "0.0.0.0"]
