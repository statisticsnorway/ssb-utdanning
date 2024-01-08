import os


def pytest_sessionstart(session):
    """Called after the Session object has been created and before performing collection and entering the run test loop."""
    # Fake being in prodsone
    path = os.path.join(os.sep, "ssb", "bruker")
    os.makedirs(path, exist_ok=True)


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished, right before returning the exit status to the system."""
    # Fake being in prodsone cleanup
    ssb_path = os.path.join(os.sep, "ssb")
    path = os.path.join(ssb_path, "bruker")
    try:
        os.rmdir(path)
    except OSError:
        ...
    try:
        os.rmdir(ssb_path)
    except OSError:
        ...
