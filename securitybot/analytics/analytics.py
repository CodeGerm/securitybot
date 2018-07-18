from urllib2 import Request, urlopen, quote
import json
from os import getenv

BASE_URL = 'https://data-platform-pod0-dev.centrify.io'
TOKEN = getenv('ANALYTICS_TOKEN')
DASHBOARD_URL = BASE_URL + '/analytics/ui/#/dashboards'

def list_insightlets():

        url = BASE_URL + "/analytics/services/v1.0/preference/dashboards/library/widgets/summaries"
        widgets = []
        req = Request(url)
        req.add_header("authorization", "Bearer " + TOKEN)
        resp = urlopen(req).read()
        jsons = json.loads(resp)
        for i in range(len(jsons)):
            widgets.append(jsons[i]['parcel_name'])
        return  widgets

def get_insightlet(name):
    # type: () -> str
        url = BASE_URL + "/report?token={token}&uri=&uri=/analytics/ui/%23/widgets?parcel_name={name}&embedded=true&type=screenshot&height=600&width=800&delay=1000"
        return url.format(token=TOKEN, name=name)
        #img_name = "/tmp/" + name + ".jpg"
        #urllib.request.urlretrieve(url, img_name)

def get_insightlet_id(id):
    # type: () -> Tuple[str, str]
        i = int(id)
        widgets = list_insightlets()
        name = quote(widgets[i])
        url = BASE_URL + "/report?token={token}&uri=/analytics/ui/%23/widgets?parcel_name={name}%26embedded=true&type=screenshot&height=600&width=800&delay=2500"
        return (widgets[i], url.format(token=TOKEN, name=name))


def list_insightlet_message():
    # type: () -> str
        widgets = list_insightlets()
        md = ''
        for i in range(len(widgets)):
            md += str(i) + ". " + widgets[i] + '\n'
        return "```" + md + "```\n"

def main():
        print list_insightlet_message()


if __name__ == '__main__':
        main()
