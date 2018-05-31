# Telegram/Discord Facial Recognition Bot [Python 3/Docker]

This script runs over docker

 1. Clone the repository
 2. Enter the directory
 3. Build the desired image, either `docker build . -f DockerfileTelegram -t witb-Telegram` or `docker build . -f DockerfileDiscord -t witb-Discord`
 4 `docker run -e "api-key=529959023:AAEPH-WXIvBwxbq3sXBTa58tAsA5ou3IEZE" -v "known-person:/root/bot/known-person/ "-t witb-Telegram`


# Required Docker ENV Vars

api-key = Either a telegram bot api token or a discord bot api token

# Sample Images

Add a sample photo of the people you want to be recognized to the known-person directory
The file name will be used as the person name
