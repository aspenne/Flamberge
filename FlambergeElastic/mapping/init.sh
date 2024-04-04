curl -XDELETE flamberge-elasticsearch:9200/artiste;
curl -XDELETE flamberge-elasticsearch:9200/joue_dans;
curl -XDELETE flamberge-elasticsearch:9200/film;
curl -XDELETE flamberge-elasticsearch:9200/genre;
curl -XDELETE flamberge-elasticsearch:9200/possede_genre;
curl -XDELETE flamberge-elasticsearch:9200/role;

curl -XPUT flamberge-elasticsearch:9200/artiste -H 'Content-Type: application/json' --data "@/tmp/files/artiste.json";
curl -XPUT flamberge-elasticsearch:9200/joue_dans -H 'Content-Type: application/json' --data "@/tmp/files/joue_dans.json";
curl -XPUT flamberge-elasticsearch:9200/film -H 'Content-Type: application/json' --data "@/tmp/files/film.json";
curl -XPUT flamberge-elasticsearch:9200/genre -H 'Content-Type: application/json' --data "@/tmp/files/genre.json";
curl -XPUT flamberge-elasticsearch:9200/possede_genre -H 'Content-Type: application/json' --data "@/tmp/files/possede_genre.json";
curl -XPUT flamberge-elasticsearch:9200/role -H 'Content-Type: application/json' --data "@/tmp/files/role.json";
