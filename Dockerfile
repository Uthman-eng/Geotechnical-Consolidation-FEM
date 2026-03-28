FROM dolfinx/dolfinx:stable

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["streamlit", "run", "app.py"]