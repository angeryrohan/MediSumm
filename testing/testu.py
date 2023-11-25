#!/bin/python
#XML files
from datetime import datetime
xml_file_path = 'Clifford_Burton_CHARM0031_ClinicalSummary.xml'


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

#for name,info in all_extracted_info.items():
#    if(str(info).replace(' ','') != ''):
#        if (len(info['Table Rows'])>0):
#            non_empty_parameters.append(name)

        #parameter_dic[name] = tabulate(info['Table Rows'], headers=info['Table Headers'], tablefmt='html')

# giving a name to all the items of all_extracted_information
all_info = all_extracted_info.items()

#function to get the most recent date in an array of dates


def get_most_recent_date(date_array):
    if not date_array:
        return None  # Handle empty array

    # Parse the first date as the initial reference
    most_recent_date = datetime.strptime(date_array[0], "%m/%d/%Y")

    # Iterate through the remaining dates
    for date_str in date_array[1:]:
        current_date = datetime.strptime(date_str, "%m/%d/%Y")
        if current_date > most_recent_date:
            most_recent_date = current_date

    return most_recent_date.strftime("%m/%d/%Y")

# get only the parameters which have non empty tables

def get_filled_information(all_info):
    filled_information = {}
    for name,info in all_info:
        if(str(info).replace(' ','') != ''):
            if (len(info['Table Rows'])>0):
                filled_information[name] = info
    return filled_information

filled_information = get_filled_information(all_info)
#print(filled_information)


# get the most recent problem in PROBLEMS parameter if that parameter has a non empty table
def get_recent_problems(dim, filled_information):
    for name,info in filled_information.items():
            if(name == 'PROBLEMS'):
                answer=[]
                problems = []
                dates = []
                # remove the first empty bracket
                problems_rows = filled_information['PROBLEMS']['Table Rows']
                problems_rows.pop(0)
                for row in problems_rows:
                    if(row[2] != ''):
                        problems.append(row[0].split(",")[0])
                        dates.append(row[2])
                match dim:
                    case 1:
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        return answer
                    case 2:
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        problems.pop(most_recent_index)
                        dates.pop(most_recent_index)
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        return answer
                    case 5:
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        problems.pop(most_recent_index)
                        dates.pop(most_recent_index)
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        problems.pop(most_recent_index)
                        dates.pop(most_recent_index)
                        most_recent_date = get_most_recent_date(dates)
                        most_recent_index = dates.index(str(most_recent_date))
                        answer.append((problems[most_recent_index],dates[most_recent_index]))
                        return answer
            else:
                pass
    return False

print(get_recent_problems(5,filled_information))



def get_recent_medication(filled_information):
    for name,info in filled_information.items():
        if(name == 'Medications/Supplements'):
            medications = []
            directions = []
            dates = []
            medication_rows = filled_information['Medications/Supplements']['Table Rows']
            medication_rows.pop(0)
            for row in medication_rows:
                if(row[3] != ''):
                    medications.append(row[0])
                    directions.append(row[1])
                    dates.append(row[3])
            most_recent_date = get_most_recent_date(dates)
            #print(dates)
            most_recent_index = most_recent_date.index(str(most_recent_date))
            #print(most_recent_index)
            return (medications[most_recent_index], directions[most_recent_index], dates[most_recent_index])
    else:
        return False
#print(get_recent_medication(filled_information))

def get_recent_reason_for_visit(filled_information):
    for name, info in filled_information.items():
        if(name == 'REASON FOR VISIT'):
            reasons=[]
            dates=[]
            reasons_rows = filled_information['REASON FOR VISIT']['Table Rows']
            reasons_rows.pop(0)
            for row in reasons_rows:
                if(row[0] != ''):
                    reasons.append(row[1])
                    dates.append(row[0])
            most_recent_date = get_most_recent_date(dates)
            most_recent_index = dates.index(str(most_recent_date))
            return (reasons[most_recent_index], dates[most_recent_index])

    else:
        return False

#print(get_recent_reason_for_visit(filled_information))

def get_recent_treatment_plan(filled_information):
    for name, info in filled_information.items():
        if(name == 'TREATMENT PLAN'):
            treatments=[]
            dates=[]
            treatments_rows = filled_information['TREATMENT PLAN']['Table Rows']
            treatments_rows.pop(0)
            for row in treatments_rows:
                if(row[0] != ''):
                    treatments.append(row[1])
                    dates.append(row[0])
            most_recent_date = get_most_recent_date(dates)
            most_recent_index = dates.index(str(most_recent_date))
            return (treatments[most_recent_index], dates[most_recent_index])

    else:
        return False

#print(get_recent_treatment_plan(filled_information))

def get_recent_EncounterDiagnosis(filled_information):
    for name,info in filled_information.items():
            if(name == 'Encounter Diagnosis'):
                EncounterDiagnosis = []
                dates = []
                # remove the first empty bracket
                EncounterDiagnosis_rows = filled_information['Encounter Diagnosis']['Table Rows']
                EncounterDiagnosis_rows.pop(0)
                for row in EncounterDiagnosis_rows:
                    if(row[2] != ''):
                        EncounterDiagnosis.append(row[0].split(',')[0])
                        dates.append(row[2])
                most_recent_date = get_most_recent_date(dates)
                most_recent_index = dates.index(str(most_recent_date))
                return(EncounterDiagnosis[most_recent_index ], dates[most_recent_index])
            else:
                pass
    return False 

#print(get_recent_EncounterDiagnosis(filled_information))

# def get_important_vital_signs(filled_information):
#     for name,info in filled_information.items():
#         if(name == 'VITAL SIGNS'):
#             neck_pain_avg=[]
#             neck_pain_rows = filled_information['VITAL SIGNS']['Table Rows']
#             neck_pain_rows.pop(0)
#             #for
# get_important_vital_signs(filled_information)

def most_serious_status(status_list):
    order = {'Mild': 0, 'Moderate': 1, 'Severe': 2}
    
    most_severe_status = None
    most_severe_index = float('-inf')  # Initialize with negative infinity
    
    for status in status_list:
        current_index = order.get(status, float('-inf'))
        if current_index > most_severe_index:
            most_severe_status = status
            most_severe_index = current_index
    
    return most_severe_status

def get_recent_allergies(filled_information):
    for name,info in filled_information.items():
        if(name == 'Allergies'):
            Allergies = []
            status = []
            allergies_rows = filled_information['Allergies']['Table Rows']
            allergies_rows.pop(0)
            for row in allergies_rows:
                if len(row)>=4:
                    Allergies.append(row[0])
                    status.append(row[3])
                else:
                    continue
            if status:  # Check if there are any statuses before finding the most severe
                Severity = most_serious_status(status)
                Severity_idx = status.index(Severity)
                return Allergies[Severity_idx], Severity
            else:
                return False  

    return False

#print(get_recent_allergies(filled_information))
