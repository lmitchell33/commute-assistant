# Commute Assistant

After random spots of construction started popping up around me, causing my commute time to work vary pretty much day by day (screwing up my sleep schedule by having to wake up early some days and later others), I decided to take matters into my own hands and create this simple messaging service which will send a text message at 5AM everyday Monday-Friday with mt estimated travel time and the optimal route to take. That way, when I wake up and see the message, I can choose to go back to sleep or get up and leave for work. 

<br />

This solution is designed to be **completely free**. All you need to do is have a `Unix-based machine` capable of running `cron`, `python`, and setup a `Google App Password` and `Google API Key`. The implementation was designed in a way such that changes or enhancements, such as other types of messages or features, can be implemented very easily (hopefully). 


## Perquisites

- Python 3.7 or greater
- pip3
- Unix-based machine capable of running cron (recommended)

## Requirements

- Gmail account & email
- Google API key
- Google App Password (with permission for the Google Routes API)

See the [Google Routes API Documentation](https://developers.google.com/maps/documentation/routes) and the [Google App Password Documentation](https://support.google.com/accounts/answer/185833?hl=en) for more information.

## Setup

1. **Clone the repository**

```
$ git clone https://github.com/lmitchell33/commute-assistant.git && cd commute-assistant
```

2. **Install dependencies**

```
$ pip install -r requirements.txt
```

3. **Create a .env file**

Create a `.env` in the `/commute-assistant` directory with the following contents:

- `GMAIL_ADDRESS=`
- `GOOGLE_APP_PASSWORD=`
- `PHONE_NUMBER=`
- `GOOGLE_API_KEY=`
- `HOME_ADDRESS=`
- `WORK_ADDRESS=`

Note that the only two variables that are required are `GOOGLE_API_KEY` and `GOOGLE_APP_PASSWORD`. All other variables can be passed in as command line arguments and are completely optional. Another work around to this is to simply manually set the value of `GOOGLE_API_KEY` and `GOOGLE_APP_PASSWORD` in `config.py`

4. **Setup the cronjob**

Note, you may want to change the cron job declared in setup.sh with flags from the command line, if you wish. 

```
$ chmod +x setup.sh
$ ./setup.sh
```

## Side Notes

- Although this was created and intended to be used without a Unix/Linux based machine running cron (a person server perhaps?) you can still use it on Windows using the task scheduler application. 

- The Google Routes API has a usage cap on how many calls it can make **per month** my personal use case for this (once a day) will not even come close to touching this 

- The smtp lib package and communication protocol was used solely because it was 100% free. SMS APIs (such as Twilio) could have been used, however, they cost money (very very minimally, but still money)

-  In order to use the smtp server you need to send the text message from an email address to a phone number at a designated provided. My phone carrier is Verizon, therefore, the recipient email address for my service will be `(my phone number)@vtext.com` or `@vzwpix.com` for longer messages. 
