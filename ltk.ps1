Write-Host "
                                                                                                               
                                                             dddddddd                                          
                                         lllllll             d::::::d                   iiii                   
                                         l:::::l             d::::::d                  i::::i                  
                                         l:::::l             d::::::d                   iiii                   
                                         l:::::l             d:::::d                                           
vvvvvvv           vvvvvvvaaaaaaaaaaaaa    l::::l     ddddddddd:::::d    ooooooooooo   iiiiiiinnnn  nnnnnnnn    
 v:::::v         v:::::v a::::::::::::a   l::::l   dd::::::::::::::d  oo:::::::::::oo i:::::in:::nn::::::::nn  
  v:::::v       v:::::v  aaaaaaaaa:::::a  l::::l  d::::::::::::::::d o:::::::::::::::o i::::in::::::::::::::nn 
   v:::::v     v:::::v            a::::a  l::::l d:::::::ddddd:::::d o:::::ooooo:::::o i::::inn:::::::::::::::n
    v:::::v   v:::::v      aaaaaaa:::::a  l::::l d::::::d    d:::::d o::::o     o::::o i::::i  n:::::nnnn:::::n
     v:::::v v:::::v     aa::::::::::::a  l::::l d:::::d     d:::::d o::::o     o::::o i::::i  n::::n    n::::n
      v:::::v:::::v     a::::aaaa::::::a  l::::l d:::::d     d:::::d o::::o     o::::o i::::i  n::::n    n::::n
       v:::::::::v     a::::a    a:::::a  l::::l d:::::d     d:::::d o::::o     o::::o i::::i  n::::n    n::::n
        v:::::::v      a::::a    a:::::a l::::::ld::::::ddddd::::::ddo:::::ooooo:::::oi::::::i n::::n    n::::n
         v:::::v       a:::::aaaa::::::a l::::::l d:::::::::::::::::do:::::::::::::::oi::::::i n::::n    n::::n
          v:::v         a::::::::::aa:::al::::::l  d:::::::::ddd::::d oo:::::::::::oo i::::::i n::::n    n::::n
           vvv           aaaaaaaaaa  aaaallllllll   ddddddddd   ddddd   ooooooooooo   iiiiiiii nnnnnn    nnnnnn
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                               
" -ForegroundColor Cyan

Start-Sleep -Seconds 2.5

$leagueClientProcess = Get-Process -Name "LeagueClientUx" -ErrorAction SilentlyContinue

if (-not $leagueClientProcess) {
    Write-Host "You must start League Client first !" -ForegroundColor Red
    Start-Sleep -Seconds 2
    exit 1
}

$wmicOutput = wmic PROCESS WHERE name=`'LeagueClientUx.exe`' GET commandline
$port = ($wmicOutput  | Select-String -Pattern '--app-port=([0-9]*)').matches.groups[1].Value
$token = ($wmicOutput | Select-String -Pattern '--remoting-auth-token=([\w-]*)').matches.groups[1].Value
$summonerId = (curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-summoner/v1/current-summoner | ConvertFrom-json).summonerId
$puuid = (curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-summoner/v1/current-summoner | ConvertFrom-json).puuid

py requirements.py

function CalculateAccountWorth {
    $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
    $enterPressed = $false
    Write-Host "Downloading data..." -ForegroundColor Cyan
    curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-champions/v1/inventories/$summonerId/skins-minimal > ./data/owned-skins.json 
    Write-Host "Running script..." -ForegroundColor Cyan
    py ./scripts/owned-skins-script.py
    Write-Host "Press Enter to continue ..." -ForegroundColor Cyan
    $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").VirtualKeyCode
    if ($key -eq 13) { $enterPressed = $true }  
    if ($enterPressed) {
        ShowMenu
    }
}

function CurrentSeasonStats {
    $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
    $enterPressed = $false
    Write-Host "Downloading data..." -ForegroundColor Cyan
    curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-career-stats/v1/summoner-games/$puuid > ./data/games-stats-data.json
    Write-Host "Running script..." -ForegroundColor Cyan
    py ./scripts/season-stats-script.py
    Write-Host "Press Enter to continue ..." -ForegroundColor Cyan
    $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").VirtualKeyCode
    if ($key -eq 13) { $enterPressed = $true }  
    if ($enterPressed) {
        ShowMenu
    }
}

function CheckBlockedPlayers {
    $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
    $enterPressed = $false
    Write-Host "Downloading data..." -ForegroundColor Cyan
    curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-chat/v1/blocked-players > ./data/blocked-players.json 
    Write-Host "Running script..." -ForegroundColor Cyan
    py ./scripts/blocked-players-script.py
    Write-Host "Press Enter to continue ..." -ForegroundColor Cyan
    $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").VirtualKeyCode
    if ($key -eq 13) { $enterPressed = $true }  
    if ($enterPressed) {
        ShowMenu
    }
}
	
function FindTheirWeaknesses {
    $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
    $enterPressed = $false
    Write-Host "Downloading data..." -ForegroundColor Cyan
    curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-champ-select/v1/session > ./data/champ-select-data.json 
    Write-Host "Running script..." -ForegroundColor Cyan
    py ./scripts/champ-select-counters-script.py
    Write-Host "Press Enter to continue ..." -ForegroundColor Cyan
    $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").VirtualKeyCode
    if ($key -eq 13) { $enterPressed = $true }  
    if ($enterPressed) {
        ShowMenu
    }
}

function HomiesStats {
    $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
    $enterPressed = $false
    Write-Host "Downloading data..." -ForegroundColor Cyan
    curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-chat/v1/friends > ./data/chat-logs.json
    curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-chat/v1/friend-counts > ./data/friend-counts.json
    Write-Host "Running script..." -ForegroundColor Cyan
    py ./scripts/homies-stats-script.py
    Write-Host "Press Enter to continue ..." -ForegroundColor Cyan
    $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").VirtualKeyCode
    if ($key -eq 13) { $enterPressed = $true }  
    if ($enterPressed) {
        ShowMenu
    }
}

function ShowMenu {
    $options = @("Calculate your account worth", "Find Their Weaknesses (champ select counters)", "Current Season Stats", "Homies Stats (work in progress)", "Check blocked players", "Exit")
    $index = 0
    $enterPressed = $false
    while (-not $enterPressed) {
        Clear-Host
        Write-Host "Please select an option (use arrow keys and press Enter):"
        for ($i = 0; $i -lt $options.Length; $i++) {
            if ($i -eq $index) {
                Write-Host "> $($options[$i])" -ForegroundColor Cyan
            } else {
                Write-Host "  $($options[$i])"
            }
        }

        $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").VirtualKeyCode

        switch ($key) {
            38 { $index = if ($index -gt 0) { $index - 1 } else { $options.Length - 1 } }  # Up arrow
            40 { $index = if ($index -lt $options.Length - 1) { $index + 1 } else { 0 } }  # Down arrow
            13 { $enterPressed = $true }  # Enter
        }
    }

    switch ($index) {
        0 { CalculateAccountWorth }
		1 { FindTheirWeaknesses }
        2 { CurrentSeasonStats }
        3 { HomiesStats }
        4 { CheckBlockedPlayers }
        5 { Exit }
    }
}



ShowMenu
