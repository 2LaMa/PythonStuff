# =============================================================================
# URL Extraction Function
# =============================================================================
#
# A specialized function returning an array of  resolved URLs from a text
#

import re
import json
import csv
from ural import get_domain_name
from urllib.parse import urlsplit
from collections import defaultdict, Counter
from tqdm import tqdm

#filepath = 'small_success.txt'
filepath = 'success_resolving.txt'
dic = {}
dic_ok =  defaultdict(list)
shorteners = set()
counteroflinks = Counter({})

with open(filepath) as fp:
    cnt = 1
    for line in tqdm(fp, total = 9419543):
       line_splitted = {}
       line = line.strip()
       linesplitted = line.split(':', 1)
       code = linesplitted[0][:3]           #get the 3 characters code at the beginning
       urls = linesplitted[1].split('->', 1)

       line_splitted['code'] = code
       line_splitted['dom1'] = urlsplit(urls[0].strip()).hostname
       line_splitted['dom2'] = urlsplit(urls[1].strip()).hostname

       dic[cnt] = line_splitted
       cnt += 1


for line in dic.values():
    counteroflinks[line['dom1']] += 1
    if (line['dom1'] != line['dom2']):
        dic_ok[line['dom1']].append(line['dom2'])


for dom in dic_ok:
    dic_ok[dom] = Counter(dic_ok[dom])


try:
    with open('shorteners.csv', 'w', newline='') as f, open('shorteners_with_metrics.csv', 'w', newline='') as f2:
        w = csv.writer(f)
        wp = csv.writer(f2)

        w.writerow(['shortener', 'redirection', 'count'])
        wp.writerow(['shortener', 'domain', 'shortener length', 'total number of redirections', 'total number of links', 'most common redirection', 'number of distinct subdomains','number of distinct domains' ])

        for short, urls in dic_ok.items():
            distinct_domains = set()
            for key, value in urls.items():
                w.writerow([short, key, value])

            domain = get_domain_name(short)
            shortener_length = len(short)
            total_size = len(list(urls.elements()))
            total_links = counteroflinks[short]
            mostcommon = urls.most_common(1)
            distinct_subdomains_size = len(urls)
            for url in urls:
                distinct_domains.add(get_domain_name(url))
            distinct_domains_size = len(distinct_domains)


            wp.writerow([short,domain, shortener_length, total_size, total_links, mostcommon, distinct_subdomains_size, distinct_domains_size])

except IOError:
    print("Could not write the CSV file")
