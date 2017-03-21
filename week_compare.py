import smtplib
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup

import settings

cristina_id = 470
spike_id = 29


def get_weekly_total(log_id):
    ''' Return training time in minutes.'''
    base_url = 'https://www.attackpoint.org/log.jsp/user_'
    url = base_url + str(log_id)
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    row = soup.find('table').find('td', text="Total")
    total = row.find_next_sibling().find_next_sibling().text

    try:
        h, m, s = total.strip().split(':')
    except:
        # weaksauce
        m, s = total.strip().split(':')

    # ignore seconds, that's petty and Spike doesn't use them anyway
    total = int(h)*60 + int(m)
    return total


def send_email(msg):
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.send_message(msg)
    server.quit()


def generate_msg(diff, prev_diff):
    ''' Generate email message to send to annoy spike. '''
    if diff == 0:
        msg = MIMEText('The race is tight! You and Cristina have trained '
                       'the same number of minutes over the past week!')
        status = 'tied!'
    elif diff < prev_diff:
        msg = MIMEText('Oh no! Better get training! '
                       'Cristina currently has {} more '
                       'minutes than you over the past week!'.format(-diff))
        status = '{} minutes behind'.format(-diff)
    elif diff > prev_diff:
        msg = MIMEText('You seem motivated this week, with {} more '
                       'minutes of training than Cristina.'.format(diff))
        status = '{} minutes ahead'.format(diff)

    msg['Subject'] = 'Spikevs status change: ' + status
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = settings.EMAIL_RECIPIENT

    return msg


def main():
    cristina_total = get_weekly_total(cristina_id)
    spike_total = get_weekly_total(spike_id)
    diff = spike_total - cristina_total

    try:
        with open('diff.txt', 'r') as f:
            prev_diff = int(f.read())
    except:
        prev_diff = 0

    if prev_diff != diff:
        with open('diff.txt', 'w') as f:
            f.write(str(diff))

    # Check for sign change
    if diff * prev_diff > 0:
        return

    # There's a change! Send an obnoxious email!
    msg = generate_msg(diff, prev_diff)
    send_email(msg)

if __name__ == '__main__':
    main()
