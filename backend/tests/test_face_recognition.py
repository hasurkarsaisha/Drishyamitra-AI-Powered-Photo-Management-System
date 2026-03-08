import pytest
import numpy as np
from services.face_recognition import FaceRecognitionService

def test_cosine_distance():
    service = FaceRecognitionService()
    
    emb1 = np.array([1, 0, 0, 0])
    emb2 = np.array([1, 0, 0, 0])
    
    distance = service._cosine_distance(emb1, emb2)
    assert distance < 0.01
    
    emb3 = np.array([0, 1, 0, 0])
    distance2 = service._cosine_distance(emb1, emb3)
    assert distance2 > 0.9

def test_find_matching_person_no_match():
    service = FaceRecognitionService()
    
    embedding = np.random.rand(512)
    result = service.find_matching_person(embedding, user_id=1)
    
    assert result is None
