from getData import get_data,store_to_json
from csvHandler import CSVHandler
import asyncio

def main():
    filename="election-2082.json"
    data=asyncio.run(get_data("https://result.election.gov.np/ElectionResultCentral2082.aspx"))
    store_to_json(data,filename)
    handler=CSVHandler(filename)
    handler.parse_json()
    handler.store_to_csv()

if __name__=="__main__":
    main()
    
    