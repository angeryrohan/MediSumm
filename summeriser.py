import openai
from recent_info import *

for x,y in filled_information.items():
    print(x)
#openai.api_key = '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'

def problems_summary(my_arr):
    problems_msg=""
    for problem, recent_date in my_arr:
        problems_msg+= " Problem: " + problem + "." + " date: " + recent_date + "."
    return problems_msg

def medications_and_directions_summary(my_arr):
    mnd_msg=""
    for med,direc,my_date in my_arr:
        mnd_msg+= " Medication: " + med + ". Direction: " + direc + ". Date: " + my_date
    return mnd_msg

def reason_for_visit_summary(my_arr):
    rfv_msg=""
    for rfv, date in my_arr:
        problems_msg+= " Reason for visit: " + rfv + "." + " date: " + date + "."
    return rfv_msg

def treatment_plan_summary(my_arr):
    tp_msg=""
    for tp, date in my_arr:
        problems_msg+= " Treatment Plan: " + tp + "." + " date: " + date + "."
    return tp_msg

def encounter_diagnosis_summary(my_arr):
    ed_msg=""
    for tp, date in my_arr:
        problems_msg+= " Encountered Diagnosis: " + ed + "." + " date: " + date + "."
    return ed_msg 

def allergies_summary(allergen, severity):
    allergy_msg =  "Allergy: " + allergen + "." + " Severity: " + severity + "."
    return allergy_msg


#problems = get_recent_problems(filled_information)
#encounter_diagnosis = "Encounter Diagnosis: " + str(get_recent_EncounterDiagnosis(filled_information)[0])
#medication_and_direction = "Medication: " + str(get_recent_medication(filled_information)[0])
#reason_for_visit = "Reason for visit: " + str(get_recent_reason_for_visit(filled_information)[0])
#treatment_and_plan = "Treatment Plan: " + str(get_recent_treatment_plan(filled_information)[0])
#allergy_and_severity = "Allergy: " + str(get_recent_allergies(filled_information)[0])

#input2GPT = "I am a doctor and I have the following information. Problems: " + str(p1) + ". Encounter Diagnosis: " + str(ed1) + ". Medications and directions: " + str(med1) + ". " + str(dir1) + ". Reason for visit: " + str(rfv1) + ". Treatment Plan: " + str(tp1) + ". Allergies: " +  str(alg1) + ". Allergy severity: " + str(alg_severity) + ". I want you to summarize this in 100 words without loosing any major health information."
#print(input2GPT)

# function to create an array  


def compose_message(duration_in_minutes, *param):
    msg=""
    if(param == "none"):
        msg+=param
    final_msg = "I am a doctor and I have the following information." + msg + ". I want you to summarize this in " + str(duration_in_minutes*100) + " words without loosing any major health information."
    return final_msg
  

# output = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo", 
#   messages=[{"role": "user", "content": 
#     input2GPT}]
#   )

# outputGPT = output['choices'][0]['message']['content']