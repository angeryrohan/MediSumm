#!/bin/python
from flask import Flask, render_template
from structured_dictionary import all_extracted_info,dr_name, patient_name, parameters
from tabulate import tabulate
app = Flask(__name__)


#summary functions
oms = "I've done the MBA"
tms = "Brock Purdy, a 45-year-old male patient seeks medical assistance due to ongoing struggles with Post-Traumatic Stress Disorder (PTSD) resulting from a traumatic incident several years ago. The patient encounters distressing flashbacks, hyperarousal, and avoidance behaviours. These symptoms have negatively impacted his personal relationships and work performance. Alongside PTSD, he has a past medical history of mild depression. The patient's current treatment plan includes Desvenlafaxine."
fms = "I've done the MBA, blah blah, The MBA was done by me. Pehle M, phir B phir A, MBA."

# Print the extracted information for all parameters
parameter_dic={}
all_info = all_extracted_info.items()
for name,info in all_info:
    if(str(info).replace(' ','') != ''):
        parameter_dic[name] = tabulate(info['Table Rows'], headers=info['Table Headers'], tablefmt='html')




#templating
@app.route('/')
def index():
    return render_template("index.html",duration=2,summary_text=tms, patient_name=patient_name, dr_name=dr_name, parameters=parameters, parameter_dic=parameter_dic)

@app.route('/one-minute')
def om():
    return render_template("index.html",duration=1, summary_text=oms, patient_name=patient_name, dr_name=dr_name, parameters=parameters)

@app.route('/two-minute')
def tm():
    return render_template("index.html",duration=2, summary_text=tms, patient_name=patient_name, dr_name=dr_name, parameters=parameters)

@app.route('/five-minute')
def fm():
    return render_template("index.html",duration=5, summary_text=fms, patient_name=patient_name, dr_name=dr_name, parameters=parameters)


app.run(host="0.0.0.0", port=8000)