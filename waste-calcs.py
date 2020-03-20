# run calculations, run output, make files

import gspread
from oauth2client.service_account import ServiceAccountCredentials
def count_day(day) :
    count = 0
    for dic in data:
        if dic['day'] == day :
            count += 1
    return count

def each_days_total(day, which) :
    if dic['day'] == day:
        which[food] += dic[food]
    return which

def average(day, count) :
    for food in food_items :
        av = day[food] / count
        string = str(av)
        slice = string[:4]
        if len(slice) == 3 : # makes each output 4 characters
            slice = slice + '0'
        day[food] = slice
    return day

def output(full_weekday, day_dic) :
    print('  ' + full_weekday + ' - ')
    print('    ', end='')
    for k,v in day_dic.items() :
        print(k + ':', v, '| ', end='')
    print('\n')

# connect to google sheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


stores = ['test1', 'test2']

for store in stores :

    print('Running for:', store)

    name = store + ' food waste log'

    try :
        sheet = client.open(name).sheet1
    except :
        print('Problem opening spreadsheet')
        quit()

    # month/year for file names
    month_year = sheet.acell('A1').value

    raw_data = sheet.get_all_records(empty2zero=True, head=2)

    data = []
    index = -1 # keeps track of index to delete any accidental extra rows
    for dic in raw_data :
        index = index + 1

        try :
            dic.pop('number')
        except :
            print('Problem removing number column from dataset')
            quit()

        if '' in dic.keys() : # deletes accidental extra columns
            dic.pop('')

        if dic['day'] != 0 : # creates new dictionary without accidental extra rows
            data.append(dic)

    # error checks for non-numbers in dataset
    for dic in data :
        for key, value in dic.items() :
            if key != 'day' : # excludes key 'day'/weekday values from int(v)
                try :
                    value = int(value)
                except :
                    print('Spreadsheet values should be numbers only')
                    quit()

    #Calculations
    food_items = []

    sun = {}
    mon = {}
    tue = {}
    wed = {}
    thu = {}
    fri = {}
    sat = {}

    # gets food items in list
    for key,value in data[0].items() :
        food_items.append(key)
    food_items.pop(0)

    # sets up dictionaries for each day with correct food items set to zero
    for food in food_items :
        sun.update({food: 0})
        mon.update({food: 0})
        tue.update({food: 0})
        wed.update({food: 0})
        thu.update({food: 0})
        fri.update({food: 0})
        sat.update({food: 0})

    sun_count = count_day('sun')
    mon_count = count_day('mon')
    tue_count = count_day('tue')
    wed_count = count_day('wed')
    thu_count = count_day('thu')
    fri_count = count_day('fri')
    sat_count = count_day('sat')

    for food in food_items :
        for dic in data :
            each_days_total('sun', sun)
            each_days_total('mon', mon)
            each_days_total('tue', tue)
            each_days_total('wed', wed)
            each_days_total('thu', thu)
            each_days_total('fri', fri)
            each_days_total('sat', sat)

    average(sun, sun_count)
    average(mon, mon_count)
    average(tue, tue_count)
    average(wed, wed_count)
    average(thu, thu_count)
    average(fri, fri_count)
    average(sat, sat_count)

    # calculates total waste
    total_waste = 0
    for dic in data:
        for key,value in dic.items():
            try:
                num = int(value)
            except:
                continue
            total_waste = total_waste + num

    # outputs
    print('======================')
    print('Total Waste:', total_waste, 'items')
    print('======================')

    print('Averages: \n')
    output('Sunday', sun)
    output('Monday', mon)
    output('Tuesday', tue)
    output('Wednesday', wed)
    output('Thursday', thu)
    output('Friday', fri)
    output('Saturday', sat)

    # format ex. westlake_data_01-2020.txt
    data_file_name = store + '-files/' + store + '_data_' + month_year + '.txt'
    calcs_file_name = store + '-files/' + store + '_calcs_' + month_year + '.txt'

    # Create Files
    def calcs_for_f2(full_weekday, day_dic) :
        f_list3 = []
        counter = 0
        f_list3.append(full_weekday)
        f_list3.append(' - \n      ')
        for key, value in day_dic.items() :
            f_list3.append(key)
            f_list3.append(' : ')
            f_list3.append(value)
            f_list3.append(' | ')
            counter = counter + 1
            if counter == 5 :
                f_list3.append('\n      ')
                counter = 1
        f_list3.append('\n\n')
        f2.writelines(f_list3)

    f_list = []
    f1 = open(data_file_name, 'w+')
    count = 0
    for dic in data :
        for key,value in dic.items() :
            f_list.append(str(key))
            f_list.append(' : ')
            f_list.append(str(value))
            f_list.append(' | ')
            count = count + 1
            if count >= len(dic) :
                f_list.append('\n\n')
                count = 0

    f1.writelines(f_list)
    f1.close()

    f_list2 = []
    f2 = open(calcs_file_name, 'w+')

    f_list2.append('Total Waste: ')
    f_list2.append(str(total_waste))
    f_list2.append('\n\nAverages: \n\n  ')
    f2.writelines(f_list2)

    calcs_for_f2('Sunday', sun)
    calcs_for_f2('Monday', mon)
    calcs_for_f2('Tuesday', tue)
    calcs_for_f2('Wednesday', wed)
    calcs_for_f2('Thursday', thu)
    calcs_for_f2('Friday', fri)
    calcs_for_f2('Saturday', sat)

    f2.close()
