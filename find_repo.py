import requests
import json
import sys
import time
page, wrote_urls = 1, 0
username = ""
password = ""
fw = open('Projects2019.csv', 'w')
fw.write('url\n')
while True:
    url1 = "https://api.github.com/search/repositories?q=language:java+pushed:>2020-01-01+created:>2019-01-01&page=%d"%page
    try:
        r1 = requests.get(url1, auth=(username, password))
        j1 = json.loads(r1.text)
        total_repos = j1['total_count']
    except:
        time.sleep(5)
        continue
    for idx, item in enumerate(j1['items']):
        try:
            full_name = item['full_name']
            url2 = "https://api.github.com/repos/%s/stats/commit_activity"%full_name
            time.sleep(0.5)
            r2 = requests.get(url2, auth=(username, password))
            j2 = json.loads(r2.text)
            total_commits = 0
            for week in j2:
                total_commits += week['total']
        except:
            time.sleep(5)
            print(r2.text)
        try:
            url3 = "https://api.github.com/search/code?q=repo:%s+filename:pom.xml"%full_name
            time.sleep(0.5)
            r3 = requests.get(url3, auth=(username, password))
            j3 = json.loads(r3.text)
            maven = j3['total_count']
            if total_commits > 100 and maven > 1 and total_commits < 200:
                fw.write("https://github.com/%s\n" % full_name)
                wrote_urls += 1
                print("write " + full_name, ', total: %d' % wrote_urls)
            print(page, idx, total_repos)
        except:
            time.sleep(5)
            print(r3.text)
    page += 1