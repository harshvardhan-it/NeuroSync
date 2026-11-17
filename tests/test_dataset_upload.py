from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import UploadFile
from openpyxl import Workbook

from backend.routes import dataset as dataset_routes


def _xlsx_bytes():
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["Revenue", "Region"])
    worksheet.append([100, "North"])

    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


@pytest.mark.parametrize(
    ("filename", "contents"),
    [
        ("sales.csv", b"Revenue,Region\n100,North\n"),
        ("sales.xlsx", _xlsx_bytes()),
    ],
)
def test_upload_accepts_csv_and_xlsx(
    tmp_path,
    monkeypatch,
    filename,
    contents,
):
    captured = {}

    def analyze_dataframe(dataframe):
        captured["dataframe"] = dataframe.copy()
        return {"summary": "test analysis"}

    monkeypatch.setattr(dataset_routes, "UPLOAD_DIR", tmp_path)
    monkeypatch.setattr(dataset_routes, "analyze_dataframe", analyze_dataframe)

    session = Mock()
    session.refresh.side_effect = lambda dataset: setattr(dataset, "id", 123)

    upload = UploadFile(
        filename=filename,
        file=BytesIO(contents),
    )

    result = dataset_routes.upload_dataset(
        file=upload,
        current_user=SimpleNamespace(id=7),
        session=session,
    )

    dataframe = captured["dataframe"]
    assert result["success"] is True
    assert result["data"]["dataset_id"] == 123
    assert result["data"]["status"] == "completed"
    assert result["data"]["rows"] == 1
    assert result["data"]["columns"] == 2
    assert dataframe.columns.tolist() == ["Revenue", "Region"]
    assert dataframe.iloc[0]["Revenue"] == 100
    assert session.commit.call_count == 2

    stored_files = list(tmp_path.iterdir())
    assert len(stored_files) == 1
    assert stored_files[0].name != filename
