from core.generator import markdown_to_html

def test_markdown_to_html():
    test_cases = [
        ("**bold**", "<strong>bold</strong>"),
        ("__bold__", "<strong>bold</strong>"),
        ("*italic*", "<em>italic</em>"),
        ("_italic_", "<em>italic</em>"),
        ("Normal text with **bold** and *italic*.", "Normal text with <strong>bold</strong> and <em>italic</em>."),
        ("No markdown here", "No markdown here"),
        ("", ""),
        (None, None),
    ]
    
    for input_text, expected_output in test_cases:
        actual_output = markdown_to_html(input_text)
        print(f"Input: {input_text}")
        print(f"Expected: {expected_output}")
        print(f"Actual: {actual_output}")
        assert actual_output == expected_output
        print("MATCH!")
        print("-" * 20)

if __name__ == "__main__":
    try:
        test_markdown_to_html()
        print("\nSUCCESS: All test cases passed!")
    except AssertionError as e:
        print("\nFAILURE: Some test cases failed.")
        exit(1)
