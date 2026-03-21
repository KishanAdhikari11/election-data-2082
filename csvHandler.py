import csv
import os
from collections import defaultdict
from typing import Literal

class CSVHandler:
    """ Convert Json File into CSV file """
    def __init__(self,json_data,type:Literal["FTPT","PR"]):
        self.json_data=json_data
        self.type=type
        self.grouped_data=None 
        
                    
    def parse_json(self):
        self.grouped_data=defaultdict(list)
        for data in self.json_data:
            state=data["StateName"]
            district=data["DistrictName"]
            constituency=data["SCConstID"]
            self.grouped_data[(state,district,constituency)].append(data)
            self.make_folder(f"{self.type}/{state}/{district}")
                   
    @staticmethod
    def make_folder(folder_name: str):
        try:
            os.makedirs(folder_name)
        except FileExistsError:
            pass
        return None             

    def store_to_csv(self,file_name=None):
        if self.type=="FTPT":
            columns=["Rank","CandidateName","PoliticalPartyName","PartySymbol","TotalVoteReceived","Gender","Age","Status","StateName","DistrictName","Constituency","QUALIFICATION","EXPERIENCE","OTHERDETAILS","NAMEOFINST"]
            for (state,district,constituency),candidates in self.grouped_data.items():
                filename = f"{self.type}/{state}/{district}/{constituency}.csv"
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
                            "Status":candidate.get("Remarks"),
                            "StateName": candidate.get("StateName"),
                            "DistrictName": candidate.get("DistrictName"),
                            "Constituency": candidate.get("SCConstID"),
                            "QUALIFICATION": candidate.get("QUALIFICATION"),
                            "EXPERIENCE": candidate.get("EXPERIENCE"),
                            "OTHERDETAILS": candidate.get("OTHERDETAILS"),
                            "NAMEOFINST": candidate.get("NAMEOFINST"),
                        }
                        writer.writerow(row)
        elif self.type == "PR":
            columns = ["Rank", "PoliticalPartyName", "SymbolName", "TotalVoteReceived"]

            with open(file_name, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()

                for index, data in enumerate(self.json_data):
                    row = {
                        "Rank": index + 1,
                        "PoliticalPartyName": data.get("PoliticalPartyName"),
                        "SymbolName": data.get("SymbolName"),
                        "TotalVoteReceived": int(data.get("TotalVoteReceived")),
                    }
                    writer.writerow(row)   