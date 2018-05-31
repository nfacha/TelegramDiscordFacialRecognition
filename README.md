# Telegram/Discord Facial Recognition Bot [Python 3/Docker]

This script runs over docker

 1. Clone the repository
 2. Enter the directory
 3. Build the desired image, either `docker build . -f DockerfileTelegram -t witb-telegram` or `docker build . -f DockerfileDiscord -t witb-discord`
 4 `docker run -e apikey="YOUR API KEY HERE" -v "known-person:/root/bot/known-person/" -t witb-telegram`


# Required Docker ENV Vars

apikey = Either a telegram bot api token or a discord bot api token

# Sample Images

Add a sample photo of the people you want to be recognized to the known-person directory
The file name will be used as the person name
