from structured_dictionary import *
from app import all_info
from datetime import datetime

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

# function to get only the parameters which have non empty tables

def get_filled_information(all_info):
    filled_information = {}
    for name,info in all_info:
        if(str(info).replace(' ','') != ''):
            if (len(info['Table Rows'])>0):
                filled_information[name] = info
    return filled_information

filled_information = get_filled_information(all_info)
#print(filled_information)


# function to get the most recent problem in PROBLEMS parameter if that parameter has a non empty table
def get_recent_problems(dim, filled_information):
    answer=[]
    problems = []
    dates = []
    if('PROBLEMS' in filled_information):
        problems_rows = filled_information['PROBLEMS']['Table Rows']
        # remove the first empty bracket
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
                if(len(dates) != 0):
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
                if(len(dates) != 0):
                    most_recent_date = get_most_recent_date(dates)
                    most_recent_index = dates.index(str(most_recent_date))
                    answer.append((problems[most_recent_index],dates[most_recent_index]))
                    problems.pop(most_recent_index)
                    dates.pop(most_recent_index)
                if(len(dates) != 0):    
                    most_recent_date = get_most_recent_date(dates)
                    most_recent_index = dates.index(str(most_recent_date))
                    answer.append((problems[most_recent_index],dates[most_recent_index]))
                return answer
    else:
        return False


#print(get_recent_problems(5,filled_information))



def get_recent_medication(filled_information):
    medications = []
    directions = []
    dates = []
    if('Medications/Supplements' in filled_information):
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

print(get_recent_medication(filled_information))

def get_recent_reason_for_visit(filled_information):
    reasons=[]
    dates=[]
    if('REASON FOR VISIT' in filled_information):
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

print(get_recent_reason_for_visit(filled_information))

def get_recent_treatment_plan(filled_information):

    treatments=[]
    dates=[]
    if('TREATMENT PLAN' in filled_information):
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

print(get_recent_treatment_plan(filled_information))

def get_recent_EncounterDiagnosis(dim,filled_information):
    answer=[]
    EncounterDiagnosis = []
    dates = []
    # remove the first empty bracket
    if('Encounter Diagnosis' in filled_information):
        EncounterDiagnosis_rows = filled_information['Encounter Diagnosis']['Table Rows']
        EncounterDiagnosis_rows.pop(0)
        for row in EncounterDiagnosis_rows:
            if(row[2] != ''):
                EncounterDiagnosis.append(row[0].split(',')[0])
                dates.append(row[2])
        match dim:
            case 1:
                most_recent_date = get_most_recent_date(dates)
                most_recent_index = dates.index(str(most_recent_date))
                answer.append((EncounterDiagnosis[most_recent_index ], dates[most_recent_index]))
                return answer
            case 2: 
                most_recent_date = get_most_recent_date(dates)
                most_recent_index = dates.index(str(most_recent_date))
                answer.append((EncounterDiagnosis[most_recent_index ], dates[most_recent_index]))
                EncounterDiagnosis.pop(most_recent_index)
                dates.pop(most_recent_index)
                most_recent_date = get_most_recent_date(dates)
                most_recent_index = dates.index(str(most_recent_date))
                answer.append((EncounterDiagnosis[most_recent_index ], dates[most_recent_index]))
                return answer
            case 5:
                most_recent_date = get_most_recent_date(dates)
                most_recent_index = dates.index(str(most_recent_date))
                answer.append((EncounterDiagnosis[most_recent_index ], dates[most_recent_index]))
                EncounterDiagnosis.pop(most_recent_index)
                dates.pop(most_recent_index)
                most_recent_date = get_most_recent_date(dates)
                most_recent_index = dates.index(str(most_recent_date))
                answer.append((EncounterDiagnosis[most_recent_index ], dates[most_recent_index]))
                EncounterDiagnosis.pop(most_recent_index)
                dates.pop(most_recent_index)
                most_recent_date = get_most_recent_date(dates)
                most_recent_index = dates.index(str(most_recent_date))
                answer.append((EncounterDiagnosis[most_recent_index ], dates[most_recent_index]))
                return answer
    else:
        return False



print(get_recent_EncounterDiagnosis(5,filled_information))


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
    Allergies = []
    status = []
    if('Allergies' in filled_information):
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


print(get_recent_allergies(filled_information))
