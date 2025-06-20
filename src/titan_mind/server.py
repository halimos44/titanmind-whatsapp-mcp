from contextvars import ContextVar
from functools import wraps
from typing import Optional, Dict, Any, Callable

from fastmcp import FastMCP

from titan_mind.engage import \
    register_a_whatsapp_message_template_for_approval_to_send_first_message_to_a_phone_number_in_te, \
    get_is_the_whatsapp_message_template_approved_in_te, \
    send_a_whatsapp_message_to_a_phone_number_for_the_first_time_using_a_approved_whatsapp_message_template_in_te
from titan_mind.networking import set_titan_engage_token, set_titan_engage_business_code
from titan_mind.whatsapp import get_whatsapp_recent_conversations_from_titan_mind, \
    send_whatsapp_message_to_a_conversation_from_titan_mind
from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request as StarletteRequest

mcp = FastMCP("TitanMind Whatsapp MCP", stateless_http=True)


# mcp = FastMCP("TitanMind Whatsapp MCP")

def get_and_set_the_auth_token(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        request: StarletteRequest = get_http_request()
        auth_token = request.headers.get("auth-token")
        business_code = request.headers.get("bus-code")
        set_titan_engage_token(auth_token)
        set_titan_engage_business_code(business_code)

        return func(*args, **kwargs)

    return wrapper


@mcp.tool()
@get_and_set_the_auth_token
def get_whatsapp_recent_conversations_tool() -> Optional[Dict[str, Any]]:
    """
    gets the recent conversations in the titan messages's whatsapp channel

    Args:
    Returns:
        a boolean if the message was sent successfully against key "status"
        a string containing the message or error if the message was not sent successfully against the key "message"
        a List of conversations of whatsapp channel in TitanMind or error details against key "result"
    """
    return get_whatsapp_recent_conversations_from_titan_mind()


@mcp.tool()
@get_and_set_the_auth_token
def send_whatsapp_message_to_a_conversation(conversation_id: str, message: str) -> Optional[Dict[str, Any]]:
    """
    sends a whatsapp message to a phone number using TitanMind.

    Args:
        conversation_id (str): alphanumeric id of the whatsapp conversation, to which a message is required to be sent.
        message (str): the message to send.
    Returns:
        a boolean if the message was sent successfully against key "status"
        a string containing the message or error if the message was not sent successfully against the key "message"
        a dict with response details or error details against the key "result
    """

    return send_whatsapp_message_to_a_conversation_from_titan_mind(
        conversation_id, message
    )


messaging_on_whatsapp_channel_requirements_and_functionality_documentation = \
    """product Documentation: to send a message on whatsapp channel using TitanMind to a phone number for the very first time,
     Step 1: It is required that the message is first registered as a template and then approved. 
     Step 2: After the template is created, it takes some time for it to get approved. 
     Step 3: An Approved template can be used to send a message on whatsapp channel to a phone number for the very first time.
      """


@mcp.tool()
@get_and_set_the_auth_token
def register_msg_template_for_approval_to_send_first_time_to_number(
        template_name: str, message_content_components: list[dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    creates a new whatsapp message template, This is the step 1 of the description given next
    """ + messaging_on_whatsapp_channel_requirements_and_functionality_documentation + """
    Args:
        template_name (str): name of the whatsapp message template, It only accepts a word without no special characters only underscores
        message_content_components (dict): the message content that needs to be sent. It needs to be structured like the below example, 
        components are required to have BODY component for the very least like this: {"type": "BODY", "text": "lorem body text"}, BODY component is for the simple text.
        All other components are optional. message_content_components value will all type of components is mentioned below.
            [
                    {
    "type": "HEADER",
                        "format": "TEXT",
                        "text": "lorem header text"
                    },
                    {
    "type": "BODY",
                        "text": "lorem body text"
                    },
                    {
    "type": "FOOTER",
                        "text": "lorem footer text"
                    },
                    {
    "type": "BUTTONS",
                        "buttons": [
                            {
    "type": "QUICK_REPLY",
                                "text": "lorem reply bt"
                            }
                        ]
                    }
                ]
                
    Returns:
        a boolean if the template was sent successfully registered for approval against the key "status"
        a string containing the message or error if the function ran successfully against the key "message"
        a dict containing the registered template id and other details or error details against the key "result"
    """

    return register_a_whatsapp_message_template_for_approval_to_send_first_message_to_a_phone_number_in_te(
        template_name, message_content_components
    )


@mcp.tool()
@get_and_set_the_auth_token
def get_if_the_whatsapp_message_template_approved(
        template_name: str,
) -> Optional[Dict[str, Any]]:
    f"""
    checks if the whatsapp message template is approved and ready to be sent as a message to a phone number for the very first time,
    {messaging_on_whatsapp_channel_requirements_and_functionality_documentation}

    Args:
        template_name (str): name of the whatsapp message template, It only accepts a word without no special characters only underscores
                
    Returns:
        a boolean if the template is approved against the key "status"
        a string containing the message or error if the function ran successfully against the key "message"
        a dict containing the registered template and other details or error details against the key "result"
    """
    return get_is_the_whatsapp_message_template_approved_in_te(
        template_name
    )


@mcp.tool()
@get_and_set_the_auth_token
def send_message_to_a_number_for_first_time_using_approved_template(
        template_name: str, dialer_code: str, phone_without_dialer_code: str,
) -> Optional[Dict[str, Any]]:
    f"""
    sends a message to a phone number for the very first time using an approved whatsapp template,
    {messaging_on_whatsapp_channel_requirements_and_functionality_documentation}

    Args:
        template_name (str): name of the whatsapp message template, It only accepts a word without no special characters only underscores
        dialer_code (str): dialer code of the phone number
        phone_without_dialer_code (str): phone number without dialer code
                
    Returns:
        a dict containing of the details of the template sent or error details
    """
    return send_a_whatsapp_message_to_a_phone_number_for_the_first_time_using_a_approved_whatsapp_message_template_in_te(
        template_name, dialer_code, phone_without_dialer_code
    )


def main():
    # mcp.run()
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8010)


if __name__ == "__main__":
    main()
