"""
Borrowing this retry decorator from the nasbox smoketests.
"""
import time

from requests.exceptions import ConnectionError


def retry(reason, max_secs=300, wait_secs=1, falloff_factor=2):
    """
    Retry an .assert*() that is known to be eventually consistent.
    Retry will try immediately, then use exponential falloff while waiting
    for a test to become true.

    retry() is implemented as a function decorator, but it IMMEDIATELY EXECUTES
    the function it decorates. It's used to decorate a closure inside of a
    test function. (Because Python doesn't support anonymous code blocks).

    reason -- The reason why you are retrying. (ex: "Wait for X to finish.")
    max_secs -- the maximum number of seconds to retry.
    wait_secs -- the number of seconds to wait after the first try fails.
    falloff_factor -- How quickly to ramp up the wait time.

    Returns: A decorator that immediately executes its function and retries
    on errors.
    """

    if falloff_factor < 1:
        raise ValueError("falloff_factor must be >= 1")
    if wait_secs < 0:
        raise ValueError("wait_secs must be >= 0")

    def decorator(run_tests):
        start_time = time.time()

        def secs_elapsed():
            return time.time() - start_time

        def secs_remaining():
            return max_secs - secs_elapsed()

        # Use a local `wait` that we can assign to:
        wait = wait_secs
        while secs_remaining() > 0:
            try:
                return run_tests()
            except (AssertionError, ConnectionError) as error:
                print("Assertion or Connection error in retry():", error)
                print("Sleeping for", wait, "seconds before retrying because:", reason)
                time.sleep(wait)
                # Set how long we'll wait next time:
                wait = wait * falloff_factor
                wait = min(wait, secs_remaining())

        # We've exceeded our timeout.
        # Do one last attempt. Allow its exception to escape and fail the test:
        return run_tests()

    return decorator
