# elastic-search-with-script


To run: <br><br>
step 1: go to the folder directory <br>
step 2: then user "docker-compose up -d" in terminal for mulitple node or "docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.25"<br>
step 3: the in terminal run elastic_script.py script to update data in elastic db<br>
step 4: after updating the data then we can verify elastic search by running second script elastic_query.py<br>
step 5: happy journey
