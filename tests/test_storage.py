import pytest

import os
import sys
import uuid

from storage.sqlite import SQLiteStorage


def test_initialization():
    file_path = f'./{str(uuid.uuid4())}'
    try:
        storage = SQLiteStorage(file_path)
        assert os.path.exists(file_path)
        storage.close()
        os.unlink(file_path)
    except:
        if storage is not None:
            storage.close()
        os.unlink(file_path)
        pytest.fail(f'Can\'t initialize sqlite database, reason: {sys.exc_info()[1]}')
