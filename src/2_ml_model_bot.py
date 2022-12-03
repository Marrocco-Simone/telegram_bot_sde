from common.classes.classes import ResponseException
from common.methods.getResearchPapers import getResearchPapers
from common.methods.parseUpdate import UpdateInfo
from common.methods.sendTelegramMessage import sendTelegramMessage
from common.methods.startServer import startServerPolling
from common.methods.summarizeWithML import summarizeWithML


def parse_response(update_info: UpdateInfo):
    keyword = update_info['message']
    chat_id = update_info['chat_id']
    abstracts_text = ""

    sendTelegramMessage(chat_id, "Elaborating request...")

    try:
        response = getResearchPapers(keyword, 5, 0)
        if len(response['results']) == 0:
            sendTelegramMessage(
                chat_id, 'CoreAC was not able to find any result for ' + keyword)
        else:
            for paper in response['results']:
                return_msg = paper['abstract']
                sendTelegramMessage(chat_id, return_msg)
                # TODO 1: concatenate all abstracts in one string with \n as separator
                abstracts_text += paper['abstract'] + "\n"
    except Exception:
        return_msg = 'Error getting the research papers. Please retry later.'
        sendTelegramMessage(chat_id, return_msg)
        return

    # - summarize ----------------------------------------------------------------------------------------------------------

    # Sends a message to the user informing him that the summarization could take time
    return_msg = f"Summarizing the paper Abstracts, this can take some time..."
    sendTelegramMessage(chat_id, return_msg)

    try:
        # TODO 2: call summarizeWithML function, and send the summarized text with a message to the user
        hugging_face_obj = summarizeWithML(abstracts_text)
        return_msg = hugging_face_obj[0]['summary_text']
        sendTelegramMessage(chat_id, return_msg)
    except ResponseException as e:
        # Handles a Hugging Face exception occuring when the model is
        # loading on their servers.
        return_msg = f"Sorry, request failed at HuggingFace API. Reason: {e}"
        sendTelegramMessage(chat_id, return_msg)
        return
    except:
        # TODO 3: Handle the exceptions that could arise and inform the user with a message
        return_msg = "Sorry, request failed at HuggingFace API."
        sendTelegramMessage(chat_id, return_msg)


startServerPolling(parse_response)
