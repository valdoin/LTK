echo "
                                                                                                               
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
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                               
"


$wmicOutput = wmic PROCESS WHERE name=`'LeagueClientUx.exe`' GET commandline
$port = ($wmicOutput  | Select-String -Pattern '--app-port=([0-9]*)').matches.groups[1].Value
$token = ($wmicOutput | Select-String -Pattern '--remoting-auth-token=([\w-]*)').matches.groups[1].Value

$summonerId = (curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-summoner/v1/current-summoner | ConvertFrom-json).summonerId

$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-champions/v1/inventories/$summonerId/skins-minimal > ./data/owned-skins.json

py script.py