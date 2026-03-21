import httpx
from constant import DISTRICT_CONSTITUENCIES
import asyncio
import random


class DataExtractor:
    def __init__(self,base_url: str):
        self.user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        self.csrf_token=None
        self.base_url=base_url
        self.client = httpx.AsyncClient(
            headers={"user-agent": self.user_agent},
            timeout=30.0
        )
        self.initialized = False
        self.semaphore = asyncio.Semaphore(3)
        
    async def init_session(self):
        if not self.initialized:
            r = await self.client.get(self.base_url)
            r.raise_for_status()
            self.initialized = True
            
    async def close(self):
        await self.client.aclose()

        
    async def send_request(self,files):
        async with self.semaphore:
            await self.init_session()
            
            await asyncio.sleep(random.uniform(1.5,2.5))
        
            csrf_token=self.client.cookies.get("CsrfToken")
            headers={"user-agent":self.user_agent,
                    "x-csrf-token": csrf_token,
                    "x-requested-with": "XMLHttpRequest",
                    "referer": self.base_url,
            }
            r = await self.client.get(
                    "https://result.election.gov.np/Handlers/SecureJson.ashx",
                        params={"file":files},
                        headers=headers,
                )
            r.raise_for_status()
                
            return r.json()
        

    async def get_FTPT_data(self):
        files= "JSONFiles/ElectionResultCentral2082.txt"  
        data=await self.send_request(files)
        return data
        
        
    async def get_PR_data(self) :
        files="JSONFiles/Election2082/Common/PRHoRPartyTop5.txt"
        data= await self.send_request(files)
        return data
    
    async def get_province_wise_data(self)-> list:
        provincal_data=[]
        for i in range(1,8):
            files=f"JSONFiles/Election2082/HOR/PR/Province/{i}.json"
            data=await self.send_request(files)
            provincal_data.append(data)
        return provincal_data
            
    async def get_constituency_wise_data(self):
        constituency_data={}
        for dist,v in DISTRICT_CONSTITUENCIES.items():
            for const in range(1,v+1):
                files=f"JSONFiles/Election2082/HOR/PR/HOR/HOR-{dist}-{const}.json"
                data=await self.send_request(files)
                constituency_data[(dist,const)]=data  
        return constituency_data
                
                    