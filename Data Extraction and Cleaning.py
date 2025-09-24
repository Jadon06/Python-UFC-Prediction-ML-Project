from bs4 import BeautifulSoup
import pandas as pd
import requests

fighter1 = input("Enter a fighter: ").title().strip()
last_name_initial = fighter1.split(" ", 1)[1][0].lower()

fighter2 = input("Enter a fighter: ").title().strip()
last_name_initial2 = fighter2.split(" ", 1)[1][0].lower()

All_fighters_inital1 = 'http://ufcstats.com/statistics/fighters?char='+last_name_initial+'&page=all'
All_fighters_inital2 = 'http://ufcstats.com/statistics/fighters?char='+last_name_initial2+'&page=all'

class FighterInfo:
    def __init__(self, data, fighter):
        self.data = data
        self.fighter = fighter
        #self.fighter2 = fighter2

    def get_data(self):
        page = requests.get(self.data)
        self.soup = BeautifulSoup(page.text, 'html.parser')
        self.row_data = self.soup.find_all("tr")

    def get_headers(self):
        self.table_headers = []
        headers = self.soup.find_all("th")
        for header in headers:
            self.table_headers.append(header.text.strip())
    
    def set_dataframe(self):
        self.dataframe = pd.DataFrame(columns = self.table_headers)
        return(self.dataframe)

    def get_urls(self):
        self.urls = []
        self.stats = []
        for row in self.row_data:
            cell_data = row.find_all("td")
            length = len(self.dataframe)
            row_info = [data.text.strip() for data in cell_data]
            try:
                self.dataframe.loc[length] = row_info
            except ValueError:
                pass
            for tag in cell_data:
                reference_url = tag.find('a')
                if reference_url:
                    self.urls.append(reference_url['href'])
        self.urls = [
            link for i, link in enumerate(self.urls)
            if link not in self.urls[:i]]
        self.urls = [sublist for sublist in self.urls if sublist]
    
    def set_dataframe_urls(self):
            self.dataframe['UFC Link'] = self.urls
            return(self.dataframe)

    def find_fighter(self):
        fighter_name_fixed = self.fighter.title().strip()
        fighter_split_name = self.fighter.split(" ")

        fighter_firstname = fighter_split_name[0]
        fighter_lastname = fighter_split_name[1]

        mask = (
            (self.dataframe['First'] == fighter_firstname) & 
            (self.dataframe['Last'] == fighter_lastname)
        )

        index = self.dataframe.index[mask]
        self.link = list(self.dataframe.loc[index, 'UFC Link'])
        return(self.dataframe.iloc[index])

    def get_fighter_info(self):
        url = self.link[0]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        row_data = soup.find_all("tr")

        self.individual_row_data = []
        for row in row_data:
            cell_data = row.find_all("td")
            row_info = []
            for cell in cell_data:
                row_info.append(cell.get_text(strip=True, separator=" "))
            self.individual_row_data.append(row_info)

        self.individual_row_data = [
            row for row in self.individual_row_data
            if any(cell.strip() for cell in row)
        ]
        self.table_headers_fighter = []
        title_headers = soup.find_all("th")
        for header in title_headers:
            self.table_headers_fighter.append(header.text.strip())

    def set_fighthistory_dataframe(self):
        self.dataframe_fighthistory = pd.DataFrame(columns = self.table_headers_fighter)
        for row in self.individual_row_data:
            length = len(self.dataframe_fighthistory)
            self.dataframe_fighthistory.loc[length] = row

    def clean_data(self):
        self.dataframe_fighthistory[["Td_fighter", "Td_opponent"]] = (
            self.dataframe_fighthistory["Td"].astype(str).str.split(" ", expand=True)
        )

        self.dataframe_fighthistory[["Kd_fighter", "Kd_opponent"]] = (
            self.dataframe_fighthistory["Kd"].astype(str).str.split(" ", expand=True)
        )

        split_names = (
            self.dataframe_fighthistory["Fighter"].astype(str).str.split(" ", expand=True)
        )

        self.dataframe_fighthistory["Fighter"] = split_names[0] + " " + split_names[1]
        self.dataframe_fighthistory["Opponent"] = split_names[2] + " " + split_names[3]


        self.dataframe_fighthistory[["Str_fighter", "Str_opponent"]] = (
            self.dataframe_fighthistory["Str"].astype(str).str.split(" ", expand=True)
        )

        self.dataframe_fighthistory[["Sub_fighter", "Sub_opponent"]] = (
            self.dataframe_fighthistory["Sub"].astype(str).str.split(" ", expand=True)
        )

        reorder = [
            "W/L", "Fighter", "Opponent", "Kd_fighter", "Kd_opponent",
            "Str_fighter", "Str_opponent", "Td_fighter", "Td_opponent",
            "Sub_fighter", "Sub_opponent", "Event", "Method", "Time"
        ]

        self.dataframe_fighthistory = self.dataframe_fighthistory[reorder]  
    
    def run_all(self):
        self.get_data()
        self.get_headers()
        self.set_dataframe()
        self.get_urls()
        self.set_dataframe_urls()
        self.find_fighter()
        self.get_fighter_info()
        self.set_fighthistory_dataframe()
        self.clean_data()
    
    def Display(self):
        return(self.dataframe_fighthistory)
        
F1_info = FighterInfo(All_fighters_inital1, fighter1)
F1_info.run_all()
fighthistory1 = F1_info.Display()
print(fighthistory1)

F2_info = FighterInfo(All_fighters_inital2, fighter2)
F2_info.run_all()
fighthistory2 = F2_info.set_dataframe_urls()
print(fighthistory2)