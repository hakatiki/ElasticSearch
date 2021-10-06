# ElasticSearch

I did not create the docker container on AWS, since I am not that experienced with cloud

I created the docker container with elasticsearch. The commands:
  
  >docker pull docker.elastic.co/elasticsearch/elasticsearch:7.15.0

  >docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.15.0


Then I found Crawler.py on github. It was in python2 so I had to modify it.
