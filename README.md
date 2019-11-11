 # Convert Pipedrive Telephone Numbers to internatinal standard
There was a problem calling contacts directly from the Pipedrive app. The root cause was a wrong phone number format.

Source: 02331 666777
Format needed: +49 2331 666 777

## Create a file to handover the Pipedrive API Access Token
```
#!/bin/bash
export PDTOKEN=XXXXXXXXXXXXXXXXX
python3 ./main.py
```

## Be Careful / main.py - Line 77 

For the internationalization of the telephone number we need the country to which the number belongs. In my case we only had german telephone numbers. Maybe you have to extend the programlogic, to figure out the country of the individual  contact. 

```
t = phonenumbers.parse(telefon['value'], "DE")
```



