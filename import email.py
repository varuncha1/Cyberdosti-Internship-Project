import email
from email import policy
from email.parser import BytesParser

def parse_email_header(raw_email):
    headers = {}
    msg = BytesParser(policy=policy.default).parsebytes(raw_email)

    # Extract important headers
    headers['From'] = msg['From']
    headers['To'] = msg['To']
    headers['Subject'] = msg['Subject']
    headers['Date'] = msg['Date']
    headers['Message-ID'] = msg['Message-ID']
    headers['Received'] = msg.get_all('Received')

    return headers

def analyze_received_headers(received_headers):
    path = []
    for received in received_headers:
        parts = received.split(';')
        for part in parts:
            if 'by' in part.lower() and 'from' in part.lower():
                path.append(part.strip())

    return path

def print_headers(headers):
    print("Parsed Headers:")
    for key, value in headers.items():
        if key != 'Received':
            print(f"{key}: {value}")
    if 'Received' in headers:
        print("\nReceived Headers:")
        for received in headers['Received']:
            print(received)

# Sample raw email for testing (you need to provide your own raw email string)
raw_email = b"""\
From: sender@example.com
To: recipient@example.com
Subject: Test email
Date: Mon, 27 Jun 2024 10:00:00 +0000
Message-ID: <test-message-id@example.com>
Received: from mail.example.com (mail.example.com [192.0.2.1]) by recipient.example.com with ESMTP id 1234567890 for <recipient@example.com>; Mon, 27 Jun 2024 10:00:00 +0000
Received: from [192.0.2.2] (unknown [192.0.2.2]) by mail.example.com with ESMTP id abcdefg123456 for <sender@example.com>; Mon, 27 Jun 2024 09:55:00 +0000
"""

# Parse email headers
headers = parse_email_header(raw_email)
print_headers(headers)

# Analyze 'Received' headers
if 'Received' in headers:
    received_path = analyze_received_headers(headers['Received'])
    print("\nEmail Path:")
    for hop in received_path:
        print(hop)
