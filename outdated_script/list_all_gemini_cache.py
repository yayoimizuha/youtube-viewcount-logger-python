from json import load

with open("gemini-cache.json", mode="r", encoding="utf-8") as f:
    cache_dict: dict = load(f)
for item in cache_dict.keys():
    # print(f"{item} → {cache_dict[item]['song_name']} : {','.join(cache_dict[item]['singer'])}", end='')
    # if cache_dict[item]['edition'] != '':
    #     print(' - ' + cache_dict[item]['edition'], end='')
    # if cache_dict[item]['version'] != '':
    #     print(' - ' + cache_dict[item]['version'], end='')
    # print()
    print(item)
