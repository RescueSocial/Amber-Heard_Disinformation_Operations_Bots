# SNA-AH-Links-Analysis-Cross-Platforms
**Cross-Platform Social Network Analysis of Links and analysis, monitoring of Petitions/News/Videos on Amber Heard.**

Checking the domains, links, on social platforms and search engines about a person. 
- Using APIs to get cross-platform link analysis on Change.org, YouTube for 6+ platforms.
- Using NLP and text extraction.
- Checking timelines, timestamps, social amplifications, title, descriptions, countries of links/videos/domains which are 'articles/news/videos' and astroturfed.
- Using [informationtracer.com](https://informationtracer.comstable/) for the CrowdTangle API (Enter url, hashtag, any string, files for multiple queries)
- Cross-Platform Reports on Links/Videos/Petitions

Social Network Analysis and understanding monitoring of News and checking the domains, links, with crawlers on search engines about a person. 




## Contents

- Reddit_URLs extraction notebook.
- Twitter_URLs extraction notebook.
- YouTube_URLs extraction notebook.
- Instagram_URLs extraction notebook.

## Data

- The original Data Scrapped  from the monthioned Platfroms.
[Case Data](https://cutt.us/OriginalData)

## Problems
- **Twitter URLs** were shortened, so it hould be expanded, To expand the url we should make a request, the request response should be in  certain schema otherise the expand proccess will throw an exception.


```
15632    https://t.co/Styqc2uTCH
15633    https://t.co/QufuYeWaMf
15634    https://t.co/ImM46fL4p7
15635    https://t.co/jzVoAsZhKj
15636    https://t.co/3m7bqXgJVe
```
-- The tweets that have url were 62K so we need to make more than 100K request (100K not 62K as we rerequest the link using another condition to get the original link without breaking the code).
```bash
pip install urlexpander
```
```python
import requests
import pandas as pd
import urlexpander

def unshorten_one(url):
    try:
        short = urlexpander.expand(url)
    except requests.exceptions.MissingSchema:
        short = urlexpander.expand("http://" + url)
    except requests.ConnectionError:
        short = "connection error"
        
    if "__CLIENT_ERROR__" in short or "__CONNECTIONPOOL_ERROR__"  in short:
        try:
            r = requests.get(url, allow_redirects=False)
            try:
                short = r.headers["location"]
            except KeyError:
                short = "Page doesn't exist!"
        except requests.exceptions.MissingSchema:
            r = requests.get("http://" + url, allow_redirects=False)
            try:
                short = r.headers["location"]
            except KeyError:
                short = "Page doesn't exist!"
        except requests.ConnectionError:
            short = "connection error"

    return short

df = pd.read_csv("df_tweets_4_months_urls.csv") 

# get only recordsthat has on url
df_data_2_one = df[df.n_urls == 1]

# get the short url
df_data_2_one["short_url"] =  df_data_2_one.urls.apply(lambda x: x[2:-2])

n = []
for v in df_data_2_one.short_url.iloc[45000:].values:
    try:
        n.append(unshorten_one(v))
    except:
        n.append("error")

print(len(n))
```
-- The tweets that have more than one url should be treated differently on structuring the result only, each record will be a list of urls.

-- Although applying the function on pandas df is better, I used list. The reason is the code may break so if braeked I will hav all preious appendded links, also I will know in which lin the code broke.

-- The code takes abot 15 minutes to expand 1000 urls.

-- I used Watson and AWS SageMaker for better performance, but most of data got using my ideapad 320 that got about 40% of data.

```
https://twitter.com/plove2963/status/1344847238124556290/photo/1
https://twitter.com/basta110/status/1344846462656589825/photo/1
https://twitter.com/bacacov/status/1344845107418296320/photo/1
https://twitter.com/SheaOSullivan2/status/1344841968585621504/photo/1
https://www.nickwallis.com/depp-trial
```
-- Some urls may be __error__, __Page doesn't exist!__, __connection error__, so it should be fixed after getting all urls.
 [URLs Data](https://cutt.us/URLsData)
![alt text](https://cutt.us/qrcoder.php?size=180&qr=https://cutt.us/URLsData)

## Results
[URLs Data](https://cutt.us/URLsData)
![alt text](https://cutt.us/qrcoder.php?size=180&qr=https://cutt.us/URLsData)







