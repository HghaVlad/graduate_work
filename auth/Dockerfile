FROM python:3.12.4

WORKDIR /opt/app

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/bin/bash", "./run_auth_service.sh" ]
# ENTRYPOINT [ "python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000" ]
