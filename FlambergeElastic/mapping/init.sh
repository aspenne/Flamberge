curl -XDELETE flamberge-elasticsearch:9200/acteur;
curl -XDELETE flamberge-elasticsearch:9200/joue_dans;
curl -XDELETE flamberge-elasticsearch:9200/film;
curl -XDELETE flamberge-elasticsearch:9200/genres;
curl -XDELETE flamberge-elasticsearch:9200/possede_genres;
curl -XDELETE flamberge-elasticsearch:9200/role;

curl -XPUT flamberge-elasticsearch:9200/acteur -H 'Content-Type: application/json' --data "@/tmp/files/acteur.json";
curl -XPUT flamberge-elasticsearch:9200/joue_dans -H 'Content-Type: application/json' --data "@/tmp/files/joue_dans.json";
curl -XPUT flamberge-elasticsearch:9200/film -H 'Content-Type: application/json' --data "@/tmp/files/film.json";
curl -XPUT flamberge-elasticsearch:9200/genres -H 'Content-Type: application/json' --data "@/tmp/files/genres.json";
curl -XPUT flamberge-elasticsearch:9200/possede_genres -H 'Content-Type: application/json' --data "@/tmp/files/possede_genres.json";
curl -XPUT flamberge-elasticsearch:9200/role -H 'Content-Type: application/json' --data "@/tmp/files/role.json";
