import asyncio
import os
from getData import DataExtractor
from csvHandler import CSVHandler
from constant import PROVINCE_NAMES  


async def run_election_scraper():
    base_url = "https://result.election.gov.np/ElectionResultCentral2082.aspx"
    extractor = DataExtractor(base_url)
    
    try:
        print("Fetching FTPT data...")
        ftpt_raw = await extractor.get_FTPT_data()
        ftpt_handler = CSVHandler(ftpt_raw, "FTPT")
        ftpt_handler.parse_json()
        ftpt_handler.store_to_csv()
        
        print("Fetching National PR data...")
        os.makedirs("PR", exist_ok=True)
        total_pr_raw = await extractor.get_PR_data()
        total_pr_handler = CSVHandler(total_pr_raw, "PR")
        total_pr_handler.store_to_csv(file_name="PR/Total.csv")
        
        print("Fetching Province PR data...")
        province_data_list = await extractor.get_province_wise_data()
        for i, data in enumerate(province_data_list, start=1):
            province_name = PROVINCE_NAMES.get(i, f"प्रदेश-{i}")
            p_handler = CSVHandler(data, "PR")
            p_handler.store_to_csv(file_name=f"PR/{province_name}.csv")
        
        print("Fetching Constituency PR data (this may take a while)...")
        const_data_map = await extractor.get_constituency_wise_data()
        
        for (state_num, district_name, const_str), candidates in ftpt_handler.grouped_data.items():
            if not candidates:
                continue
                
            try:
                const_num = int(const_str)
            except ValueError:
                print(f"Invalid constituency ID: {const_str} in {district_name}")
                continue
            
            district_cd = None
            for cand in candidates:
                dc = cand.get("DistrictCd")
                if dc is not None:
                    try:
                        district_cd = int(dc)
                        break
                    except (ValueError, TypeError):
                        pass
            
            if district_cd is None:
                print(f"Warning: No valid DistrictCd found for {district_name} - {const_str} (state {state_num})")
                continue
            
            pr_data = const_data_map.get((district_cd, const_num))
            
            if pr_data:
                province_name = PROVINCE_NAMES.get(state_num, f"{state_num}")
                
                folder_path = f"PR/{province_name}/{district_name}"
                os.makedirs(folder_path, exist_ok=True)
                
                csv_path = f"{folder_path}/{const_num}.csv"
                
                c_handler = CSVHandler(pr_data, "PR")
                c_handler.store_to_csv(file_name=csv_path)
                
                print(f"Saved constituency PR: {csv_path}")
            else:
                print(f"No PR data for district {district_cd} constituency {const_num} ({district_name})")
                
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        await extractor.close()

if __name__ == "__main__":
    asyncio.run(run_election_scraper())