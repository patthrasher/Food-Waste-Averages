import gspread
from oauth2client.service_account import ServiceAccountCredentials

def blanks_to_zeros(str_row, int_list) :
    str_row.pop(0)
    for each in str_row :
        if each == '' :
            each = 0
        int_list.append(int(each)) # make separate function for converting to int?
    add_zeros(int_list)

def add_zeros(int_row) : # add zeros if end of spreadsheet was blank
    if len(int_row) < 35 :
        zeros = 35 - len(int_row)
        j = 1
        while j <= zeros :
            int_row.append(0)
            j = j + 1

def add_days(item, row) :
    item['mon'] += row[4]
    item['tue'] += row[9]
    item['wed'] += row[14]
    item['thu'] += row[19]
    item['fri'] += row[24]
    item['sat'] += row[29]
    item['sun'] += row[34]

def days_average(item, item_av) :
    for key, value in item.items() :
        item_av[key] = two_decimals(value / how_many_sheets)
    mon = str(item_av['mon'])
    tue = str(item_av['tue'])
    wed = str(item_av['wed'])
    thu = str(item_av['thu'])
    fri = str(item_av['fri'])
    sat = str(item_av['sat'])
    sun = str(item_av['sun'])
    print('    ' + 'Mon: ' + mon + '  Tue: ' + tue + '  Wed: ' + wed + '  Thu: ' + thu + '  Fri: ' + fri + '  Sat: ' + sat + '  Sun: ' + sun)
    return item_av

def two_decimals(av):
    string = str(av)
    slice = string[:4]
    if len(slice) == 3 : # makes each output 4 characters
        slice = slice + '0'
    return slice

# totals
bean = {'mon' : 0, 'tue' : 0, 'wed' : 0, 'thu' : 0, 'fri' : 0, 'sat' : 0, 'sun' : 0}
migas = {'mon' : 0, 'tue' : 0, 'wed' : 0, 'thu' : 0, 'fri' : 0, 'sat' : 0, 'sun' : 0}
potato = {'mon' : 0, 'tue' : 0, 'wed' : 0, 'thu' : 0, 'fri' : 0, 'sat' : 0, 'sun' : 0}
vegan = {'mon' : 0, 'tue' : 0, 'wed' : 0, 'thu' : 0, 'fri' : 0, 'sat' : 0, 'sun' : 0}

# averages
bean_av = {}
migas_av = {}
potato_av = {}
vegan_av = {}

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

spreadsheet_name = input('Spreadsheet name: ')
if spreadsheet_name == '':
    spreadsheet_name = 'Test Data South 1st Waste Log'
how_many_sheets = input('How many weeks? ')
spreadsheet_name = spreadsheet_name.split(',')

try:
    how_many_sheets = int(how_many_sheets)
except:
    print('Enter a number')
    quit()
try:
    spreadsheet = client.open(spreadsheet_name[0])
except:
    print('Spreadsheet not found')
    quit()

print('=============')
i = 1
while i <= how_many_sheets :
    try:
        current_sheet = spreadsheet.get_worksheet(i) # Added 2 to skip template and non-conforming layout, changed for new spreadsheet
    except:
        print('Not that many sheets in spreadsheet, enter lower number') # Maybe don't need this try/except
        quit()                 # better way would be to standardize the number of weeks per spreadsheet then base try/except on that number
    if current_sheet == None : # works but not very efficient, runs calculations on all sheets before failing
        print('Not that many sheets in spreadsheet, enter lower number')
        quit()

    data = current_sheet.get_all_values()

    # print(current_sheet)

    strslice = str(current_sheet)
    slice = strslice[12:27]
    print('Week', i, ':', slice)

    # print(data)
    # print('sheet', i)

    # lists of rows as strings with blanks
    bean_row_str = current_sheet.row_values(3)
    migas_row_str = current_sheet.row_values(4)
    potato_row_str = current_sheet.row_values(5)
    vegan_row_str = current_sheet.row_values(6)

    # lists of rows as integers with zeros instead of blanks
    bean_row = []
    migas_row = []
    potato_row = []
    vegan_row = []

    blanks_to_zeros(bean_row_str, bean_row)
    blanks_to_zeros(migas_row_str, migas_row)
    blanks_to_zeros(potato_row_str, potato_row)
    blanks_to_zeros(vegan_row_str, vegan_row)

    add_days(bean, bean_row)
    add_days(migas, migas_row)
    add_days(potato, potato_row)
    add_days(vegan, vegan_row)

    i = i + 1

# print('bean', bean)
# print('migas', migas)
# print('potato', potato)
# print('vegan', vegan)

print('=========================')

total = 0 # Calculates total tacos wasted
for key, value in bean.items() :
    total = total + value
for key, value in migas.items() :
    total = total + value
for key, value in potato.items() :
    total = total + value
for key, value in vegan.items() :
    total = total + value

print('Total taco waste:', total)

print('=========================')
print('Averages:')
print('')

print('Bean - ')
days_average(bean, bean_av)
print('')
print('Migas - ')
days_average(migas, migas_av)
print('')
print('Potato - ')
days_average(potato, potato_av)
print('')
print('Vegan - ')
days_average(vegan, vegan_av)
print('')

# print(bean_av)
# print(migas_av)
# print(potato_av)
# print(vegan_av)
