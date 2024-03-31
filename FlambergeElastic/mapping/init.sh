curl -XPUT flamberge_elasticsearch:9200/artiste -H 'Content-Type: application/json' --data "@/tmp/files/artiste.json";
curl -XPUT flamberge_elasticsearch:9200/exerce_metier -H 'Content-Type: application/json' --data "@/tmp/files/exerce_metier.json";
curl -XPUT flamberge_elasticsearch:9200/film -H 'Content-Type: application/json' --data "@/tmp/files/film.json";
curl -XPUT flamberge_elasticsearch:9200/genre -H 'Content-Type: application/json' --data "@/tmp/files/genre.json";
curl -XPUT flamberge_elasticsearch:9200/metier -H 'Content-Type: application/json' --data "@/tmp/files/metier.json";
curl -XPUT flamberge_elasticsearch:9200/possede_genre -H 'Content-Type: application/json' --data "@/tmp/files/possede_genre.json";
curl -XPUT flamberge_elasticsearch:9200/role -H 'Content-Type: application/json' --data "@/tmp/files/role.json";
