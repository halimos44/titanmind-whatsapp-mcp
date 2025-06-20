import requests

from titan_mind.networking import print_request_and_response, get_titan_engage_url, \
    get_titan_engage_headers


def get_whatsapp_recent_conversations_from_titan_mind():
    # todo - add the filter to return only last 24 hour convos as only then we can send the free form messages to a phone number
    # or we can filter the convo by a phone number or we use an api on backend which can return if a phone number is in window or not
    try:
        response = requests.get(
            get_titan_engage_url(
                f"msg/conversations/?page=1&page_size=10&status=&created_before=&created_after=&last_message_before=&last_message_after="),
            headers=get_titan_engage_headers(),
        )
        print_request_and_response(response)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return {
            "status": True,
            "message": "conversations fetched",
            "result": response.json()["result"]["results"]
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


def send_whatsapp_message_to_a_conversation_from_titan_mind(conversation_id: str, message: str):
    try:
        response = requests.post(
            get_titan_engage_url(f"msg/conversations/{conversation_id}/messages/whatsapp/send-text/"),
            headers=get_titan_engage_headers(),
            json={
                "body": message
            }
        )
        print_request_and_response(response)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return {
            "status": True,
            "message": "message sent successfully",
            "result": response.json()
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
