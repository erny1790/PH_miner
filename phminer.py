import os

import yaml
from ph_py import ProductHuntClient
from ph_py.error import ProductHuntError
import csv

config_file = 'credentials.yml'

def run(key, secret, uri, token):
    phc = ProductHuntClient(key, secret, uri, token)

    # Example request
    try:
        with open('popular_2018-04-20.csv', 'w', newline='', encoding='UTF8') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
            spamwriter.writerow(['Name', 'TagLine', 'Logo', 'URL', 'NumberOfUpvotes', 'NumberOfComments', 'HunterName'])

            for post in phc.get_todays_posts():
                print('Name: ', post.name)
                print('Tagline: ', post.tagline)

                logo=post.screenshot_url['850px']
                print('Logo: ', logo)
                print('URL: ', post.redirect_url)
                print('number of upvotes: ', post.votes_count)
                print('number of comments: ', post.comments_count)
                print('Hunter name: ', post.user.name)


                spamwriter.writerow([post.name, post.tagline, logo, post.redirect_url, post.votes_count, post.comments_count, post.user.name])

                print('-------------------------------------------')
                print('-------------------------------------------')





    except ProductHuntError as e:
        print(e.error_message)
        print(e.status_code)


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), config_file), 'r') as config:
        cfg = yaml.load(config)
        client_key = cfg['api']['key']
        client_secret = cfg['api']['secret']
        redirect_uri = cfg['api']['redirect_uri']
        dev_token = cfg['api']['dev_token']

    run(client_key, client_secret, redirect_uri, dev_token)
