from deferred_result import *
import pytest
from threading import Timer


def test_timeout_waiting_for_result():
    r = DeferredResult[int]()

    with pytest.raises(TimeoutError):
        r.get(timeout=0.3)


def test_get_result_from_immediately_resolved():
    r = DeferredResult[int].resolved(12)

    assert r.get(0.3) == 12


def test_wait_for_result_from_background_thread():
    r = DeferredResult[int]()

    Timer(interval=0.2, function=lambda: r.resolve(12)).start()

    assert r.get(0.5) == 12


def test_fail_on_setting_result_on_immediately_resolved():
    r = DeferredResult.resolved(12)

    with pytest.raises(RuntimeError):
        r.resolve(13)

    assert r.get(0.5) == 12


def test_get_result_from_immediately_rejected():
    r = DeferredResult.rejected(ValueError('Invalid'))

    with pytest.raises(ValueError):
        r.get(0.3)


def test_wait_for_rejection_from_background_thread():
    r = DeferredResult[int]()

    Timer(interval=0.2, function=lambda: r.reject(ValueError('Invalid'))).start()

    with pytest.raises(ValueError):
        r.get(0.3)


def test_fail_on_setting_result_on_rejected():
    r = DeferredResult.rejected(ValueError())

    with pytest.raises(RuntimeError):
        r.resolve(13)


def test_fail_on_rejecting_rejected():
    r = DeferredResult.resolved(12)

    with pytest.raises(RuntimeError):
        r.reject(ValueError())

