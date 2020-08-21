import config
import json
import os
import pprint
import requests

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

    # Only classifying top 150 (allow some space to remove bad tags)
    taglist150 = taglist[:151]
    
    # Remove unnecessary data
    def del_tags(tag):
        del tag['category']
        del tag['created_at']
        del tag['updated_at']
        del tag['is_locked']
        return tag

    reduced_taglist = list(map(del_tags, taglist150))

    # Write to file so we don't have to pull everytime
    with open('characters.json', 'w') as fp:
        json.dump(reduced_taglist, fp, indent=4)

    return reduced_taglist

def pull_images(client, taglist):
    for tag in taglist:
        try:
            os.mkdir(f'images/{tag["name"]}')
        except OSError:
            print(f'Creation of {tag["name"]} failed')
        else:
            pull_images_for_character(client, tag)

def pull_images_for_character(client, char_data):
    num_added = 0
    page_num = 1
    while num_added < 100:
        postlist = client.post_list(limit=100, page=page_num, tags=char_data['name'])
        for post in postlist:
            if 'file_ext' in post and post['file_ext'] == 'jpg' and post['tag_count_character'] == 1:
                response = requests.get(post['file_url'])
                with open(f'images/{char_data["name"]}/{char_data["name"]}{num_added}.jpg', 'wb') as fp:
                    fp.write(response.content)
                    num_added += 1
        page_num += 1

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    client = Danbooru('danbooru', username=config.user, api_key=config.api_key)
    taglist = get_characters(client)
    pull_images(client, taglist)