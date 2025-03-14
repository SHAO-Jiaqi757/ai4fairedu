from translations import get_translation

def test_translation():
    """Test that the get_translation function works correctly."""
    # Test a known translation
    assert get_translation('learning_view', 'unknown_date', 'en') == 'Unknown date'
    assert get_translation('learning_view', 'unknown_date', 'zh') == '未知日期'
    
    # Test a fallback to English
    assert get_translation('learning_view', 'unknown_date', 'fr') == 'Unknown date'
    
    # Test a non-existent key
    assert get_translation('learning_view', 'non_existent_key', 'en') == 'non_existent_key'
    
    print("All translation tests passed!")

if __name__ == "__main__":
    test_translation() 