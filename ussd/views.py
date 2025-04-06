# from django.views.decorators.csrf import csrf_exempt # type: ignore
# from django.http import HttpResponse # type: ignore
# import uuid

# # Simulating a database for problem reports
# problem_reports = {}

# @csrf_exempt
# def ussd_view(request):
#     if request.method == 'POST':
#         session_id = request.POST.get('sessionId')
#         service_code = request.POST.get('serviceCode')
#         phone_number = request.POST.get('phoneNumber')
#         text = request.POST.get('text')

#         response = ""

#         if text == "":
#             # Main Menu
#             response = "CON Welcome to Open Space Management System\n"
#             response += "1. Report a Problem\n"
#             response += "2. Check Report Status\n"
#             response += "3. Exit\n"
        
#         elif text == "1":
#             # Prompt for open space name
#             response = "CON Enter Open Space location or name:\n"

#         elif len(text.split("*")) == 2 and text.split("*")[0] == "1":
#             # Optional description
#             open_space = text.split("*")[1]
#             response = f"CON Enter a small description (optional) for the problem at {open_space}:\n"

#         elif len(text.split("*")) == 3 and text.split("*")[0] == "1":
#             # Confirmation
#             open_space = text.split("*")[1]
#             description = text.split("*")[2]
#             reference_number = str(uuid.uuid4())[:8]  # Generate a unique reference number
#             problem_reports[reference_number] = {
#                 "phone_number": phone_number,
#                 "open_space": open_space,
#                 "description": description,
#                 "status": "Pending"
#             }
#             response = f"CON Confirm Report:\n"
#             response += f"Problem at {open_space}\n"
#             response += f"Description: {description}\n"
#             response += f"1. Confirm\n"
#             response += f"2. Cancel\n"

#         elif len(text.split("*")) == 4 and text.split("*")[0] == "1" and text.split("*")[3] == "1":
#             # Submit report
#             reference_number = list(problem_reports.keys())[-1]  # Fetch last inserted reference number
#             response = f"END Thank you! Your problem report has been submitted.\n"
#             response += f"Reference Number: {reference_number}\n"

#         elif len(text.split("*")) == 2 and text.split("*")[0] == "2":
#             # Check Report Status
#             reference_number = text.split("*")[1]
#             if reference_number in problem_reports:
#                 report = problem_reports[reference_number]
#                 response = f"END Report Status:\n"
#                 response += f"Location: {report['open_space']}\n"
#                 response += f"Description: {report['description']}\n"
#                 response += f"Status: {report['status']}\n"
#             else:
#                 response = f"END No report found with Reference Number: {reference_number}\n"

#         elif text == "3":
#             # Exit
#             response = "END Thank you for using Open Space Management System.\n"

#         return HttpResponse(response)

#     return HttpResponse("END Error: Invalid request")


# In your USSD Django project (views.py)

import uuid
import requests  # Import requests to send HTTP requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def ussd_view(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""

        if text == "":
            # Main Menu
            response = "CON Welcome to Open Space Management System\n"
            response += "1. Report a Problem\n"
            response += "2. Check Report Status\n"
            response += "3. Exit\n"

        elif text == "1":
            # Prompt for open space name
            response = "CON Enter Open Space location or name:\n"

        elif len(text.split("*")) == 2 and text.split("*")[0] == "1":
            # Optional description
            open_space = text.split("*")[1]
            response = f"CON Enter a small description (optional) for the problem at {open_space}:\n"

        elif len(text.split("*")) == 3 and text.split("*")[0] == "1":
            # Confirmation
            open_space = text.split("*")[1]
            description = text.split("*")[2]
            reference_number = str(uuid.uuid4())[:8]  # Generate a unique reference number
            
            # Send the report data to OpenSpace API (for storage)
            openspace_url = 'http://127.0.0.1:8000/api/v1/ussd/'  # API URL in OpenSpace project
            payload = {
                'reference_number': reference_number,
                'phone_number': phone_number,
                'open_space': open_space,
                'description': description,
                'status': 'Pending'
            }

            try:
                # Make a POST request to the OpenSpace API to store the report
                response_from_openspace = requests.post(openspace_url, data=payload)
                if response_from_openspace.status_code == 200:
                    print('Data successfully submitted to OpenSpace')
                else:
                    print(f'Failed to submit to OpenSpace: {response_from_openspace.status_code}')
            except requests.exceptions.RequestException as e:
                print(f'Error during HTTP request: {e}')
            
            response = f"CON Confirm Report:\n"
            response += f"Problem at {open_space}\n"
            response += f"Description: {description}\n"
            response += f"1. Confirm\n"
            response += f"2. Cancel\n"

        elif len(text.split("*")) == 4 and text.split("*")[0] == "1" and text.split("*")[3] == "1":
            # Submit report
            reference_number = str(uuid.uuid4())[:8]  # Use the same reference number if needed
            response = f"END Thank you! Your problem report has been submitted.\n"
            response += f"Reference Number: {reference_number}\n"

        elif len(text.split("*")) == 2 and text.split("*")[0] == "2":
            # Check Report Status
            reference_number = text.split("*")[1]
            # This logic is for checking the status from the USSD, you can add additional logic if needed
            response = f"END Report Status:\n"
            response += f"Location: {open_space}\n"
            response += f"Description: {description}\n"
            response += f"Status: Pending\n"

        elif text == "3":
            # Exit
            response = "END Thank you for using Open Space Management System.\n"

        return HttpResponse(response)

    return HttpResponse("END Error: Invalid request")
