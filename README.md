# Streamlabs Chatbot Rank Change Announcer
A Python script for use in [Streamlabs Chatbots's](https://streamlabs.com/chatbot) built-in scripting feature which announces in chat when a user changes ranks.
You can check out the functionality on [Github](https://github.com/HyperNeon/ankhbot-rank-change-announcer)

This script will monitor all Twitch/YouTube/Mixer users currently connected to chat and make an announcement in chat whenever a user ranks up or ranks down. The script allows you to customize:
* The message sent when a user ranks up
* The message sent when a user ranks down
* How often the script should run
* Whether to enable the rank up messages
* Whether to enable the rank down messages
* Whether to send alerts for lurkers or only active chatters

Streamers using Streamlabs Chatbot Rank Change Announcer:
* http://twitch.tv/gametangent

### Installation
This script is meant to be run from within the Scripts module in [Streamlabs Chatbots's](https://streamlabs.com/chatbot).
Instructions for installing a new script in the bot can be found here: [Offical Chatbot Documention](https://cdn.streamlabs.com/chatbot/Documentation.pdf).
Everything else you need for configuring the bot can be found within the tooltips that appear when hovering over each configuration parameter in the UI.

### Contributing
I'd love it if you'd like to help out making this thing better. Simply fork the repo and submit a PR and I'll be glad to take a look at it. Also feel free to reach out to me with any questions and check out the [Chatbot Discord](https://discordapp.com/invite/J4QMG5m). I go by GameTangent in the Discord.

**Note:** This bot deprecates my previous standalone version built in Ruby: [Ankhbot Ruby Bot](https://github.com/HyperNeon/Ankhbot-Ruby-Bot)
