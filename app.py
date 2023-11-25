#!/bin/python
from flask import Flask, render_template
app = Flask(__name__)

#XML files
xml_file_path = 'Clifford_Burton_CHARM0031_ClinicalSummary.xml'

#my functions
oms = "I've done the MBA"
tms = "Brock Purdy, a 45-year-old male patient seeks medical assistance due to ongoing struggles with Post-Traumatic Stress Disorder (PTSD) resulting from a traumatic incident several years ago. The patient encounters distressing flashbacks, hyperarousal, and avoidance behaviours. These symptoms have negatively impacted his personal relationships and work performance. Alongside PTSD, he has a past medical history of mild depression. The patient's current treatment plan includes Desvenlafaxine."
fms = "I've done the MBA, blah blah, The MBA was done by me. Pehle M, phir B phir A, MBA."


#get all parameters 
import xml.etree.ElementTree as ET

tree = ET.parse(xml_file_path)
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
dr_name = "Dr. " +dr_first_name + " " + dr_last_name

#function for getting details of each parameter
from tabulate import tabulate
import xml.etree.ElementTree as ET

def extract_component_titles(xml_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Define namespaces
    ns = {'cda': 'urn:hl7-org:v3'}

    # Find all <component> elements
    components = root.findall(".//cda:component", namespaces=ns)

    # Extract titles from <title> elements within <component>
    titles = [component.find(".//cda:title", namespaces=ns).text.strip() if component.find(".//cda:title", namespaces=ns) is not None else None for component in components]

    return titles

def extract_information(xml_file_path, parameters):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Define namespaces
    ns = {'cda': 'urn:hl7-org:v3'}

    # Dictionary to store extracted information for each parameter
    extracted_data = {}

    for param in parameters:
        # Find all sections for the current parameter
        sections = root.findall(f".//cda:section[cda:title='{param['title']}']", namespaces=ns)
        for idx, section in enumerate(sections, start=1):
            title = section.find(".//cda:title", namespaces=ns).text
            text_elements = section.findall(".//cda:text", namespaces=ns)
            rows = []
            for text_element in text_elements:
                table_element = text_element.find(".//cda:table", namespaces=ns)
                if table_element is not None:
                    # Extract table headers (or infer from the first row)
                    headers = [th.text.strip() if th.text is not None else '' for th in table_element.findall(".//cda:th", namespaces=ns)]
                    if not headers:
                        # Infer headers from the first row if no explicit headers are present
                        first_row = table_element.find(".//cda:tr", namespaces=ns)
                        headers = [td.text.strip() if td.text is not None else '' for td in first_row.findall(".//cda:td", namespaces=ns)]

                    # Extract table rows
                    for tr in table_element.findall(".//cda:tr", namespaces=ns):
                        row_data = [td.text.strip() if td.text is not None else '' for td in tr.findall(".//cda:td", namespaces=ns)]
                        rows.append(row_data)

            # Store extracted information in the dictionary
            param_name = f"{param['name']}_{idx}" if len(sections) > 1 else param['name']
            extracted_data[param_name] = {
                'Title': title,
                'Table Headers': headers,
                'Table Rows': rows
            }

    return extracted_data

# Extract component titles from the XML file
component_titles = extract_component_titles(xml_file_path)

# Filter out None values from the list
component_titles = [title for title in component_titles if title is not None]

# Create parameters_list using the extracted titles
parameters_list = [{'name': title, 'title': title} for title in component_titles]

# Extract information for all parameters
all_extracted_info = extract_information(xml_file_path, parameters_list)

# Print the extracted information for all parameters
parameter_dic={}
all_info = all_extracted_info.items()
for name,info in all_info:
    print(name)
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