import requests, json, csv, random
from bs4 import BeautifulSoup
import os
os.chdir(r'C:\projects\shl_scraper')

user_agent_list = [
   # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def get_smjhl_players(url_file, smjhl_players_csv):
    """use the urls provided in the json to get each player's information"""
    team_url_list = get_roster_url(url_file, 'SMJHL')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in team_url_list:  # For each team in the list
        player_url_list = get_player_urls(team[1])  # get each player page URL
        for player in player_url_list:  # for each player in player_url_list
            player_dict_list.append(get_player_stats('https://www.simulationhockey.com/' + player, team[0],'Prospect'))
    # look into using csv dictwriter.writerows() to write the list of dictionaries into the csv file
    csv_file = smjhl_players_csv
    csv_columns = player_dict_list[0].keys()
    with open(csv_file, 'w+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in player_dict_list:
            writer.writerow(data)


def get_shl_players(url_file, shl_players_csv):
    """use the urls provided in the json to get each player's information"""
    team_url_list = get_roster_url(url_file, 'SHL')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in team_url_list:  # For each team in the list
        player_url_list = get_player_urls(team[1])  # get each player page URL
        for player in player_url_list:  # for each player in player_url_list
            player_dict_list.append(get_player_stats('https://www.simulationhockey.com/' + player, team[0],'SHL'))
    # look into using csv dictwriter.writerows() to write the list of dictionaries into the csv file
    csv_file = shl_players_csv
    csv_columns = player_dict_list[0].keys()
    with open(csv_file, 'w+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in player_dict_list:
            writer.writerow(data)

def get_shl_prospects(url_file, shl_prospects_csv):
    """use the urls provided in the json to get each player's information"""
    prospect_url_list = get_roster_url(url_file, 'Prospects')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in prospect_url_list:  # For each team in the list
        player_url_list = get_player_urls(team[1])  # get each player page URL
        for player in player_url_list:  # for each player in player_url_list
            player_dict_list.append(get_player_stats('https://www.simulationhockey.com/' + player, team[0],'Prospect'))
    # look into using csv dictwriter.writerows() to write the list of dictionaries into the csv file
    csv_file = shl_prospects_csv
    csv_columns = player_dict_list[0].keys()
    with open(csv_file, 'w+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in player_dict_list:
            writer.writerow(data)

def get_roster_url(url_file, league):
    """Get the roster URLs for the specified league"""
    return_list = []
    with open(url_file, 'r') as rf:
        data = json.load(rf)
        for team in data['Team Roster URLs'][league]:  # go through the json and get the urls for each roster
            return_list.append((team, data['Team Roster URLs'][league][team]))  # add tuple of team name and url to list
    return return_list


def get_player_urls(team_roster_url):
    """Returns a list of player page URLs from the team roster page"""
    has_next = True
    page = 1
    return_list = list()
    while has_next:  # this loop ensures that all pages of the roster are hit
        user_agent = random.choice(user_agent_list)
        print(user_agent)
        headers = {'User-Agent': user_agent}
        roster_page = requests.get(team_roster_url + '&page=' + str(page), headers=headers)
        soup = BeautifulSoup(roster_page.content, 'html.parser')
        smaller_soup = soup.find_all('tr', 'inline_row')
        for section in smaller_soup:
            a = section.find('a', attrs={'style':'font-size:14px;'}, href=True)
            return_list.append(a['href'])
        has_next = len(soup.find_all('a', 'pagination_next')) != 0  # check if there is a next page
        if has_next:
            page += 1
    return return_list


def get_player_stats(name_url, team, player_type):
    """Use the given url to find and get all of the stats. Returns a dictionary"""
    player = dict.fromkeys(['Team', 'Player Type', 'Player URL', 'Draft Class', 'Draft Class Numeric', 'First Name', 'Last Name', 'Position', 'Shoots', 'Recruited by',
                            'Player Render', 'Jersey Number', 'Height', 'Weight', 'Birthplace', 'Player Role',
                            'Strengths', 'Weakness', 'Points Available', 
                            'Screening', 'Getting Open', 'Passing', 'Puckhandling', 'Shooting Accuracy', 'Shooting Range', 'Offensive Read',
                            'Checking','Hitting','Stickchecking','Shot Blocking','Faceoffs','Defensive Read',
                            'Acceleration','Agility','Balance','Speed','Stamina','Strength','Fighting',
                            'Aggression','Bravery','Determination','Team Player','Leadership','Temperament','Professionalism',
                            'Blocker','Glove','Passing','Poke Check','Positioning','Rebound','Recovery','Puckhandling','Low Shots','Reflexes','Skating',
                            'Mental Toughness','Goalie Stamina',
                            'Listed TPE','Applied TPE','Total TPE'
                           ])
    player['Player URL'] = name_url
    player['Team'] = team
    player['Player Type'] = player_type
    user_agent = random.choice(user_agent_list)
    #print(user_agent)
    headers = {'User-Agent': user_agent}
    player_page = requests.get(name_url, headers=headers)
    soup = BeautifulSoup(player_page.content, 'html.parser')

    # Get the Position, TPE, and Draft Class
    print(soup.find_all('td', 'thead')[1].strong.text)
    position_and_class = soup.find_all('td', 'thead')[1].strong.text
    tpe = str()
    draft_class = str()
    position = str()
    if position_and_class.__contains__(' C ') or position_and_class.lower().__contains__('center') or position_and_class.__contains__(' C-') or position_and_class.lower().__contains__('centre'): 
        position = 'C'
    if position_and_class.__contains__(' LW ') or position_and_class.lower().__contains__('left wing') or position_and_class.__contains__(' LW-'):
        position = 'LW'
    if position_and_class.__contains__(' RW ') or position_and_class.lower().__contains__('right wing') or position_and_class.__contains__(' RW-'):
        position = 'RW'
    if position_and_class.__contains__(' D ') or position_and_class.lower().__contains__('defense') or position_and_class.__contains__(' D-'):
        position = 'D'
    if position_and_class.__contains__(' G ') or position_and_class.__contains__(
            ' Goalie ') or position_and_class.lower().__contains__('goalie') or position_and_class.__contains__(' G-'):
        position = 'G'

    draft_class = position_and_class.split()[0].strip('[').strip(']').strip('(').strip(')')
    #draft_class_num = position_and_class.split()[0].strip('[').strip(']').strip('S').strip('(').strip(')')
    try:
        tpe = soup.find_all('td', 'thead')[1].small.text
        if len(tpe.split()) == 3:
            tpe = tpe.split()[2]
        else:
            tpe = tpe.split()[1]
    except:
        tpe = 'Calculation function not available'

    post = soup.find_all('div', 'post_body scaleimages')[0]
    post_text = post.text.split('\n') # split the text from the body up into rows for easy iteration

    player['Draft Class'] = 'S'+draft_class.strip('S')
    player['Draft Class Numeric'] = draft_class.strip('S')
    player['Listed TPE'] = tpe
    player['Played Position'] = position

    for l in post_text:
        ln = l.split('|')
        for line in ln:
            # why don't switch statements exist in Python???????
            if line.lower().startswith('first name'):
                try:
                    player['First Name'] = get_attr(line,1)  # this gets the first name from the first name line
                except:
                    player['First Name'] = ''
            elif line.lower().startswith('last name'):
                try:
                    player['Last Name'] = get_attr(line,1)  # this gets the first name from the last name line
                except:
                    player['Last Name'] = ''
            elif line.lower().startswith('shoots'):
                try:
                    if get_attr(line,1)  == 'L':
                        player['Shoots'] = 'Left'  # this gets the player shooting hand
                    if get_attr(line,1)  == 'R':
                        player['Shoots'] = 'Right'
                    else:
                        player['Shoots'] = get_attr(line,1) 
                except:
                    player['Shoots'] = ''
            elif line.lower().startswith('recruited'):
                try:
                    player['Recruited by'] = get_attr(line,1)   # this gets where they were recruited (if applicable)
                except:
                    player['Recruited by'] = ''
            elif line.lower().startswith('player render'):
                try:
                    player['Player Render'] = get_attr(line,1)   # this gets the player render
                except:
                    player['Player Render'] = ''
            elif line.lower().startswith('jersey number'):
                try:
                    player['Jersey Number'] = get_attr(line,1)   # this gets the player Jersey Number
                except:
                    player['Jersey Number'] = ''
            elif line.lower().startswith('height'):
                try:
                    player['Height'] = get_attr(line,1)   # this gets the player height
                except:
                    player['Height'] = ''
            elif line.lower().startswith('weight'):
                try:
                    player['Weight'] = get_attr(line,1)   # this gets the player weight
                except:
                    player['Weight'] = ''
            elif line.lower().startswith('birthplace'):
                try:
                    player['Birthplace'] = get_attr(line,1)   # this gets the player birthplace
                except:
                    player['Birthplace'] = ''
            elif line.lower().startswith('player type'):
                try:
                    player['Player Role'] = get_attr(line,1)   # this gets the player type
                except:
                    player['Player Role'] = ''
            elif line.lower().startswith('points available') or line.lower().startswith('bank') or line.lower().startswith('total bank'):
                try:
                    available = get_attr(line,1)   # this gets the amount of points the player has available
                    #available = available.split()[0].rstrip('Â')
                    player['Points Available'] = available
                except:
                    player['Points Available'] = '0'
            #if position != 'G' and player['Last Name'] != 'Yukikami' and player['Last Name'] != 'Hughes':
            #skater ratings
            if position != 'G':
                #Offensive Ratings
                if line.lower().startswith('screening'):
                    player['Screening'] = get_attr(line,1)   # this gets the player Screening
                elif line.lower().startswith('getting open'):
                    player['Getting Open'] = get_attr(line,1)   # this gets the player Getting Open
                elif line.lower().startswith('passing'):
                    player['Passing'] = get_attr(line,1)   # this gets the player Passing
                elif line.lower().startswith('puckhandling'):
                    player['Puckhandling'] = get_attr(line,1)  # this gets the player Puckhandling
                elif line.lower().startswith('shooting accuracy'):
                    player['Shooting Accuracy'] = get_attr(line,1)   # this gets the player Shooting Accuracy
                elif line.lower().startswith('shooting range'):
                    player['Shooting Range'] = get_attr(line,1)   # this gets the player Shooting Range
                elif line.lower().startswith('offensive read'):
                    player['Offensive Read'] = get_attr(line,1)   # this gets the player Offensive Read
                #Defensive Ratings
                elif line.lower().startswith('checking'):
                    player['Checking'] = get_attr(line,1)   # this gets the player Checking
                elif line.lower().startswith('hitting'):
                    player['Hitting'] = get_attr(line,1)   # this gets the player Hitting
                elif line.lower().startswith('positioning'):
                    player['Positioning'] = get_attr(line,1)   # this gets the player Positioning
                elif line.lower().startswith('stickchecking'):
                    player['Stickchecking'] = get_attr(line,1)   # this gets the player Stickchecking
                elif line.lower().startswith('shot blocking'):
                    player['Shot Blocking'] = get_attr(line,1)   # this gets the player Shot Blocking
                elif line.lower().startswith('faceoffs'):
                    player['Faceoffs'] = get_attr(line,1)   # this gets the player Faceoffs
                elif line.lower().startswith('defensive read'):
                    player['Defensive Read'] = get_attr(line,1)   # this gets the player Defensive Read
                #Physical Ratings
                elif line.lower().startswith('acceleration'):
                    player['Acceleration'] = get_attr(line,1)   # this gets the player Acceleration
                elif line.lower().startswith('agility'):
                    player['Agility'] = get_attr(line,1)   # this gets the player Agility
                elif line.lower().startswith('balance'):
                    player['Balance'] = get_attr(line,1)   # this gets the player Balance
                elif line.lower().startswith('speed'):
                    player['Speed'] = get_attr(line,1)   # this gets the player Speed
                elif line.lower().startswith('stamina'):
                    player['Stamina'] = get_attr(line,1)   # this gets the player Stamina
                elif line.lower().startswith('strength:') or line.lower().startswith('strength '):
                    player['Strength'] = get_attr(line,1)   # this gets the player Strength
                elif line.lower().startswith('fighting'):
                    player['Fighting'] = get_attr(line,1)   # this gets the player Fighting
                #Mental Ratings
                elif line.lower().startswith('aggression'):
                    player['Aggression'] = get_attr(line,1)   # this gets the player Aggression
                elif line.lower().startswith('bravery'):
                    player['Bravery'] = get_attr(line,1)   # this gets the player Bravery
                elif line.lower().startswith('*determination'):
                    player['Determination'] = '15'  # this gets the player Determination
                elif line.lower().startswith('*team player'):
                    player['Team Player'] = '15'  # this gets the player Team Player
                elif line.lower().startswith('*temperament'):
                    player['Temperament'] = '15'  # this gets the player Temperament
                elif line.lower().startswith('*professionalism'):
                    player['Professionalism'] = '15'  # this gets the player Professionalism
            #goalie ratings    
            elif position == 'G':
                #goalie ratings
                if line.lower().startswith('blocker'):
                    player['Blocker'] = get_attr(line,1)   # this gets the player Blocker
                elif line.lower().startswith('glove'):
                    player['Glove'] = get_attr(line,1)  # this gets the player Glove
                elif line.lower().startswith('passing'):
                    player['Passing'] = get_attr(line,1)   # this gets the player Passing
                elif line.lower().startswith('poke check'):
                    player['Poke Check'] = get_attr(line,1)   # this gets the player Poke Check
                elif line.lower().startswith('positioning'):
                    player['Positioning'] = get_attr(line,1)   # this gets the player Positioning
                elif line.lower().startswith('rebound'):
                    player['Rebound'] = get_attr(line,1)   # this gets the player Rebound
                elif line.lower().startswith('recovery'):
                    player['Recovery'] = get_attr(line,1)   # this gets the player Recovery
                elif line.lower().startswith('puckhandling'):
                    player['Puckhandling'] = get_attr(line,1)   # this gets the player Puckhandling
                elif line.lower().startswith('low shots'):
                    player['Low Shots'] = get_attr(line,1)   # this gets the player Low Shots
                elif line.lower().startswith('reflexes'):
                    player['Reflexes'] = get_attr(line,1)   # this gets the player Reflexes
                elif line.lower().startswith('skating'):
                    player['Skating'] = get_attr(line,1)   # this gets the player Skating
                #mental ratings
                elif line.lower().startswith('*aggression'):
                    player['Aggression'] = '8'  # this gets the player Aggression
                elif line.lower().startswith('mental toughness'):
                    player['Mental Toughness'] = get_attr(line,1)   # this gets the player Mental Toughness
                elif line.lower().startswith('*determination'):
                    player['Determination'] = '15'  # this gets the player Determination
                elif line.lower().startswith('*team player'):
                    player['Team Player'] = '15' # this gets the player Team Player
                elif line.lower().startswith('*leadership'):
                    player['Leadership'] = '15'  # this gets the player Leadership
                elif line.lower().startswith('goalie stamina'):
                    player['Goalie Stamina'] = get_attr(line,1)   # this gets the player Goalie Stamina
                elif line.lower().startswith('*professionalism'):
                    player['Professionalism'] = '15' # this gets the player Professionalism
        
    player['Applied TPE'] = get_tpe(player,player['Played Position'])
    try:
        player['Total TPE'] = get_tpe(player,player['Played Position']) + int(player['Points Available'])
    except:
        player['Total TPE'] = get_tpe(player,player['Played Position'])
    
    print(player['Team'],' - ',player['First Name'],' ',player['Last Name'],' - ',player['Played Position'])
    return player  # return the player

def get_tpe(player,position):
    if position != 'G':
        attr_set = ['Screening', 'Getting Open', 'Passing', 'Puckhandling', 'Shooting Accuracy', 'Shooting Range', 'Offensive Read',
                    'Checking','Hitting','Stickchecking','Positioning','Shot Blocking','Faceoffs','Defensive Read',
                    'Acceleration','Agility','Balance','Speed','Strength','Fighting',
                    'Aggression','Bravery',
                    #next week take stamina out of this calc
                    'Stamina'
                    ]
    elif position == 'G':
        attr_set = ['Positioning','Passing','Poke Check','Blocker','Glove','Rebound','Recovery','Puckhandling'
                      ,'Low Shots','Reflexes','Skating','Mental Toughness','Goalie Stamina'

                    ]
    try:
        tpe = 0
        for a in attr_set:
            if int(player[a]) > 17:
                tpe += (int(player[a]) - 17)*40 + (17 - 15)*25 + (15 - 13)*15 + (13 - 11)*8 + (11 - 9)*5 + (9 - 7)*2 + (7 - 5)*1
            elif int(player[a]) > 15:
                tpe += (int(player[a]) - 15)*25 + (15 - 13)*15 + (13 - 11)*8 + (11 - 9)*5 + (9 - 7)*2 + (7 - 5)*1
            elif int(player[a]) > 13:
                tpe += (int(player[a]) - 13)*15 + (13 - 11)*8 + (11 - 9)*5 + (9 - 7)*2 + (7 - 5)*1
            elif int(player[a]) > 11:
                tpe += (int(player[a]) - 11)*8 + (11 - 9)*5 + (9 - 7)*2 + (7 - 5)*1
            elif int(player[a]) > 9:
                tpe += (int(player[a]) - 9)*5 + (9 - 7)*2 + (7 - 5)*1
            elif int(player[a]) > 7:
                tpe += (int(player[a]) - 7)*2 + (7 - 5)*1
            elif int(player[a]) > 5:
                tpe += (int(player[a]) - 5)*1

        ####### NEXT WEEK ADD THIS BLOCK BACK IN ######    

        #if int(player['Stamina']) > 17:
        #    tpe += (int(player['Stamina']) - 17)*40 + (17 - 15)*25 + (15 - 11)*8
        #elif int(player['Stamina']) > 15:
        #    tpe += (int(player['Stamina']) - 15)*25 + (15 - 11)*8
        #elif int(player['Stamina']) > 11:
        #    tpe += (int(player['Stamina']) - 11)*8
        #print('Stamina',player['Stamina'],tpe)
    except:
        tpe = 0
        
    return tpe

def get_attr(line,pos):
    try:
        out = line.strip().lower().split(':')[pos]
    except:
        try:
            out = line.lower().split(' ')
            out = out[len(out)-1].strip()
        except:
            out = None
    return out

def main():
    """main"""
    url_file = "roster_urls.json"
    smjhl_players_csv = "smjhl-2020-5-12.csv"
    shl_players_csv = "shl-2020-5-12.csv"
    shl_prospects_csv = "prospects-2020-5-12.csv"
    get_smjhl_players(url_file, smjhl_players_csv)
    get_shl_players(url_file, shl_players_csv)
    get_shl_prospects(url_file, shl_prospects_csv)

main()