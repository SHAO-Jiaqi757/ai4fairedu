from translations import get_translation

def test_learning_view_translations():
    """Test that the translations for learning view are working correctly."""
    # Test difficulty levels
    assert get_translation('learning_view', 'standard', 'en') == 'Standard'
    assert get_translation('learning_view', 'standard', 'zh') == '标准'
    
    # Test learning types
    assert get_translation('learning_view', 'adhd', 'en') == 'ADHD'
    assert get_translation('learning_view', 'adhd', 'zh') == '注意力缺陷多动障碍'
    
    # Test support levels
    assert get_translation('learning_view', 'moderate', 'en') == 'Moderate'
    assert get_translation('learning_view', 'moderate', 'zh') == '中等'
    
    print("All learning view translations passed!")

if __name__ == "__main__":
    test_learning_view_translations() 