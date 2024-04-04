FROM php:latest

WORKDIR /app

# Installation d'Elasticsearch
RUN apt-get update \
  && apt-get install -y \
  wget \
  apt-transport-https \
  gnupg \
  && wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - \
  && echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list \
  && apt-get update \
  && apt-get install -y elasticsearch \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Installation des extensions PHP nécessaires pour Elasticsearch
RUN docker-php-ext-install sockets


RUN apt-get update \
  && apt-get install -y \
  libpq-dev \
  && docker-php-ext-install pdo pdo_pgsql             

EXPOSE 80

CMD ["php", "-S", "0.0.0.0:80"]
