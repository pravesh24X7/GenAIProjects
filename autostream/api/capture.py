def mock_lead_capture(name: str, email: str, platform: str) -> str:
    """
    Sent the API call to backend server with details provided in the input parameters.
    """
    print(f"Lead captured sucessfully: {name}, {email}, {platform}")