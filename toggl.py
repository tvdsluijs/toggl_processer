#https://pypi.org/project/TogglPy/
import time
import datetime
import json

from functions.readConfig import readConfig

from toggl.TogglPy import Toggl


class Toggle:
    def __init__(self, user_agent=None, workspace_id=None):
        if user_agent == workspace_id is None:
            return None

        cf = readConfig()
        self.config = cf.config

        self.config['api']
        self.user_agent = user_agent
        self.workspace_id = workspace_id
        self.response = None
        self.last_month_first = None
        self.last_month_last = None
        self.filename = None

        self.about_last_month()
        self.get_data()
        self.save_data()

    def about_last_month(self):
        now = time.localtime()

        self.filename = "{}{}".format(now.year, now.month(-1))

        # Get the last day of last month by taking the first day of this month
        # and subtracting 1 day.
        last = datetime.date(now.tm_year, now.tm_mon, 1) - datetime.timedelta(1)

        # Set the day to 1 gives us the start of last month
        first = last.replace(day=1)

        # The default string representation of these datetime instances is
        # YYYY-mm-dd format (which is what I usually need),
        # so we can just print them out
        self.last_month_first = first
        self.last_month_last = last

    def get_data(self):
        toggl = Toggl()
        toggl.setAPIKey(api)

        data = {
            'workspace_id': workspace_id,
            'user_agent': user_agent,
            'since': self.last_month_first,
            'until': self.last_month_last
        }
        self.response = toggl.request("https://toggl.com/reports/api/v2/details", parameters=data)

        # for d in self.response['data']:
        #     print

    def save_data(self):
        app_json = json.dumps(self.response)

        f = open("{}.json".format(self.filename), "w")
        f.write(app_json)
        f.close()


if __name__ == '__main__':
    user_agent = "theo@vandersluijs.nl"
    workspace_id = 881607
    t = Toggle(user_agent, workspace_id)

# todayDate = datetime.date.today()
# if todayDate.day > 25:
#     todayDate += datetime.timedelta(7)
# print(todayDate.replace(day=1))

# response = toggl.request("https://toggl.com/reports/api/v2/weekly")

# data = {
#          'workspace_id': workspace_id,
#          'user_agent': user_agent,
#          'since':'2019-06-01',
#          'until':'2019-06-30'
#         }
# response = toggl.request("https://toggl.com/reports/api/v2/summary", parameters=data)

# data = {
#          'workspace_id': workspace_id,
#          'user_agent': user_agent
#         }
# response = toggl.request("https://toggl.com/reports/api/v2/weekly", parameters=data)


# for line in response:
#     print(line)


# print(response)

# print(toggl.getWorkspaces())
# print(toggl.getClients())



