import uuid
import requests # type: ignore
from django.http import HttpResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore

@csrf_exempt
def ussd_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""

        steps = text.split("*")

        if text == "":
            # Main menu
            response = "CON Welcome to Open Space Management System\n"
            response += "1. Report a Problem\n"
            response += "2. Check Report Status\n"
            response += "3. Exit"

        elif steps[0] == "1":
            if len(steps) == 1:
                response = "CON Enter Open Space location or name:"
            elif len(steps) == 2:
                response = f"CON Enter a small description (optional) for the problem at {steps[1]}:"
            elif len(steps) == 3:
                response = f"CON Confirm Report:\n"
                response += f"Location: {steps[1]}\n"
                response += f"Description: {steps[2]}\n"
                response += f"1. Confirm\n"
                response += f"2. Cancel"
            elif len(steps) == 4 and steps[3] == "1":
                # User confirmed, now generate reference and submit to API
                open_space = steps[1]
                description = steps[2]
                reference_number = str(uuid.uuid4())[:8]

                payload = {
                    'reference_number': reference_number,
                    'phone_number': phone_number,
                    'open_space': open_space,
                    'description': description,
                    'status': 'Pending'
                }

                try:
                    openspace_url = 'http://127.0.0.1:8000/api/v1/ussd/'
                    res = requests.post(openspace_url, data=payload)
                    if res.status_code == 200:
                        print("Submitted successfully")
                    else:
                        print("Failed to submit:", res.status_code)
                except Exception as e:
                    print("Error submitting:", str(e))

                response = f"END Thank you! Your problem report has been submitted.\n"
                response += f"Reference Number: {reference_number}"
            elif len(steps) == 4 and steps[3] == "2":
                response = "END Report cancelled. Thank you."

        # elif steps[0] == "2":
        #     if len(steps) == 1:
        #         response = "CON Enter your Reference Number to check status:"
        #     elif len(steps) == 2:
        #         reference_number = steps[1]
        #         # Here you can query your DB for status (this is just a placeholder)
        #         response = f"END Report Status for {reference_number}:\nStatus: Pending"

        elif steps[0] == "2":
            if len(steps) == 1:
                response = "CON Enter your Reference Number to check status:"
            elif len(steps) == 2:
                reference_number = steps[1]
                try:
                    status_url = f'http://127.0.0.1:8000/api/v1/reference-ussd/{reference_number}/'
                    res = requests.get(status_url)
                    if res.status_code == 200:
                        data = res.json()
                        status = data.get('status', 'Unknown')
                        response = f"END Report Status for {reference_number}:\nStatus: {status}"
                    else:
                        response = f"END No report found with reference {reference_number}."
                except Exception as e:
                    print("Error:", str(e))
                    response = "END Error retrieving status. Please try again later."


        elif steps[0] == "3":
            response = "END Thank you for using Open Space Management System."

        return HttpResponse(response)
