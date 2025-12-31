import time

import gspread
import numpy as np
import pandas as pd
from gspread_dataframe import *
from gspread_formatting import *


def retry(exceptions, total_tries=1000, delay=1):
    def retry_decorator(f):
        def func_with_retries(*args, **kwargs):
            _tries = total_tries + 1
            while _tries > 1:
                try:
                    return f(*args, **kwargs)
                except:
                    # print(e)
                    print(f"{_tries} Retrying")
                    time.sleep(3)
                    _tries -= 1
                    if _tries == 1:
                        raise
                    time.sleep(delay)

        return func_with_retries

    return retry_decorator


class GoogleSheetOps:

    def __init__(self, service_account_key):
        self.sa = gspread.service_account(filename=service_account_key)

    def get_sheet(self, sheet_name):
        sh = self.sa.open_by_url(sheet_name)
        return sh

    @retry(gspread.exceptions.APIError)
    def setting_data_as_df(self, data, sheets):
        set_with_dataframe(sheets, data)

    @retry(gspread.exceptions.APIError)
    def get_worksheet(self, sheet_name, worksheet_name):
        sh = self.get_sheet(sheet_name)
        wks = sh.worksheet(worksheet_name)
        return wks

    @retry(gspread.exceptions.APIError)
    def get_worksheet_df(self, sh, worksheet_name):
        wks = sh.worksheet(worksheet_name)
        wks_df = pd.DataFrame(wks.get_all_records(numericise_ignore=['all']))
        return wks_df

    @retry(gspread.exceptions.APIError)
    def get_worksheet_as_df(self, sheet_name, worksheet_name):
        sh = self.get_sheet(sheet_name)
        wks_df = self.get_worksheet_df(sh, worksheet_name)
        return wks_df

    @retry(gspread.exceptions.APIError)
    def add_data_(self, data, sheet_name, worksheet_name, header=True, spacing=0, table_range=None):
        data = data.replace(np.nan, '')
        sh = self.get_sheet(sheet_name)
        wks = sh.worksheet(worksheet_name)
        space = [[''] * data.shape[1] for _ in range(spacing)]
        data_ = data.values.astype(str).tolist()
        existing_header = wks.row_values(1)
        if header:
            header = data.columns.values.tolist()
            if existing_header != header:
                wks.insert_row(header, 1)
        wks.freeze(1, 0)
        wks.append_rows(space + data_, table_range=table_range)

    @retry(gspread.exceptions.APIError)
    def create_worksheet(self, sheet_name, worksheet_name):
        sh = self.get_sheet(sheet_name)
        worksheets = [s.title for s in sh.worksheets()]
        if worksheet_name not in worksheets:
            sh.add_worksheet(title=worksheet_name, rows="100", cols="20")

    @retry(gspread.exceptions.APIError)
    def create_new_worksheet(self, title):
        sh = self.sa.create(title)
        # worksheets = [sh.title for s in sh.worksheets()]
        # if worksheet_name not in worksheets:
        #     sh.add_worksheet(title=worksheet_name, rows="100", cols="20")
        return sh

    def get_coloring_rules(self, end_col, end_row, sheet, start_col, start_row):

        return ConditionalFormatRule(
            ranges=[
                GridRange(
                    sheetId=sheet.id,
                    startRowIndex=start_row,
                    endRowIndex=end_row,
                    startColumnIndex=start_col,
                    endColumnIndex=end_col)
            ],
            gradientRule=GradientRule(
                maxpoint=InterpolationPoint(
                    color=Color.fromHex("#57BB8A"), type="Percent", value="100"),
                midpoint=InterpolationPoint(
                    color=Color.fromHex("#EFEFEF"), type="Percentile", value="50"),
                minpoint=InterpolationPoint(
                    color=Color.fromHex("#E67C73"), type="MIN"),
            ))

    def apply_coloring_gradient(self, sheet, rule):
        apply_color = get_conditional_format_rules(sheet)
        apply_color.clear()
        apply_color += rule
        apply_color.save()


if __name__ == '__main__':
    gs = GoogleSheetOps(service_account_key=r'C:\Users\Saurabh\PycharmProjects\keys.json')
    # dashboard = gs.get_worksheet_as_df('DeploymentConfigurations', 'DeploymentConfigurations')
    # layers = gs.get_worksheet_as_df('DeploymentConfigurations', 'Layers')

    df = gs.get_worksheet_as_df('VL', 'Sheet1')
# gs.add_data(df, 'VL', 'Sheet1')