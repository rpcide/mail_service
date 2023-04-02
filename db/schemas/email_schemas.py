def email_schema(email) -> dict:
    return {"email": email["email"]}

def email_list_schema(emails) -> list:
    return [email_schema(email) for email in emails]