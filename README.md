### Project Structure  

```
├── car-list.json
├── create_url.py
├── detailed_crawl.py
├── environment.yml
├── README.md
├── requirements.txt
└── short_crawl.py
```


In general, web-crawling has some real-world applicability.  
I can search and create specific datasets when there is nothing public.  
Or as a byproduct, I can help with data wrangling. Data on the web comes in different formats, and often something must be changed.   
There are dedicated tools in Data Engineering that handle this, tools like Kafka, Apache-Spark, Hadoop etc.  


In this project, I crawl the **olx.ro** site for auto ads and send the result of the crawl via email.  

Within this project I define 4 scripts:  
* one that creates the **search URL** and exports it as an environment variable  
* a script that gets the detailed description of the add  
* a short description  
* email notification script  

### Usage examples

For better readibility export the results of the crawl with datetime format.  

```
scrapy crawl {script.name} -o '%(time)s_scraperesults.csv' --nolog  
```

### Release 2

In release 2, I created a URL exporter. In the previous release, I used hardcoded URLs in the python script.  
The idea is to export the search URL and make it part of the environment variable.  
The URL is created based on specific search options.  


Ref:  
* https://stackoverflow.com/questions/43914442/how-to-create-file-name-of-feed-export-dynamically-using-scrapy-command  
* https://docs.scrapy.org/en/latest/topics/feed-exports.html  
