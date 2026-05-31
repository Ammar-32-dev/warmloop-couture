import os
import pytest

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

@pytest.fixture(autouse=True)
def seed_data(db):
    """
    Seed the database with Categories and Products before every test run.
    """
    from seed_db import seed_database
    seed_database()
