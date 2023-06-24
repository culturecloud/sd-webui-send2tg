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
            label="Enable"
        )
        return [enable]
    
    def run(self, p, enable):
        proc = process_images(p)
        send_document = f"https://api.telegram.org/bot{shared.opts.send2tg.tg_token}/sendDocument"
        
        if enable:
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
                    "chat_id": shared.opts.send2tg.channel_id,
                    "parse_mode": "MARKDOWN",
                    "caption": f"`{proc.prompt}`"
                }
            
                files = {
                    "document": open(image, "rb")
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
        "bot_token",
        shared.OptionInfo(
            "5824420342:AAHYD_E_o0DGIlybbTHywCgdyvQbRWSVdfE"
            "Telegram Bot Token. This bot should have message permission on your channel.This bot should have message permission on your channel.",
            gr.Textbox,
            section=section
        )
    )
    shared.opts.add_option(
        "channel_id",
        shared.OptionInfo(
            "-1001974141145",
            "Channel ID of your Telegram channel where the bot would send the images.",
            gr.Number,
            section=section
        )
    )
        
script_callbacks.on_ui_settings(on_ui_settings)
