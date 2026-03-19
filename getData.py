import httpx
import json
import asyncio
from csvHandler import CSVHandler

async def get_data(base_url: str) -> json:
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    async with httpx.AsyncClient() as client:
        await client.get(base_url)
        csrf_token=client.cookies.get("CsrfToken")
        headers={"user-agent":user_agent,
                  "x-csrf-token": csrf_token,
                "x-requested-with": "XMLHttpRequest",
                "referer": base_url,
        }
        
        params = {
            "file": "JSONFiles/ElectionResultCentral2082.txt"   #this needs to be figure out for district wise PR

        }
        
        r = await client.get(
            "https://result.election.gov.np/Handlers/SecureJson.ashx",
            params=params,
            headers=headers,
        )

        return r.json()


def store_to_json(data,filename)-> None:
    try:
        with open(filename,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
    except Exception as e:
        print("Error occured while dumping to json: ",e)
          