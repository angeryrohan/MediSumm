import openai
from testu import *
openai.api_key = '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'


problems = get_recent_problems(filled_information)
encounter_diagnosis = "Encounter Diagnosis: " + str(get_recent_EncounterDiagnosis(filled_information)[0])
medication_and_direction = "Medication: " + str(get_recent_medication(filled_information)[0])
reason_for_visit = "Reason for visit: " + str(get_recent_reason_for_visit(filled_information)[0])
treatment_and_plan = "Treatment Plan: " + str(get_recent_treatment_plan(filled_information)[0])
allergy_and_severity = "Allergy: " + str(get_recent_allergies(filled_information)[0])

#input2GPT = "I am a doctor and I have the following information. Problems: " + str(p1) + ". Encounter Diagnosis: " + str(ed1) + ". Medications and directions: " + str(med1) + ". " + str(dir1) + ". Reason for visit: " + str(rfv1) + ". Treatment Plan: " + str(tp1) + ". Allergies: " +  str(alg1) + ". Allergy severity: " + str(alg_severity) + ". I want you to summarize this in 100 words without loosing any major health information."
#print(input2GPT)

# function to create an array  

def compose_message(duration_in_minutes, *param):
    msg=""
    if(param == "none"):
        msg+=param
    final_msg = "I am a doctor and I have the following information." + msg + ". I want you to summarize this in " + str(duration_in_minutes*100) + " words without loosing any major health information."
    return final_msg
  

print(type(p1))
print(type(ed1))
print(type(med1))
print(type(med1))
print(type(rfv1))
print(type(tp1))
print(type(alg1))
print(type(alg_severity))

# output = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo", 
#   messages=[{"role": "user", "content": 
#     input2GPT}]
#   )

# outputGPT = output['choices'][0]['message']['content']