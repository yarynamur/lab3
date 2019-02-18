import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl


def get_acct():
    while True:
        print('')
        acct = input('Enter Twitter Account:')
        if (len(acct) > 1):
            break
    return acct


def get_key():
    """
    Defines which info user wants to get from json
    """
    print("Choose information you'd like to get: followers count(enter '1'), status(enter '2'), geo(enter '3') or id (enter '4')")
    num = input()
    if num == '1':
        return 'followers_count'
    if num == '2':
        return 'status'
    if num == '3':
        return 'geo'
    if num == '4':
        return 'id'


def get_json(acct):
    """
    Makes json about given account
    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    headers = dict(connection.getheaders())
    return js


def get_info(js, key):
    """
    Gets info from json
    """
    for u in js['users']:
        print(u['screen_name'])
        if key not in u:
            print('   * No {} found'.format(key))
        else:
            if type(u[key]) != str:
                print(u[key])
            else:
                s = u[key]['text']
                print('  ', s[:50])


if __name__ == "__main__":
    acct = get_acct()
    key = get_key()
    js = get_json(acct)
    get_info(js, key)
    with open('data.json', 'w') as outfile:
        json.dump(js, outfile)
