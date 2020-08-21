import config, json, os, pprint, requests, sys, argparse

from pybooru import Danbooru
from os import path

# Define characters whose characters have more than 1 tag, since these are subsets of some other (all) tag
char_exceptions = {'saber', "jeanne_d'arc_(fate)", "jeanne_d'arc_(alter)_(fate)", 'tamamo_no_mae_(fate)'}

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

# Pull images for the given tags/characters
def pull_images(client, taglist, idx_offset=0):
    for idx, tag in enumerate(taglist):
        # Pictures will be stored at images/{charname}
        # Only create new dir if dir doesn't exist already, helps when pulling fails
        if not os.path.isdir(f'images/{tag["name"]}'):
            try:
                os.mkdir(f'images/{tag["name"]}')
            except OSError:
                print(f'Creation of {tag["name"]} failed')
        print(f'Pulling images for {tag["name"]}, index = {idx_offset + idx}')
        pull_images_for_character(client, tag)

# A post is valid if it it's an image post, is a jpg, and only has one character (or is an exception)
def valid_post(post, name):
    file_chk = 'file_ext' in post and post['file_ext'] == 'jpg'
    char_chk = post['tag_count_character'] == 1 or (name in char_exceptions and post['tag_count_character'] == 2)
    return file_chk and char_chk

def pull_images_for_character(client, char_data):
    num_added = 0
    page_num = 1
    # Since we won't be adding all posts (not all posts are valid), we want at least 100 photos
    while num_added < 100:
        # Get 100 posts from each page, not all will be good, so check multiple pages
        postlist = client.post_list(limit=100, page=page_num, tags=char_data['name'])
        for post in postlist:
            if valid_post(post, char_data['name']):
                response = requests.get(post['file_url'])
                with open(f'images/{char_data["name"]}/{char_data["name"]}{num_added}.jpg', 'wb') as fp:
                    fp.write(response.content)
                    num_added += 1
        page_num += 1

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    parser = argparse.ArgumentParser(description='Tool to create 15,000 image dataset from Danbooru')
    parser.add_argument('-n', action='store', dest='offset', type=int)
    args = parser.parse_args(sys.argv[1:])

    offset = 0 if args.offset == None else args.offset

    client = Danbooru('danbooru', username=config.user, api_key=config.api_key)
    taglist = get_characters(client)
    pull_images(client, taglist[offset:], offset)