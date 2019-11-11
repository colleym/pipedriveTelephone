import json
import requests
import os
import phonenumbers

# Credentials
try:
  PDTOKEN=str(os.environ['PDTOKEN'])
except:
  print("Required Environment Variable(s) not defined")
  raise

def requestAllContacts():
  # Query Pipedrive for all Contacts
  START = 0
  BATCHSIZE = 500
  totalPeople = 0
  contactTmp = []
  
  # How many Contact?
  # pipedrive api only supports 500 objects each get request
  r = requests.get('https://api.pipedrive.com/v1/persons?start=0&limit=0&get_summary=1&api_token=' + PDTOKEN)
  
  if r.status_code != 200:
      raise ValueError(
          'Request to pipedrive returned an error %s, the response is:\n%s'
          % (r.status_code, r.text)
      )

  CONTACTCOUNT = r.json()
  totalPeople = CONTACTCOUNT['additional_data']['summary']['total_count']
  iterations = (totalPeople // 500) + 1

  i = 1

  while  i <= iterations:
    r = requests.get('https://api.pipedrive.com/v1/persons?start=' + str(START) + '&limit=' + str(BATCHSIZE) + '&api_token=' + PDTOKEN)
    
    if r.status_code != 200:
      raise ValueError(
          'Request to pipedrive returned an error %s, the response is:\n%s'
          % (r.status_code, r.text)
    )
    
    PDCONTACTS = r.json()

    # Combine batches into an Array
    for item in PDCONTACTS['data']:
      contactTmp.append(item.copy())
    
    # Count up
    i = i + 1
    START = START + BATCHSIZE

  return contactTmp


for contact in requestAllContacts():
    tmp_contact = {}
    tmp_contact['phone'] = []
    tmp_telefon = {}

    print ("User: " + contact['name'] + "(" + str(contact['id']) + ")")
    if contact['phone'][0]['value'] != "":
        for telefon in contact['phone']:
            try:
              tmp_telefon['label'] = str(telefon['label'])
              tmp_telefon['primary'] = str(telefon['primary'])
              pass
            except:
              # defaults
              tmp_telefon['label'] = "work"
              tmp_telefon['primary'] = "true"
              pass

            try:
                # For the internationalization of the telephone number we need the country to which the number belongs.
                # We had 99% german contacts therefore it was easy for me.
                t = phonenumbers.parse(telefon['value'], "DE")
                
                tmp_telefon['value'] = phonenumbers.format_number(t, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                tmp_contact['phone'].append(tmp_telefon.copy())

                print("Number [" + telefon['label'] + "] will be changed: " + str(telefon['value']) + " (old) | " + phonenumbers.format_number(t, phonenumbers.PhoneNumberFormat.INTERNATIONAL) + " (new)")
                pass
            except:
                print("Error in Number [" + telefon['label'] + "]: " + str(telefon['value']))
                pass

        if len(tmp_contact['phone']) > 0:
                
                header = {'Content-type': 'application/json'}
                p = requests.put ('https://api.pipedrive.com/v1/persons/' + str(contact['id']) + '?api_token=' + PDTOKEN, data=json.dumps(tmp_contact),  headers=header)
                
                if p.status_code != 200:
                    raise ValueError(
                        'Request to pipedrive returned an error %s, the response is:\n%s'
                        % (p.status_code, p.text)
                    )
                else:
                    print(f"Updated " + str(json.dumps(tmp_contact)))
    tmp_contact.clear()
    tmp_telefon.clear()