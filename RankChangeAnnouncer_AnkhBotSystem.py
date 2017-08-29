#---------------------------------------
#	Import Libraries
#---------------------------------------
import os
import codecs
import json
import time

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "Rank Change Announcer"
Website = "https://www.github.com/hyperneon"
Creator = "GameTangent"
Version = "1.0.0"
Description = "Announce in chat when a user changes ranks"

#---------------------------------------
#	Set Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "RCASettings.json")

#---------------------------------------
# Classes
#---------------------------------------
class Settings(object):
    """ Load in saved settings file if available else set default values. """
    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
                self.rank_up_message = "KAPOW Congrats to {0} for LEVELING UP to {1} KAPOW"
                self.rank_down_message = "FailFish {0} is slacking and leveled down to {1} FailFish"
                self.announcer_timer = 30
                self.rank_system = "Points"
                self.announce_rank_ups = true
                self.announce_rank_downs = false
                self.announce_lurkers = false

    def reload(self, jsondata):
        """ Reload settings from AnkhBot user interface by given json data. """
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def save(self, settingsfile):
        """ Save settings contained within to .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return

#---------------------------------------
#	Functions
#---------------------------------------
def GetRankList():
    """
        GetRankList is a function that retrieves the full list of viewers and then looks up their
        ranks and points. It returns a dictionary with the following structure:
        {user_name: {'rank': rank, 'points': points}}
        If ScriptSettings.announce_lurkers is false it will only return active users
    """
    # If announce_lurkers is true then get the full Viewer list
    if ScriptSettings.announce_lurkers:
        viewers = Parent.GetViewerList()
    else:
        viewers = Parent.GetActiveUsers()
        
    ranks = Parent.GetRanksAll(viewers)
    points = Parent.GetPointsAll(viewers)
    
    rank_list = {}   
    for name,rank in ranks.items():
        rank_list[name] = {'rank': rank, 'points': points[name]}
    
    return rank_list
    
def CalculateRankChanges(new_ranks, old_ranks):
    """
        CalculateRankChanges is a function which compares 2 dictionaries of ranks and finds
        those items which are present in both sets AND whose ranks have changed. It then
        compares the point values in each set to determine if the rank has gone up or down.
        It returns a dictionary with the following structure:
        {user_name: {'rank': new_rank, 'level_up': True/False}}
    """
    # Get only names in both sets as new names may have just joined chat and not actually changed rank
    intersect = set(new_ranks) & set(old_ranks)
    rank_changes = {}
    for name in intersect:
        new_rank = new_ranks[name]
        old_rank = old_ranks[name]
        # Add rank to list if new rank title is different from old title
        if new_rank['rank'] != old_rank['rank']:
            # Leveling up if new points are higher than old points
            # If we're using an Hours based system then we'll always level up
            if ScriptSettings.rank_system == "Hours" or new_rank['points'] >= old_rank['points']:
                rank_changes[name] = {'rank': new_rank['rank'], 'level_up': True}
            else:
                rank_changes[name] = {'rank': new_rank['rank'], 'level_up': False}
            
    return rank_changes

#---------------------------------------
#	[Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    """
        Init is a required function and is called the script is being loaded into memory
        and becomes	active. In here you can initialize any data your script will require,
        for example read the settings file for saved settings.
    """

    # Globals
    global ScriptSettings
    global LastRunTime
    global LastRankList

    # Load in saved settings
    ScriptSettings = Settings(SettingsFile)
    # Set LastRunTime to now
    LastRunTime = time.time()
    # Initialize With The Current Rank List
    LastRankList = GetRankList()

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsondata):

    """
        ReloadSettings is an optional function that gets called once the user clicks on
        the Save Settings button of the corresponding script in the scripts tab if an
        user interface has been created for said script. The entire Json object will be
        passed to the function	so you can load that back	into your settings without
        having to read the newly saved settings file.
    """

    # Globals
    global ScriptSettings

    # Reload newly saved settings
    ScriptSettings.reload(jsondata)

    # End of ReloadSettings
    return

#---------------------------------------
#	[Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    """
        Execute is a required function that gets called when there is new data to be
        processed. Like a Twitch or Discord chat messages or even raw data send from
        Twitch IRC.	This function will _not_ be called when the user disabled the script
        with the switch on the user interface.
    """
    return
       

#---------------------------------------
#	[Required] Tick Function
#---------------------------------------
def Tick():
    """
        Tick is a required function and will be called every time the program progresses.
        This can be used for example to create simple timer if you want to do let the
        script do something on a timed basis.This function will _not_ be called	when the
        user disabled the script	with the switch on the user interface.
    """
    # Only run check if it's been more than the announcer_timer limit since the LastRunTime
    if time.time() - LastRunTime >= ScriptSettings.announcer_timer:
        # Globals
        global LastRunTime
        global LastRankList
                
        new_ranks = GetRankList()
        rank_changes = CalculateRankChanges(new_ranks, LastRankList)
        
        # Iterate over each rank_change and send chat messages if enabled
        for name, rank_details in rank_changes.items():
            if rank_details['level_up']:
                if ScriptSettings.announce_rank_ups:
                    Parent.SendTwitchMessage(ScriptSettings.rank_up_message.format(name, rank_details['rank']))
            else:
                if ScriptSettings.announce_rank_downs:
                    Parent.SendTwitchMessage(ScriptSettings.rank_down_message.format(name, rank_details['rank']))

        # Save new rank list to LastRankList for next time
        LastRankList = new_ranks
        # Set new timestamp
        LastRunTime = time.time()
    return