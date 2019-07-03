#https://pypi.org/project/TogglPy/
import time
from datetime import datetime, date, timedelta
import json

from toggl.TogglPy import Toggl
import xlrd, xlwt
from xlutils.copy import copy

from functions.readConfig import readConfig


class TogglMe:
    def __init__(self, user_agent=None, workspace_id=None):
        if user_agent == workspace_id is None:
            return None

        cf = readConfig()
        self.config = cf.config

        self.start_col = 0
        self.start_row = 0

        self.user_agent = user_agent
        self.workspace_id = workspace_id
        self.response = None
        self.last_month_first = None
        self.last_month_last = None
        self.filename = None

        self.my_excel_data = []
        self.excel_template = "excel/test_file.xlsx"
        self.excel_file = None

        self.about_last_month()
        self.get_data()
        self.parse_data()
        self.create_excel()

    def about_last_month(self):
        now = time.localtime()
        last_month = now.tm_mon - 1 if now.tm_mon > 1 else 12
        year = now.tm_year if now.tm_mon > 1 else now.tm_year - 1

        self.filename = "data/{}{}".format(year, last_month)
        self.excel_file = "output/{}{}.xlsx".format(year, last_month)

        # Get the last day of last month by taking the first day of this month
        # and subtracting 1 day.
        last = date(now.tm_year, now.tm_mon, 1) - timedelta(1)

        # Set the day to 1 gives us the start of last month
        first = last.replace(day=1)

        # The default string representation of these datetime instances is
        # YYYY-mm-dd format (which is what I usually need),
        # so we can just print them out
        self.last_month_first = first
        self.last_month_last = last

    def get_data(self):
        toggl = Toggl()
        toggl.setAPIKey(self.config['api'])

        data = {
            'workspace_id': workspace_id,
            'user_agent': user_agent,
            'since': self.last_month_first,
            'until': self.last_month_last
        }
        self.response = toggl.request("https://toggl.com/reports/api/v2/details", parameters=data)
        self.save_raw_data()

    def parse_data(self):
        for d in self.response['data']:
            toggl_date = self.convert_timedate(d['start'])

            row = toggl_date[0].day+self.start_row
            col = toggl_date[0].month+self.start_col
            toggl_time = self.convert_millis(d['dur'])
            data = col, row, toggl_time[2]
            self.my_excel_data.append(data)

    def create_excel(self):
        rb = xlrd.open_workbook(self.excel_template)  # Make Readable Copy
        wb = copy(rb)  # Make Writeable Copy

        ws1 = wb.get_sheet(0)  # Get sheet 1 in writeable copy
        for data in self.my_excel_data:
            ws1.write(data[0], data[1], data[2])

        wb.save(self.excel_file)  # Save the newly written copy. Enter the same as the old path to write over

    @staticmethod
    def convert_timedate(date_time_str=None):
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S+02:00')
        return date_time_obj, date_time_obj.strftime("%Y-%m-%d")

    @staticmethod
    def convert_millis(milli=None):
        seconds = round((milli / 1000) % 60)
        minutes = round((milli / (1000 * 60)) % 60)
        hours = round(((milli / (1000 * 60 * 60)) % 24),1)
        return seconds, minutes, hours

    def save_raw_data(self):
        app_json = json.dumps(self.response)

        f = open("{}.json".format(self.filename), "w")
        f.write(app_json)
        f.close()


if __name__ == '__main__':
    user_agent = "theo@vandersluijs.nl"
    workspace_id = 881607
    t = TogglMe(user_agent, workspace_id)

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



