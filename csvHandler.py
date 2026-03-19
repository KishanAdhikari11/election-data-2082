import csv
import json
import os
from collections import defaultdict

class CSVHandler:
    """ Convert Json File into CSV file """
    def __init__(self,json_file):
        self.json_file=json_file
        self.json_data=None  
        self.grouped_data=None 
                    
    def parse_json(self):
        self.grouped_data=defaultdict(list)
        try:
            with open(self.json_file,"r") as f:
                self.json_data=json.load(f)
        except FileNotFoundError:
            print("File Not Found")
        except Exception as e:
            print(f"Error occured: {e}")
        for data in self.json_data:
            state=data["StateName"]
            district=data["DistrictName"]
            constituency=data["SCConstID"]
            self.grouped_data[(state,district,constituency)].append(data)
            self.make_folder(f"FTPT/{state}/{district}/{constituency}")
                   
    @staticmethod
    def make_folder(folder_name: str):
        try:
            os.makedirs(folder_name)
        except FileExistsError:
            print("File already exists")
        return None             

    def store_to_csv(self):
        columns=["Rank","CandidateName","PoliticalPartyName","PartySymbol","TotalVoteReceived","Gender","Age","StateName","DistrictName","Constituency","QUALIFICATION","EXPERIENCE","OTHERDETAILS","NAMEOFINST"]
        for (state,district,constituency),candidates in self.grouped_data.items():
            filename = f"FTPT/{state}/{district}/{constituency}/{constituency}.csv"
            with open(filename,"w") as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=columns)
                writer.writeheader()
                for candidate in candidates:
                      row = {
                        "Rank": candidate.get("Rank"),
                        "CandidateName": candidate.get("CandidateName"),
                        "PoliticalPartyName": candidate.get("PoliticalPartyName"),
                        "PartySymbol": candidate.get("SymbolName"),  # map SymbolName to PartySymbol
                        "TotalVoteReceived": int(candidate.get("TotalVoteReceived")),
                        "Gender": candidate.get("Gender"),
                        "Age": candidate.get("Age"),
                        "StateName": candidate.get("StateName"),
                        "DistrictName": candidate.get("DistrictName"),
                        "Constituency": candidate.get("SCConstID"),
                        "QUALIFICATION": candidate.get("QUALIFICATION"),
                        "EXPERIENCE": candidate.get("EXPERIENCE"),
                        "OTHERDETAILS": candidate.get("OTHERDETAILS"),
                        "NAMEOFINST": candidate.get("NAMEOFINST"),
                    }
                      writer.writerow(row)
        
        
    