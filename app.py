#!/bin/python
from flask import Flask, render_template
app = Flask(__name__)

#my functions
oms = "I've done the MBA"
tms = "I've done the MBA, blah blah, The MBA was done by me."
fms = "I've done the MBA, blah blah, The MBA was done by me. Pehle M, phir B phir A, MBA."


#get all parameters 
import xml.etree.ElementTree as ET

tree = ET.parse('data4.xml')
root = tree.getroot()

x = root.find("{urn:hl7-org:v3}component/{urn:hl7-org:v3}structuredBody")
parameters =[]
for i in x:
    parameters.append(i.find('{urn:hl7-org:v3}section/{urn:hl7-org:v3}title').text)

#getting the name of the patient
first_name = root.find("{urn:hl7-org:v3}recordTarget/{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}given").text
last_name = root.find("{urn:hl7-org:v3}recordTarget/{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}family").text
patient_name = first_name + " " + last_name
dr_first_name = root.find("{urn:hl7-org:v3}author/{urn:hl7-org:v3}assignedAuthor/{urn:hl7-org:v3}assignedPerson/{urn:hl7-org:v3}name/{urn:hl7-org:v3}given").text
dr_last_name = root.find("{urn:hl7-org:v3}author/{urn:hl7-org:v3}assignedAuthor/{urn:hl7-org:v3}assignedPerson/{urn:hl7-org:v3}name/{urn:hl7-org:v3}family").text
dr_name = dr_first_name + " " + dr_last_name

#function for getting details of each parameter






#templating
@app.route('/')
def index():
    return render_template("index.html",duration=2,summary_text=tms, patient_name=patient_name, dr_name=dr_name, parameters=parameters)

@app.route('/one-minute')
def om():
    return render_template("index.html",duration=1, summary_text=oms, patient_name=patient_name, dr_name=dr_name, parameters=parameters)

@app.route('/two-minute')
def tm():
    return render_template("index.html",duration=2, summary_text=tms, patient_name=patient_name, dr_name=dr_name, parameters=parameters)

@app.route('/five-minute')
def fm():
    return render_template("index.html",duration=5, summary_text=fms, patient_name=patient_name, dr_name=dr_name, parameters=parameters)


app.run(host="0.0.0.0", port=80)