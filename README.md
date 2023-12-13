# MIPT-code-rewiev

## Discription
Hi! this project was created for parsing the website of the [El Patio](https://ilpatio.ru/) restaurant 

tg bot: [Il Patio Bot](https://t.me/il_patio_bot)

## Configurations

Installing [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).

In file `docker-compose.yml` in service `bot`, specify the token for your telegram-bot: 
  ```
 environment:
      TOKEN: 'your-telegram-bot-token'
```

## Running project

Launch a project using the following commands:

```shell 
git clone git@github.com:Pe4eNPe4eNkI/MIPT-code-rewiev.git

cd MIPT-code-rewiev

bash ./build.sh
```

## Getting a token for a Telegram bot

1. Contact the bot [@BotFather](https://t.me/BotFather ).
2. Create a new bot.
3. For convenience, you can add to [@BotFather](https://t.me/BotFather ) the `settings` command. By typing `/settings` into the bot, you can access the bot settings.
