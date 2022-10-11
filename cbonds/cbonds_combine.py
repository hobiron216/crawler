import json
import os
import codecs

def dict_clean(items21):
    result = {}
    for key, value in items21.items():
        if value is None:
            value = ''
        result[key] = value
    return result

final_data = []
for root, dirs, files in os.walk("/dataph/one_time_crawling/home/cbonds/"):
    for file in files:
        raw_json = root + file

        # print(raw_html)
        f = codecs.open(raw_json, 'r', encoding="utf-8")
        json_data = json.load(f)
        for data in json_data:
            data = dict_clean(data)
            final_data.append(data)



with open("/dataph/one_time_crawling/home/cbonds/cbonds.json",'w',encoding='utf8') as outfile:
    json.dump(final_data, outfile,  ensure_ascii=False)