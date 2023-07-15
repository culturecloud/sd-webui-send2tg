# Stable Diffusion WebUI Extension - Send to Telegram
## `You can use this extension to send your generated Stable Diffusion images straight to your configured Telegram channel/group.`
## Notes
- Set your credentials using command line parameters `--send2tg-bot-token` and `--send2tg-channel-id` or in **Web UI settings > Send to Telegram.**
- Command line parameters will take priority over WebUI settings.
- The script will be enabled as long as both bot token and channel ID parameters are present (in command line).
- The bot must have messaging permission to send images to the designated channel/group.
- Use `--send2tg-as-photo` if you want the images to be sent as photo instead of document. Note that in this mode, **they'll be automatically compressed by Telegram and lose all generation info.**
- You can also set the bot to send the images to yourself instead of a channel or group. In this case, all you need is to set your Telegram user ID as the value of channel ID.
