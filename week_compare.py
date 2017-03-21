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


def generate_msg(cristina_total, spike_total):
    diff = spike_total - cristina_total

    if diff < 0:
        msg = MIMEText('Oh no! Better get training! '
                       'Cristina currently has {} more '
                       'minutes than you over the past week!'.format(-diff))
    elif diff > 0:
        msg = MIMEText('You seem motivated this week, with {} more '
                       'minutes of training than Cristina.'.format(diff))
    else:
        msg = MIMEText('The race is tight! You and Cristina have trained '
                       'the same number of minutes over the past week!')

    msg['Subject'] = 'Spikevs status: {} minutes'.format(diff)
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = settings.EMAIL_RECIPIENT

    return msg


def main():
    cristina_total = get_weekly_total(cristina_id)
    spike_total = get_weekly_total(spike_id)

    msg = generate_msg(cristina_total, spike_total)
    send_email(msg)

if __name__ == '__main__':
    main()
