import pytest
from services.chat_service import ChatService

def test_fallback_parse_email():
    service = ChatService()
    
    message = "Send photos to john@example.com"
    result = service._fallback_parse(message)
    
    assert result['intent'] == 'email'
    assert result['recipient'] == 'john@example.com'

def test_fallback_parse_whatsapp():
    service = ChatService()
    
    message = "Send via whatsapp to +1234567890"
    result = service._fallback_parse(message)
    
    assert result['intent'] == 'whatsapp'

def test_extract_parsed_data():
    service = ChatService()
    
    response = """INTENT: search
PERSON: John
DAYS_AGO: 30
RECIPIENT: none"""
    
    result = service._extract_parsed_data(response)
    
    assert result['intent'] == 'search'
    assert result['person'] == 'John'
    assert result['days_ago'] == 30
    assert result['recipient'] is None
