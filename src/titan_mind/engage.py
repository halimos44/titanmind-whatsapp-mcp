from typing import Any

import requests

from titan_mind.networking import get_titan_engage_url, \
    print_request_and_response, get_titan_engage_headers


def register_a_whatsapp_message_template_for_approval_to_send_first_message_to_a_phone_number_in_te(
        template_name: str, message_content_components: list[dict[str, Any]]
):
    try:
        response = requests.post(
            get_titan_engage_url(
                f"whatsapp/template/"),
            headers=get_titan_engage_headers(),
            json={
                "name": template_name,
                "language": "en",
                "category": "MARKETING",
                "components": message_content_components
            }
        )
        print_request_and_response(response)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return {
            "status": True,
            "message": "conversations fetched",
            "result": response.json()["result"]
        }
    except Exception as e:
        error_json = {}
        if response is not None and response.json() is not None:
            error_json = response.json()
        return {
            "status": False,
            "message": f"{e}",
            "result": error_json
        }


def get_is_the_whatsapp_message_template_approved_in_te(
        template_name: str
):
    try:
        response = requests.get(
            get_titan_engage_url(
                f"template/?channel=whatsapp&name__icontains={template_name}"),
            headers=get_titan_engage_headers(),
        )
        print_request_and_response(response)
        response.raise_for_status()

        templates = response.json()["result"]["results"]
        if len(templates) == 0:
            return {
                "status": False,
                "message": "template not found",
                # "result": response.json()["result"]
            }

        template = templates[0]

        return {
            "status": True if template["status"] == "approved" else False,
            "message": "template fetched",
            "result": template
        }
    except Exception as e:
        error_json = {}
        if response is not None and response.json() is not None:
            error_json = response.json()
        return {
            "status": False,
            "message": f"{e}",
            "result": error_json
        }


def send_a_whatsapp_message_to_a_phone_number_for_the_first_time_using_a_approved_whatsapp_message_template_in_te(
        template_name: str,
        dialer_code: str,
        phone_without_dialer_code: str,
):
    try:
        template_details = get_is_the_whatsapp_message_template_approved_in_te(
            template_name=template_name,
        )
        if not template_details["status"]:
            return template_details

        response = requests.post(
            get_titan_engage_url(
                f"whatsapp/message/send-template/"),
            headers=get_titan_engage_headers(),
            json={
                "recipients": [
                    {
                        "country_code_alpha": "IN",
                        "country_code": dialer_code,
                        "phone_without_country_code": phone_without_dialer_code
                    }
                ],
                "template": template_details["result"]["id"],
            }
        )
        print_request_and_response(response)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        return response.json()
    except Exception as e:
        error_json = {}
        if response is not None and response.json() is not None:
            error_json = response.json()
        return {
            "status": False,
            "message": f"{e}",
            "result": error_json
        }
