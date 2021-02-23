import openpyxl
from uuid import uuid4
from datetime import datetime

datenow = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
datesplit = lambda x : x.split(".")
dateinvers = lambda x : f"{x[2]}-{x[1]}-{x[0]}"

wb = openpyxl.load_workbook("base.xlsx")
ws = wb.active
data = list(ws.iter_rows(values_only=True, min_row=2))
# print(data)

def xmlformatter(r):
    sex = lambda x : 1 if x == 'М' else 2
    snils = r[2].replace('-', '').replace(' ', '')
    birth_date = dateinvers(datesplit(r[7]))

    if r[8] != None:
        receive_date = dateinvers(datesplit(r[8]))
    else:
        receive_date = birth_date

    if r[5] != None:
        patronymic = r[5].title().replace(' ', '')
    else:
        patronymic = ''
        
    result = f"""   <document>
        <document_id>{str(uuid4())}</document_id>
        <doc_date_time>{datenow}</doc_date_time>
        <citizen>
            <ext_citizen_id>{snils}</ext_citizen_id>
            <name>{r[4].title().replace(' ', '')}</name>
            <surname>{r[3].title().replace(' ', '')}</surname>
            <patronymic>{patronymic}</patronymic>
            <birthdate>{birth_date}</birthdate>
            <sex>{sex(r[6])}</sex>
            <citizenship>643</citizenship>
            <snils>{snils}</snils>
            <region>96000</region>
        </citizen>
        <benefits>
            <benefit>
            <benefit_code>1.00000.0076</benefit_code>
            <ext_benefit_code/>
            <diagnosis/>
            <receive_date>{receive_date}</receive_date>
            </benefit>
        </benefits>
        </document>"""
    return result

output = '<root>\n'

for r in data:
    output += xmlformatter(r) + '\n'
output += '</root>'

with open('output.xml', 'w') as f:
    f.write(output)