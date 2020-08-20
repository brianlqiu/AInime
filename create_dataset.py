import config
import json
import os.path

from pybooru import Danbooru
from os import path

# Gets the top 520 characters with names starting at each letter of alphabet
# Workaround since API doesn't allow to pull from straight up top 100 characters
# Rewrite
def get_characters(client):
    # Avoid pulling repeatedly
    if path.exists('characters.json'):
        with open('characters.json', 'r') as cf:
            json_data = cf.read()
        return json.loads(json_data)

    taglist = []
    for offset in range(26):
        letter = chr(ord('a') + offset)
        taglist.extend(client.tag_list(name_matches=f'{letter}*', category='4', order='count'))

    # Sort by popularity/count
    taglist.sort(key=lambda tag: tag['post_count'], reverse=True)

    # Remove unnecessary data
    def del_tags(tag):
        del tag['category']
        del tag['created_at']
        del tag['updated_at']
        del tag['is_locked']
        return tag

    reduced_taglist = list(map(del_tags, taglist))

    # Write to file so we don't have to pull everytime
    with open('characters.json', 'w') as fp:
        json.dump(reduced_taglist, fp, indent=4)

    return reduced_taglist

if __name__ == '__main__':
    client = Danbooru('danbooru', username=config.user, api_key=config.api_key)
    print(get_characters(client))