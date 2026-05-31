from app import create_app_shell


def test_create_app_shell_returns_title_and_tabs():
    shell = create_app_shell()
    assert shell["title"] == "Kindergarten Growth Journey"
    assert shell["tabs"] == ["Input", "Historical Snapshot", "Comparison"]
