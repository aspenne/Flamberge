FROM php:latest

WORKDIR /app

RUN apt-get update \
  && apt-get install -y \
  libpq-dev \
  && docker-php-ext-install pdo pdo_pgsql             

EXPOSE 80

CMD ["php", "-S", "0.0.0.0:80"]
