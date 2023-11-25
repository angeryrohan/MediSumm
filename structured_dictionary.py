#testing: 25/Nov/23 anusha
##get all parameters 
import xml.etree.ElementTree as ET

xml_file_path = 'XML Files/Harry_Styles_0056_ClinicalSummary.xml'
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