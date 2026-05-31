from services.datagov import dataset_metadata


def test_dataset_metadata_includes_title_and_download_url():
    meta = dataset_metadata()
    assert meta["title"] == "2011-12 Early Childhood and Prekindergarten Enrollment Estimations Civil Rights Data Collection"
    assert meta["download_url"].startswith("https://")
