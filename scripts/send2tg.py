import modules.scripts as scripts
import gradio as gr
import requests
import os

from modules import images, script_callbacks
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state, OptionInfo

class Script(scripts.Script):

    def title(self):
        return "Send to Telegram"

    def show(self, _):
        return scripts.AlwaysVisible
    
    def ui(self, _):
        enabled = gr.Checkbox(
            False,
            label="Send images to Telegram"
        )
        
        return [enabled]
    
    def run(self, p, enabled):
        proc = process_images(p)
        
        method = "sendDocument" if opts.send2tg_as_document else "sendPhoto"
        tg_api = f"https://api.telegram.org/bot{opts.send2tg_bot_token}/{method}"
        
        if (enabled and opts.send2tg_bot_token and opts.send2tg_channel_id):
            for i in range(len(proc.images)):
                image, txt = images.save_image(
                    image=proc.images[i],
                    path=p.outpath_samples,
                    basename="",
                    seed=proc.seed,
                    prompt=proc.prompt,
                    extension=opts.samples_format,
                    info=proc.info,
                    p=p
                )
            
                data = {
                    "chat_id": opts.send2tg_channel_id,
                    "parse_mode": "MARKDOWN",
                    "caption": f"`{proc.prompt}`"
                }
            
                files = {
                    f"{'document' if method == 'sendDocument' else 'photo'}": open(image, "rb")
                }
            
                requests.post(
                    tg_api,
                    data=data,
                    files=files,
                    stream=True
                )
            
        return proc


def on_ui_settings():
    section = ('send2tg', "Send to Telegram")
    
    opts.add_option(
        "send2tg_bot_token",
        OptionInfo(
            default="",
            label="Telegram Bot Token",
            component=gr.Textbox,
            component_args={
                "placeholder": "123456789:xxxxxxxxxxxxxxxxxxxxxxxxx"
            },
            section=section,
            comment_after="(This bot should have message permission to the channel you specify below.)"
        )
    )
    opts.add_option(
        "send2tg_channel_id",
        OptionInfo(
            default="",
            label="Telegram Channel ID",
            component=gr.Textbox,
            component_args={
                "placeholder": "-1001234567890"
            },
            section=section,
            comment_after="(This is the channel where the bot will send images.)"
        )
    )
    opts.add_option(
        "send2tg_as_document",
        OptionInfo(
            default=True,
            label="Send as Document",
            component=gr.Checkbox,
            section=section
        )
    )
        
script_callbacks.on_ui_settings(on_ui_settings)
