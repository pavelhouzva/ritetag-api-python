import argparse
import os
from .api import *

current_directory = os.getcwd()
access_token = os.getenv('ACCESS_TOKEN', None)
require_token = access_token is None


class Action(Enum):
    hashtag_stats = 'hashtag_stats'
    auto_hashtags = 'auto_hashtags'
    hashtag_suggestions_for_text = 'hashtag_suggestions_for_text'
    hashtag_suggestions_for_image = 'hashtag_suggestions_for_image'
    hashtag_history = 'hashtag_history'
    emojis_suggestion = 'emojis_suggestion'
    auto_emojify = 'auto_emojify'
    text_to_image = 'text_to_image'
    animate_image = 'animate_image'
    company_logo = 'company_logo'
    list_of_cta = 'list_of_cta'
    shorten_link = 'shorten_link'

    def __str__(self):
        return '{0}'.format(self.value)


actions = [str(x) for x in [
    Action.hashtag_stats,
    Action.auto_hashtags,
    Action.hashtag_suggestions_for_text,
    Action.hashtag_suggestions_for_image,
    Action.hashtag_history,
    Action.emojis_suggestion,
    Action.auto_emojify,
    # Action.text_to_image, not supported yet
    # Action.animate_image, not supported yet
    Action.company_logo,
    Action.list_of_cta,
    Action.shorten_link
]]


def get_hashtags(parser, args):
    if args.hashtags is None or len(args.hashtags) == 0:
        parser.error('missing hashtags')
    return args.hashtags


def get_hashtag(parser, args):
    if args.hashtags is None or len(args.hashtags) == 0:
        parser.error('missing hashtag')
    elif len(args.hashtags) > 1:
        parser.error('too many hashtags')
    return args.hashtags[0]


def get_domain(parser, args):
    if args.hashtags is None or len(args.hashtags) == 0:
        parser.error('missing domain')
    elif len(args.hashtags) > 1:
        parser.error('invalid domain')
    return args.hashtags[0]


def get_url(parser, args):
    if args.hashtags is None or len(args.hashtags) == 0:
        parser.error('missing url')
    elif len(args.hashtags) > 1:
        parser.error('invalid url')
    return args.hashtags[0]


def get_post(parser, args):
    if args.hashtags is None or len(args.hashtags) == 0:
        parser.error('missing post')
    return ' '.join(args.hashtags)


def run():
    parser = argparse.ArgumentParser(description='RiteTag API console client.')
    parser.add_argument('-t', '--access_token', type=str, help='access token', required=require_token)
    parser.add_argument('action', choices=actions, help='action')
    parser.add_argument('hashtags', type=str, nargs='*', help='hashtags')
    parser.add_argument('-m', '--max_hashtags', type=int, default=2)
    parser.add_argument('-p', '--hashtag_position', type=str, choices=['auto', 'end'], default='auto')
    parser.add_argument('-f', '--filename', type=str)
    parser.add_argument('-ci', '--cta_id', type=int)
    args = parser.parse_args()

    api = RiteTagApi(args.access_token if require_token else access_token)

    def log(limit):
        print(limit)

    api.on_limit(0, log)

    a = Action[args.action]

    # print(args)
    try:
        if a == Action.hashtag_stats:
            hashtags = get_hashtags(parser, args)
            print('\n'.join([str(x) for x in api.hashtag_stats(hashtags)]))

        elif a == Action.auto_hashtags:
            post = get_post(parser, args)
            log(api.auto_hashtag(post, args.max_hashtags))

        elif a == Action.hashtag_suggestions_for_text:
            post = get_post(parser, args)
            [log(x) for x in api.hashtag_suggestion_for_text(post)]

        elif a == Action.hashtag_suggestions_for_image:
            post = get_url(parser, args)
            [log(x) for x in api.hashtag_suggestion_for_image(post)]

        elif a == Action.hashtag_history:
            hashtag = get_hashtag(parser, args)
            [log(x) for x in api.history(hashtag)]

        elif a == Action.emojis_suggestion:
            text = get_post(parser, args)
            log(', '.join(api.emoji_suggestion(text)))

        elif a == Action.auto_emojify:
            text = get_post(parser, args)
            log(api.auto_emojify(text))

        elif a == Action.text_to_image:
            parser.error("not implemented yet")

        elif a == Action.animate_image:
            parser.error('not implemented yet')

        elif a == Action.company_logo:
            domain = get_domain(parser, args)
            img = api.company_logo(domain)
            filename = domain.replace('.', '_') if args.filename is None else args.filename
            path = img.save(current_directory, filename)
            log('Image saved. Location: {}'.format(path))

        elif a == Action.list_of_cta:
            [log(x) for x in api.list_of_cta()]

        elif a == Action.shorten_link:
            url = get_domain(parser, args)
            cta_id = args.cta_id
            log(api.shorten_url(url, cta_id).url)
    except RiteTagException as e:
        parser.error(e)
        # raise e
