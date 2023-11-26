#!/bin/python
from flask import Flask, render_template
from structured_dictionary import all_extracted_info,dr_name, patient_name, parameters
from tabulate import tabulate
from summeriser import oms,tms,fms
app = Flask(__name__)


# Print the extracted information for all parameters
parameter_dic={}
all_info = all_extracted_info.items()
for name,info in all_info:
    if(str(info).replace(' ','') != ''):
        parameter_dic[name] = tabulate(info['Table Rows'], headers=info['Table Headers'], tablefmt='html')


#templating
@app.route('/')
def index():
    return render_template("index.html",duration=2, patient_name=patient_name, dr_name=dr_name, parameters=parameters, parameter_dic=parameter_dic, oms=oms,tms=tms,fms=fms)


app.run(host="0.0.0.0", port=4000)