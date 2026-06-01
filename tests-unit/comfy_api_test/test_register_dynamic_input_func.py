"""Backward-compat tests for ``register_dynamic_input_func``.

When ``live_input_types`` was added as a sixth argument to the dynamic-input
expansion callback, third-party custom nodes that registered against the
original 5-argument signature would otherwise crash with ``TypeError`` the
first time their input was expanded. ``register_dynamic_input_func`` wraps
such legacy callables transparently.
"""

from __future__ import annotations

from comfy_api.latest import _io


def test_legacy_5arg_callback_is_wrapped_transparently():
    received = {}

    def legacy(out_dict, live_inputs, value, input_type, curr_prefix):
        received["args"] = (out_dict, live_inputs, value, input_type, curr_prefix)

    io_type = "TEST_LEGACY_5ARG_V3"
    try:
        _io.register_dynamic_input_func(io_type, legacy)
        fn = _io.get_dynamic_input_func(io_type)

        # Caller invokes with 6 arguments (current signature). The shim must
        # strip the trailing live_input_types argument before delegating.
        fn({"required": {}}, {"a": 1}, ("X", {}), "required", ["p"], {"a": "INT"})

        assert received["args"] == (
            {"required": {}}, {"a": 1}, ("X", {}), "required", ["p"]
        )
    finally:
        _io.DYNAMIC_INPUT_LOOKUP.pop(io_type, None)


def test_new_6arg_callback_passes_live_input_types_through():
    received = {}

    def modern(out_dict, live_inputs, value, input_type, curr_prefix, live_input_types=None):
        received["live_input_types"] = live_input_types

    io_type = "TEST_MODERN_6ARG_V3"
    try:
        _io.register_dynamic_input_func(io_type, modern)
        fn = _io.get_dynamic_input_func(io_type)
        fn({}, {}, ("X", {}), "required", None, {"foo": "IMAGE"})
        assert received["live_input_types"] == {"foo": "IMAGE"}
    finally:
        _io.DYNAMIC_INPUT_LOOKUP.pop(io_type, None)


def test_callable_with_uninspectable_signature_assumed_modern():
    """``functools.partial`` and C builtins may have no introspectable signature.

    The shim must not blow up; falling back to the new signature is the safe
    choice (we get a clean TypeError if the callable really is too old, which
    is no worse than the pre-shim behavior).
    """
    calls = []

    class _CallableObj:
        # Lambdas / objects with __call__ are introspectable; partial with
        # opaque builtins are not. Simulate the latter by raising in __signature__.
        def __call__(self, *args, **kwargs):
            calls.append((args, kwargs))

        @property
        def __signature__(self):
            raise ValueError("uninspectable")

    io_type = "TEST_UNINSPECTABLE_V3"
    try:
        _io.register_dynamic_input_func(io_type, _CallableObj())
        fn = _io.get_dynamic_input_func(io_type)
        fn({}, {}, ("X", {}), "required", None, {"x": "INT"})
        assert calls and len(calls[0][0]) == 6
    finally:
        _io.DYNAMIC_INPUT_LOOKUP.pop(io_type, None)
