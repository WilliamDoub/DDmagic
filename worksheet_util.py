import spreadsheet_config as s_config
import pygsheets as pyg

# UTILITY METHOD TO OVERWRITE DATAFRAME TO GSHEET
def overwrite_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    """
    Overwrites data_df under spreadsheet_id and sheet_name 
    using your credentials under service_file_path.
    """
    wks_write = get_wks(service_file_path, spreadsheet_id, sheet_name)
    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1

# UTILITY METHOD TO ADD DATAFRAME TO GSHEET AT (m, n)
def add_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df, m: int, n: int):
    """
    Adds data_df to the next available row under spreadsheet_id
    and sheet_name using your credentials under service_file_path.
    """
    wks = get_wks(service_file_path, spreadsheet_id, sheet_name)
    wks.set_dataframe(data_df, (m,n), encoding='utf-8', extend=True)
    wks.frozen_rows = 1

def get_wks(service_file_path, spreadsheet_id, sheet_name):
    gc = pyg.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks = sh.worksheet_by_title(sheet_name)
    return wks

def get_next_row_num_in_col(service_file_path, spreadsheet_id, sheet_name, n: int):
    wks = get_wks(service_file_path, spreadsheet_id, sheet_name)
    col = wks.get_col(n) # Get column n (returns a list)
    next_row_num = len(col) + 1
    return next_row_num

def insert_at_next_row_in_col(service_file_path, spreadsheet_id, sheet_name, data_df, n):
    next_row_num = get_next_row_num_in_col(service_file_path, spreadsheet_id, sheet_name, n)
    add_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df, next_row_num, n)

# UTILITY METHOD TO ADD DATAFRAME TO GSHEET ON NEXT AVAILABLE ROW
def insert_at_next_row_in_sheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    insert_at_next_row_in_col(service_file_path, spreadsheet_id, sheet_name, data_df, 1)


#row_num = get_next_row_num_in_col(s_config.service_file_path, s_config.spreadsheet_id, s_config.sheet_name2, 1)
#print(row_num)
'''
wks = get_wks(s_config.service_file_path, s_config.spreadsheet_id, s_config.sheet_name2)
col = wks.get_col(3)
print(col)
'''