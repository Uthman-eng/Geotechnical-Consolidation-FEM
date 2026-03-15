FROM dolfinx/dolfinx:stable
# add stable exact code 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app


# copy project files (optional for dev, useful for CI)
COPY . /app

# default to an interactive shell

CMD ["bash"]
