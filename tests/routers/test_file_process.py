import pytest
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app, get_db
from app.models import File as UploadedFile
from io import StringIO

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    session = Session()

    app.dependency_overrides[get_db] = lambda: session

    yield session

    session.close()
    app.dependency_overrides.pop(get_db)


def test_get_files_returns_file_list(mock_db_session):
    files = [
        UploadedFile(filename="file1.csv", filetype="csv", uploaded_at="2022-01-01", user_id=1),
        UploadedFile(filename="file2.csv", filetype="csv", uploaded_at="2022-02-01", user_id=1),
    ]
    mock_db_session.add_all(files)
    mock_db_session.commit()

    response = client.get("/?id=1")

    assert response.status_code == 200

    expected_data = {
        "Uploaded files": [
            {
                "filename": "file1.csv",
                "filetype": "csv",
                "uploaded_at": "2022-01-01",
                "columns": None,
            },
            {
                "filename": "file2.csv",
                "filetype": "csv",
                "uploaded_at": "2022-02-01",
                "columns": None,
            },
        ]
    }
    assert response.json() == expected_data


def test_get_files_returns_404_when_no_files_exist(mock_db_session):
    response = client.get("/?id=1")
    assert response.status_code == 404




def test_get_filter_file_data_returns_filtered_data(mock_db_session):
    file = UploadedFile(id=1, filename="test.csv", filetype="csv", file_data="a,b,c\n1,2,3\n4,5,6\n")
    mock_db_session.add(file)
    mock_db_session.commit()

    response = client.get("/1/filter?user_id=1&columns=a,c&column_order_by=a&sort_type=ASC")

    assert response.status_code == 200

    expected_data = {"Filtered files": [["a", "c"], ["1", "3"], ["4", "6"]]}
    assert response.json() == expected_data


def test_get_filter_file_data_returns_404_when_file_not_found(mock_db_session):
    response = client.get("/1/filter?user_id=1&file_id=1")

    assert response.status_code == 404



@pytest.mark.asyncio
async def test_delete_file(client, db_session):
    file = UploadedFile(filename='test_file.csv', filetype='text/csv', user_id=1)
    db_session.add(file)
    db_session.commit()

    response = await client.delete('/1/delete', params={'file_id': file.id})

    assert response.status_code == status.HTTP_204_NO_CONTENT

    deleted_file = db_session.query(UploadedFile).filter(UploadedFile.id == file.id).first()
    assert deleted_file is None

    db_session.query(UploadedFile).delete()
    db_session.commit()
