# LTK (LoLToolkit)
This script utilizes [Riot LCU API](https://lcu.vivide.re/) to fetch your account and session information, along with a combination of [CommunityDragon](https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/) (up to date until 06/17/2024) and [U.GG](https://u.gg/) datas.

I did this out of curiosity to explore the LoL LCU API and to improve my Python scripting skills. I implemented features that I couldn't find on existing websites/applications related to LoL.

Here are a few of them : 

- Calculate the RP/$ value of your account
- Automatically find counters for ennemy comp
- Retrieve your current season statistics across all game modes
- Identify your best friends (needs some tweaking)
- Check your list of blocked players

## How to use
- Make sure Windows PowerShell is allowed to run unsigned scripts :

  - Start Windows PowerShell as admin
  
  - Use below command :
  
        set-executionpolicy remotesigned

    
- Open a Terminal at the project's root directory then execute the PowerShell script by typing ```.\ltk.ps1``` (League client has to be launched).

*N.B : You must have Python installed before running the script or your computer might explode ⚠️*

🚧🚧🚧W.I.P.🚧🚧🚧
