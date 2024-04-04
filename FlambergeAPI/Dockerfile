FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev libpq-dev

WORKDIR /app

# RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install Distance==0.1.3
RUN pip install fastapi==0.104.1
RUN pip install kmodes==0.12.2
RUN pip install numpy==1.23.5
RUN pip install pandas==2.1.1
RUN pip install psycopg2-binary
RUN pip install scikit-learn==1.3.1
RUN pip install Levenshtein
RUN pip install "uvicorn[standard]"

EXPOSE 8000

# Spécifiez l'adresse et le port d'écoute
CMD [ "uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
