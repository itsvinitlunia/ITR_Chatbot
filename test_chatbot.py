import sys
import json
from chatbot_logic import process_chat_message, get_conversation_state

def run_conversation(test_title, user_inputs, chat_id="test_session"):
    print(f"\n{'='*60}")
    print(f"TEST: {test_title}")
    print('='*60)
    all_responses = []
    for idx, user_text in enumerate(user_inputs, 1):
        print(f"\n👤 User {idx}: {user_text}")
        bot_reply, options = process_chat_message(user_text, chat_id)
        print(f"🤖 Bot {idx}: {bot_reply}")
        if options:
            print(f"   Quick Options: {options}")
        all_responses.append({
            'message': user_text,
            'response': bot_reply,
            'quick_options': options
        })
        state = get_conversation_state(chat_id)
        print(f"   State: {state['step']}")
    return all_responses

def main():
    run_conversation("Basic Salaried ITR-1 Flow", [
        "start filing",
        "yes",
        "individual",
        "salary",
        "below 50 lakh",
        "only salary",
        "proceed with ITR-1",
        "new regime",
        "ABCDE1234F",
        "resident",
        "no exempt income",
        "salary details",
        "yes have form-16",
        "calculate tax",
        "no refund due",
        "complete filing",
        "download ITR-V",
        "aadhaar OTP",
        "done"
    ])

    run_conversation("Help Midway", [
        "start filing",
        "yes",
        "individual",
        "help",
        "salary",
        "below 50 lakh",
        "only salary"
    ])

    run_conversation("Restart Flow", [
        "start filing",
        "no",
        "continue anyway",
        "restart",
        "yes"
    ])

    run_conversation("Salary + Capital Gains (ITR-2)", [
        "start",
        "yes",
        "individual",
        "multiple sources",
        "salary + capital gains",
        "yes proceed",
        "old regime",
        "ABCDE1234F",
        "resident",
        "no exempt income",
        "salary details",
        "yes have form-16",
        "calculate tax",
        "yes tax payable",
        "pay online",
        "complete filing",
        "download",
        "net banking",
        "done"
    ])

if __name__ == "__main__":
    main()
