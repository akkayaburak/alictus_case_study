from slack import WebClient


def send_to_slack(text):
    '''Sends the text to automation channel in Slack.'''
    try:
        sc = WebClient(
            '')
        sc.chat_postMessage(channel="#automation", text=text)
    except Exception as err:
        print(f'Error occurred: {err}')
