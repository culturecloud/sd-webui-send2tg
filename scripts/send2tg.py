import modules.scripts as scripts
import gradio as gr
import requests
import os

from modules import images, shared, script_callbacks
from modules.processing import process_images

class Script(scripts.Script):

    def title(self):
        return "Send to Telegram"

    def show(self, _):
        return scripts.AlwaysVisible
    
    def ui(self, _):
        enable = gr.Checkbox(
            False,
            label="Send images to Telegram"
        )
        return [enable]
    
    def run(self, p, enable):
        proc = process_images(p)
        
        method = "sendDocument" if shared.opts.send2tg_as_document else "sendPhoto"
        send_document = f"https://api.telegram.org/bot{shared.opts.send2tg_bot_token}/{method}"
        
        if enable and shared.opts.send2tg_bot_token and shared.opts.send2tg_channel_id:
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
                    "chat_id": shared.opts.send2tg_channel_id,
                    "parse_mode": "MARKDOWN",
                    "caption": f"`{proc.prompt}`"
                }
            
                files = {
                    f"{'document' if method == 'sendDocument' else 'photo'}": open(image, "rb")
                }
            
                requests.post(
                    send_document,
                    data=data,
                    files=files,
                    stream=True
                )
            
        return proc


def on_ui_settings():
    section = ('send2tg', "Send to Telegram")
    
    shared.opts.add_option(
        "send2tg_bot_token",
        shared.OptionInfo(
            default=None,
            label="Telegram Bot Token",
            component=gr.Textbox,
            component_args={
                "placeholder": "Enter your Telegram Bot ID here."
            },
            section=section,
            comment_after="This bot should have message permission to the channel you specify below."
        )
    )
    shared.opts.add_option(
        "send2tg_channel_id",
        shared.OptionInfo(
            default=-100,
            label="Telegram Channel ID",
            component=gr.Number,
            section=section,
            comment_after="This the channel where the bot will send images."
        )
    )
    shared.opts.add_option(
        "send2tg_as_document",
        shared.OptionInfo(
            default=True,
            label="Send as Document",
            component=gr.Checkbox,
            section=section
        )
    )
        
script_callbacks.on_ui_settings(on_ui_settings)
