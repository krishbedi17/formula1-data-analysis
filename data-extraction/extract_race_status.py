import requests
import pandas as pd
from xml.dom.minidom import parseString

url = "http://ergast.com/api/f1/status"
offset = 0
limit = 30
statuses = []
while offset < 121:
    page_url = f"{url}?limit={limit}&offset={offset}"
    response = requests.get(page_url)

    if response.status_code == 200:
        offset += limit
        dom = parseString(response.text)
        status_elements = dom.getElementsByTagName("Status")
        if not status_elements:
            break
        for status in status_elements:
            status_id = status.getAttribute("statusId")
            name = status.firstChild.nodeValue
            count = status.getAttribute("count")

            statuses.append({
                'statusId': status_id,
                'name': name,
                'count': count
            })

df = pd.DataFrame(statuses)

df.to_csv('status_data.csv', index=False)
print("Data saved to status_data.csv")