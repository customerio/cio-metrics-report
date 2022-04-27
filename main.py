import requests
import json
import csv
import time
import os
from datetime import datetime, date, timedelta
from customerio import APIClient, SendEmailRequest, CustomerIOException

workspaceID = os.environ.get("CustomerWorkspaceID")
apitbID = os.environ.get("InternalAPITBID")
InternalSegmentID = os.environ.get("InternalAPITBSegment")

CIOheaders = {
    'Authorization': f'Bearer {os.environ.get("CustomerBearer")}',
    'Content-Type': 'application/json'
}

APITBheaders = {
    'Authorization': f'Bearer {os.environ.get("InternalAPITBBearer")}',
    'Content-Type': 'application/json'
}


# For newsletter sorting purposes. Extract the time the newsletter was sent.
def extract_time(to_sort):
    try:
        return int(to_sort['sent_at'])
    except KeyError:
        return 0

# For campaign sorting purposes. Extract the number of messages sent.
def extract_sent(to_sort):
    try:
        return int(to_sort['sent'])
    except KeyError:
        return 0

def buildReport(request):
    if request.args:
        entity = request.args.get('entity', "newsletters")
    else:
        entity = 'newsletters'

    url1 = f'https://beta-api.customer.io/v1/api/{entity}'
    r1 = requests.get(url1, headers=CIOheaders)
    res1 = r1.json()

    results = []
    to_sort = []

    for r in res1[entity]:
        name = r["name"]
        id = r["id"]
        now = int(time.time())
        
        if entity == 'newsletters':
            ui_overview_link = f"https://fly.customer.io/env/{workspaceID}/broadcasts/newsletter/{id}/overview/reports"
            sent_at = r["sent_at"]

            if sent_at is None:
                continue

            seconds_since_send = now-sent_at
            report_window = int(seconds_since_send/86400)
        elif entity == 'campaigns':
            ui_overview_link = f"https://fly.customer.io/env/{workspaceID}/{entity}/{id}/overview/"
            sent_at = r["updated"]
            active = r["active"]
            if active == False:
                continue
            report_window = 7
        else:
            continue

        if report_window < 8:
            if entity == 'newsletters':
                period = 'period=days&steps=2'
            elif entity == 'campaigns':
                period = 'period=days&steps=1'
            r2 = requests.get(('https://beta-api.customer.io/v1/api/%s/%s/metrics?%s' % (entity, r['id'], period)), headers=CIOheaders)
            res2 = r2.json()


            if entity == 'newsletters':
                sent_count = res2["metric"]["totals"]["sent"]
                sent_datetime = datetime.fromtimestamp(sent_at)
                series = res2["metric"]["totals"]
                sent = res2["metric"]["totals"]["sent"]
                delivered = res2["metric"]["totals"]["delivered"]
                clicked = res2["metric"]["totals"]["clicked"]
                bounced = res2["metric"]["totals"]["bounced"]
                spammed = res2["metric"]["totals"]["spammed"]
                unsubscribed = res2["metric"]["totals"]["unsubscribed"]
                opened = res2["metric"]["totals"]["opened"]
                now_dt = datetime.fromtimestamp(now)
            elif entity == 'campaigns':
                if res2["metric"]["series"]["sent"][0] == 0 or res2["metric"]["series"]["delivered"][0] == 0:
                    continue
                
                sent_count = res2["metric"]["series"]["sent"][0]
                sent_datetime = datetime.fromtimestamp(sent_at)
                series = res2["metric"]["series"]
                sent = res2["metric"]["series"]["sent"][0]
                delivered = res2["metric"]["series"]["delivered"][0]
                clicked = res2["metric"]["series"]["clicked"][0]
                bounced = res2["metric"]["series"]["bounced"][0]
                spammed = res2["metric"]["series"]["spammed"][0]
                unsubscribed = res2["metric"]["series"]["unsubscribed"][0]
                opened = res2["metric"]["series"]["opened"][0]
                now_dt = datetime.fromtimestamp(now)
                yesterday = date.today() - timedelta(days=1)
                yesterday_dt = yesterday.strftime("%Y-%m-%d")

            if opened > 0:
                opened_rate = round((opened/delivered)*100, 2)
            else:
                opened_rate = 0
            if clicked > 0:
                clicked_rate = round((clicked/opened)*100, 2)
            else:
                clicked_rate = 0
            if delivered > 0:
                delivered_rate = round((delivered/sent)*100, 2)
            else:
                delivered_rate = 0
            if unsubscribed > 0:
                unsubscribed_rate = round((unsubscribed/delivered)*100, 4)
            else:
                unsubscribed_rate = 0
            if spammed > 0:
                spammed_rate = round((spammed/delivered)*100, 4)
            else:
                spammed_rate = 0
            if bounced > 0:
                bounced_rate = round((bounced/delivered)*100, 4)
            else:
                bounced_rate = 0

            to_sort.append({
                "id": id,
                "ui_overview_link": ui_overview_link,
                "name": name,
                "sent_at": sent_at,
                "sent_datetime": str(sent_datetime.strftime("%Y-%m-%d")),
                "sent": sent,
                "bounced": bounced,
                "bounced_rate": bounced_rate,
                "delivered": delivered,
                "delivered_rate": delivered_rate,
                "opened": opened,
                "opened_rate": opened_rate,
                "clicked": clicked,
                "clicked_rate": clicked_rate,
                "unsubscribed": unsubscribed,
                "unsubscribed_rate": unsubscribed_rate,
                "spammed": spammed,
                "spammed_rate": spammed_rate
            })
            
    if entity == 'newsletters':
        to_sort = sorted(to_sort,key=extract_time,reverse=True)
    elif entity == 'campaigns':        
        to_sort = sorted(to_sort,key=extract_sent,reverse=True)

    url3 = f'https://api.customer.io/v1/campaigns/{apitbID}/triggers'

    apitbData = {
        "recipients":
            {"segment":
                {"id": InternalSegmentID}
            },
        "data":{
            "entity":entity,
            "date_range": yesterday_dt if entity=="campaigns" else "the last 7 days",
            "entity_data":to_sort
        }
    }
    
    try:
        r3 = requests.post(url3, headers=APITBheaders, data=json.dumps(apitbData))
        
        res3 = r3.json()
        # print(json.dumps(res3,indent=4))
        
        if res3.get('errors'):
            return f"Error: {res3.get('errors').get[0].get('detail')}"
        else:
            return f"Broadcast Triggered."
    except:
      return "There was an error. Reach out to services@customer.io for details."