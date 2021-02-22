import openpyxl
from uuid import uuid4
from datetime import datetime

datenow = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

wb = openpyxl.load_workbook("base.xlsx")
ws = wb.active
data = list(ws.iter_rows(values_only=True, min_row=2, max_row=10))
# print(data)

def xmlformatter(r):
    sex = lambda x : 1 if x == 'М' else 2
    result = f"""<document>
    <document_id>{str(uuid4())}</document_id>
    <doc_date_time>{datenow}</doc_date_time>
    <citizen>
        <ext_citizen_id>{r[2]}</ext_citizen_id>
        <name>{r[4].title().replace(' ', '')}</name>
        <surname>{r[3].title().replace(' ', '')}</surname>
        <patronymic>{r[5].title().replace(' ', '')}</patronymic>
        <birthdate>{r[7]}</birthdate>
        <sex>{sex(r[6])}</sex>
        <citizenship>643</citizenship>
        <snils>{r[2]}</snils>
        <region>96000</region>
    </citizen>
    <benefits>
        <benefit>
        <benefit_code>1.00000.0217</benefit_code>
        <ext_benefit_code/>
        <diagnosis/>
        <receive_date>{r[8]}</receive_date>
        </benefit>
    </benefits>
</document>"""
    return result

output = ''
for r in data:
    output += xmlformatter(r) + '\n'

with open('output.xml', 'w') as f:
    f.write(output)