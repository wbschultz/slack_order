# original author: Collin Bardini - https://github.com/cbardini
# created for Chompshop's daily standups
import os
import random
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
order_channel = "C07RDCYHZ5F"


# Listens to incoming messages that contain "order"
# To learn available listener arguments,
# visit https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html%
@app.command("/order")
def order_command(ack, say, command):
    ack()

    # get members of this channel
    response = app.client.conversations_members(channel=order_channel)
    members = response.data["members"]

    names = []
    # get names of members
    for member in members:
        response = app.client.users_info(user=member)
        name = response.data["user"]["profile"]["display_name"]
        if name == "":
            name = response.data["user"]["profile"]["real_name"]
        if name != "OrderKeeper":
            names.append(name)

    # randomize the list
    random.shuffle(names)
    name_list_string = ""
    for i in range(len(names)):
        name_list_string += f"\n {i+1}.  {names[i]}"

    # dictate!
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"I dictate that the order of the day is:{name_list_string}",
                },
            }
        ]
    )


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
