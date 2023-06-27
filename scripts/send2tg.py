import gradio as gr
import requests

from modules import script_callbacks
from modules.shared import opts, OptionInfo


def on_image_saved(params):
    method = "sendDocument" if opts.send2tg_as_document else "sendPhoto"
    tg_api = f"https://api.telegram.org/bot{opts.send2tg_bot_token}/{method}"
    
    if (opts.send2tg_enabled and opts.send2tg_bot_token and opts.send2tg_channel_id):
        data = {
            "chat_id": opts.send2tg_channel_id,
            "parse_mode": "MARKDOWN",
            "caption": f"`{params.p.prompt}`"
        }
                    
        files = {
            f"{'document' if method == 'sendDocument' else 'photo'}": open(params.filename, "rb")
        }
                    
        requests.post(
            tg_api,
            data=data,
            files=files,
            stream=True
        )
            
    
def on_ui_settings():
    section = ('send2tg', "Send to Telegram")
    
    opts.add_option(
        "send2tg_enabled",
        OptionInfo(
            default=False,
            label="Enable Send to Telegram",
            component=gr.Checkbox,
            section=section
        )
    )
    opts.add_option(
        "send2tg_bot_token",
        OptionInfo(
            default="",
            label="Bot Token",
            component=gr.Textbox,
            component_args={
                "placeholder": "123456789:xxxxxxxxxxxxxxxxxxxxxxxxx"
            },
            section=section,
            comment_after="<i>(This bot should have message permission to the channel you specify below.)</i>"
        )
    )
    opts.add_option(
        "send2tg_channel_id",
        OptionInfo(
            default="",
            label="Channel ID",
            component=gr.Textbox,
            component_args={
                "placeholder": "-1001234567890"
            },
            section=section,
            comment_after="<i>(This is the channel where the bot will send images.)</i>"
        )
    )
    opts.add_option(
        "send2tg_as_document",
        OptionInfo(
            default=True,
            label="Send as Document",
            component=gr.Checkbox,
            section=section,
            comment_after="(Image will be sent as document without compression.)"
        )
    )


script_callbacks.on_image_saved(on_image_saved)
script_callbacks.on_ui_settings(on_ui_settings)
