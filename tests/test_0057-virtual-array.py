# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import json

try:
    # pybind11 only supports cPickle protocol 2+ (-1 in pickle.dumps)
    # (automatically satisfied in Python 3; this is just to keep testing Python 2.7)
    import cPickle as pickle
except ImportError:
    import pickle

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test_forms():
    form = ak.forms.NumpyForm([], 8, "d")
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert form.inner_shape == []
    assert form.itemsize == 8
    assert form.primitive == "float64"
    assert form.has_identities == False
    assert form.parameters == {}
    assert form.form_key is None
    assert json.loads(form.tojson(False, True)) == {
        "class": "NumpyArray",
        "inner_shape": [],
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
        "has_identities": False,
        "parameters": {},
        "form_key": None,
    }
    assert json.loads(str(form)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }

    form = ak.forms.NumpyForm(
        [1, 2, 3],
        8,
        "d",
        has_identities=True,
        parameters={"hey": ["you", {"there": 3}]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert form.inner_shape == [1, 2, 3]
    assert form.itemsize == 8
    assert form.primitive == "float64"
    assert form.has_identities == True
    assert form.parameters == {"hey": ["you", {"there": 3}]}
    assert form.parameter("hey") == ["you", {"there": 3}]
    assert form.form_key == "yowzers"
    assert json.loads(form.tojson(False, True)) == {
        "class": "NumpyArray",
        "inner_shape": [1, 2, 3],
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
        "has_identities": True,
        "parameters": {"hey": ["you", {"there": 3}]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "NumpyArray",
        "inner_shape": [1, 2, 3],
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
        "has_identities": True,
        "parameters": {"hey": ["you", {"there": 3}]},
        "form_key": "yowzers",
    }

    form = ak.forms.BitMaskedForm(
        "i8",
        ak.forms.NumpyForm([], 8, "d"),
        True,
        False,
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "BitMaskedArray",
        "mask": "i8",
        "content": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "valid_when": True,
        "lsb_order": False,
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "BitMaskedArray",
        "mask": "i8",
        "content": "float64",
        "valid_when": True,
        "lsb_order": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert form.mask == "i8"
    assert json.loads(str(form.content)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert form.valid_when == True
    assert form.lsb_order == False
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.ByteMaskedForm(
        "i8",
        ak.forms.NumpyForm([], 8, "d"),
        True,
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "ByteMaskedArray",
        "mask": "i8",
        "content": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "valid_when": True,
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "ByteMaskedArray",
        "mask": "i8",
        "content": "float64",
        "valid_when": True,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert form.mask == "i8"
    assert json.loads(str(form.content)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert form.valid_when == True
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.EmptyForm(parameters={"hey": ["you"]}, form_key="yowzers")
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "EmptyArray",
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "EmptyArray",
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.IndexedForm(
        "i64",
        ak.forms.NumpyForm([], 8, "d"),
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "IndexedArray64",
        "index": "i64",
        "content": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "IndexedArray64",
        "index": "i64",
        "content": "float64",
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert form.index == "i64"
    assert json.loads(str(form.content)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.IndexedOptionForm(
        "i64",
        ak.forms.NumpyForm([], 8, "d"),
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "IndexedOptionArray64",
        "index": "i64",
        "content": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "IndexedOptionArray64",
        "index": "i64",
        "content": "float64",
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert form.index == "i64"
    assert json.loads(str(form.content)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.ListForm(
        "i64",
        "i64",
        ak.forms.NumpyForm([], 8, "d"),
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "ListArray64",
        "starts": "i64",
        "stops": "i64",
        "content": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "ListArray64",
        "starts": "i64",
        "stops": "i64",
        "content": "float64",
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert form.starts == "i64"
    assert form.stops == "i64"
    assert json.loads(str(form.content)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.ListOffsetForm(
        "i64",
        ak.forms.NumpyForm([], 8, "d"),
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "ListOffsetArray64",
        "offsets": "i64",
        "content": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "ListOffsetArray64",
        "offsets": "i64",
        "content": "float64",
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert form.offsets == "i64"
    assert json.loads(str(form.content)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.RecordForm(
        {"one": ak.forms.NumpyForm([], 8, "d"), "two": ak.forms.NumpyForm([], 1, "?")},
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "RecordArray",
        "contents": {
            "one": {
                "class": "NumpyArray",
                "inner_shape": [],
                "itemsize": 8,
                "format": "d",
                "primitive": "float64",
                "has_identities": False,
                "parameters": {},
                "form_key": None,
            },
            "two": {
                "class": "NumpyArray",
                "inner_shape": [],
                "itemsize": 1,
                "format": "?",
                "primitive": "bool",
                "has_identities": False,
                "parameters": {},
                "form_key": None,
            },
        },
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "RecordArray",
        "contents": {"one": "float64", "two": "bool"},
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    if not ak._util.py27 and not ak._util.py35:
        assert [json.loads(str(x)) for x in form.values()] == [
            {
                "class": "NumpyArray",
                "itemsize": 8,
                "format": "d",
                "primitive": "float64",
            },
            {"class": "NumpyArray", "itemsize": 1, "format": "?", "primitive": "bool"},
        ]
        assert {n: json.loads(str(x)) for n, x in form.contents.items()} == {
            "one": {
                "class": "NumpyArray",
                "itemsize": 8,
                "format": "d",
                "primitive": "float64",
            },
            "two": {
                "class": "NumpyArray",
                "itemsize": 1,
                "format": "?",
                "primitive": "bool",
            },
        }
    assert json.loads(str(form.content("one"))) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert json.loads(str(form.content("two"))) == {
        "class": "NumpyArray",
        "itemsize": 1,
        "format": "?",
        "primitive": "bool",
    }
    if not ak._util.py27 and not ak._util.py35:
        assert json.loads(str(form.content(0))) == {
            "class": "NumpyArray",
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
        }
        assert json.loads(str(form.content(1))) == {
            "class": "NumpyArray",
            "itemsize": 1,
            "format": "?",
            "primitive": "bool",
        }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.RecordForm(
        [ak.forms.NumpyForm([], 8, "d"), ak.forms.NumpyForm([], 1, "?")],
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "RecordArray",
        "contents": [
            {
                "class": "NumpyArray",
                "inner_shape": [],
                "itemsize": 8,
                "format": "d",
                "primitive": "float64",
                "has_identities": False,
                "parameters": {},
                "form_key": None,
            },
            {
                "class": "NumpyArray",
                "inner_shape": [],
                "itemsize": 1,
                "format": "?",
                "primitive": "bool",
                "has_identities": False,
                "parameters": {},
                "form_key": None,
            },
        ],
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "RecordArray",
        "contents": ["float64", "bool"],
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert [json.loads(str(x)) for x in form.values()] == [
        {"class": "NumpyArray", "itemsize": 8, "format": "d", "primitive": "float64"},
        {"class": "NumpyArray", "itemsize": 1, "format": "?", "primitive": "bool"},
    ]
    assert {n: json.loads(str(x)) for n, x in form.contents.items()} == {
        "0": {
            "class": "NumpyArray",
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
        },
        "1": {"class": "NumpyArray", "itemsize": 1, "format": "?", "primitive": "bool"},
    }
    assert json.loads(str(form.content(0))) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert json.loads(str(form.content(1))) == {
        "class": "NumpyArray",
        "itemsize": 1,
        "format": "?",
        "primitive": "bool",
    }
    assert json.loads(str(form.content("0"))) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert json.loads(str(form.content("1"))) == {
        "class": "NumpyArray",
        "itemsize": 1,
        "format": "?",
        "primitive": "bool",
    }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.RegularForm(
        ak.forms.NumpyForm([], 8, "d"),
        10,
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "RegularArray",
        "content": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "size": 10,
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "RegularArray",
        "content": "float64",
        "size": 10,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form.content)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert form.size == 10
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.UnionForm(
        "i8",
        "i64",
        [ak.forms.NumpyForm([], 8, "d"), ak.forms.NumpyForm([], 1, "?")],
        parameters={"hey": ["you"]},
        form_key="yowzers",
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "UnionArray8_64",
        "tags": "i8",
        "index": "i64",
        "contents": [
            {
                "class": "NumpyArray",
                "inner_shape": [],
                "itemsize": 8,
                "format": "d",
                "primitive": "float64",
                "has_identities": False,
                "parameters": {},
                "form_key": None,
            },
            {
                "class": "NumpyArray",
                "inner_shape": [],
                "itemsize": 1,
                "format": "?",
                "primitive": "bool",
                "has_identities": False,
                "parameters": {},
                "form_key": None,
            },
        ],
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "UnionArray8_64",
        "tags": "i8",
        "index": "i64",
        "contents": ["float64", "bool"],
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert form.tags == "i8"
    assert form.index == "i64"
    assert json.loads(str(form.contents)) == [
        {"class": "NumpyArray", "itemsize": 8, "format": "d", "primitive": "float64"},
        {"class": "NumpyArray", "itemsize": 1, "format": "?", "primitive": "bool"},
    ]
    assert json.loads(str(form.content(0))) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert json.loads(str(form.content(1))) == {
        "class": "NumpyArray",
        "itemsize": 1,
        "format": "?",
        "primitive": "bool",
    }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.UnmaskedForm(
        ak.forms.NumpyForm([], 8, "d"), parameters={"hey": ["you"]}, form_key="yowzers"
    )
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert json.loads(form.tojson(False, True)) == {
        "class": "UnmaskedArray",
        "content": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identities": False,
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form)) == {
        "class": "UnmaskedArray",
        "content": "float64",
        "parameters": {"hey": ["you"]},
        "form_key": "yowzers",
    }
    assert json.loads(str(form.content)) == {
        "class": "NumpyArray",
        "itemsize": 8,
        "format": "d",
        "primitive": "float64",
    }
    assert form.has_identities == False
    assert form.parameters == {"hey": ["you"]}
    assert form.parameter("hey") == ["you"]
    assert form.form_key == "yowzers"

    form = ak.forms.VirtualForm(ak.forms.NumpyForm([], 8, "d"), True)
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert form.form.inner_shape == []
    assert form.form.itemsize == 8
    assert form.form.primitive == "float64"
    assert form.form.has_identities == False
    assert form.form.parameters == {}
    assert form.has_length is True
    assert form.parameters == {}
    assert json.loads(form.tojson(False, True)) == {
        "class": "VirtualArray",
        "form": {
            "class": "NumpyArray",
            "inner_shape": [],
            "itemsize": 8,
            "format": "d",
            "primitive": "float64",
            "has_identities": False,
            "parameters": {},
            "form_key": None,
        },
        "has_length": True,
        "has_identities": False,
        "parameters": {},
        "form_key": None,
    }
    assert json.loads(str(form)) == {
        "class": "VirtualArray",
        "form": "float64",
        "has_length": True,
    }

    form = ak.forms.VirtualForm(None, False)
    assert form == form
    assert pickle.loads(pickle.dumps(form, -1)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, False)) == form
    assert ak.forms.Form.fromjson(form.tojson(False, True)) == form
    assert form.form is None
    assert form.has_length is False
    assert form.parameters == {}
    assert json.loads(form.tojson(False, True)) == {
        "class": "VirtualArray",
        "form": None,
        "has_length": False,
        "has_identities": False,
        "parameters": {},
        "form_key": None,
    }
    assert json.loads(str(form)) == {
        "class": "VirtualArray",
        "form": None,
        "has_length": False,
    }


def fcn():
    return ak.layout.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5]))


def test_basic():
    generator = ak.layout.ArrayGenerator(
        fcn, form=ak.forms.NumpyForm([], 8, "d"), length=5
    )

    d = ak._util.MappingProxy({})
    cache = ak.layout.ArrayCache(d)

    virtualarray = ak.layout.VirtualArray(generator, cache)
    assert virtualarray.peek_array is None
    assert virtualarray.array is not None
    assert ak.to_list(virtualarray.peek_array) == [1.1, 2.2, 3.3, 4.4, 5.5]
    assert ak.to_list(virtualarray.array) == [1.1, 2.2, 3.3, 4.4, 5.5]
    assert ak.to_list(d[virtualarray.cache_key]) == [1.1, 2.2, 3.3, 4.4, 5.5]

    cache = ak.layout.ArrayCache(None)

    virtualarray = ak.layout.VirtualArray(generator, cache)
    assert virtualarray.peek_array is None
    assert virtualarray.array is not None
    assert virtualarray.peek_array is None
    assert ak.to_list(virtualarray.array) == [1.1, 2.2, 3.3, 4.4, 5.5]


def test_slice():
    generator = ak.layout.ArrayGenerator(
        lambda: ak.Array(
            [[1.1, 2.2, 3.3, 4.4, 5.5], [6.6, 7.7, 8.8], [100, 200, 300, 400]]
        ),
        length=3,
    )
    virtualarray = ak.layout.VirtualArray(generator)

    assert isinstance(virtualarray, ak.layout.VirtualArray)

    sliced = virtualarray[:-1]

    assert isinstance(sliced, ak.layout.VirtualArray)

    assert isinstance(sliced[1], ak.layout.NumpyArray)


def test_field():
    generator = ak.layout.ArrayGenerator(
        lambda: ak.Array(
            [
                {"x": 0.0, "y": []},
                {"x": 1.1, "y": [1]},
                {"x": 2.2, "y": [2, 2]},
                {"x": 3.3, "y": [3, 3, 3]},
            ]
        )
    )
    virtualarray = ak.layout.VirtualArray(generator)

    assert isinstance(virtualarray, ak.layout.VirtualArray)

    sliced = virtualarray["y"]
    assert isinstance(sliced, ak.layout.VirtualArray)

    assert isinstance(sliced[1], ak.layout.NumpyArray)


def test_single_level():
    template = ak.Array(
        [
            [{"x": 0.0, "y": []}, {"x": 1.1, "y": [1]}, {"x": 2.2, "y": [2, 2]}],
            [],
            [{"x": 3.3, "y": [3, 3, 3]}, {"x": 4.4, "y": [4, 4, 4, 4]}],
        ]
    )
    generator = ak.layout.ArrayGenerator(
        lambda: template, form=template.layout.form, length=3
    )
    d = ak._util.MappingProxy({})
    cache = ak.layout.ArrayCache(d)
    virtualarray = ak.layout.VirtualArray(generator, cache)

    a = virtualarray[2]
    assert isinstance(a, ak.layout.RecordArray)
    assert len(d) == 1
    assert ak.to_list(a) == [{"x": 3.3, "y": [3, 3, 3]}, {"x": 4.4, "y": [4, 4, 4, 4]}]
    d.clear()

    a = virtualarray[1:]
    assert isinstance(a, ak.layout.VirtualArray)
    assert len(d) == 0
    b = a[1]
    assert isinstance(b, ak.layout.RecordArray)
    assert len(d) >= 1
    assert ak.to_list(b) == [{"x": 3.3, "y": [3, 3, 3]}, {"x": 4.4, "y": [4, 4, 4, 4]}]
    d.clear()

    a = virtualarray[[0, 2, 1, 0]]
    assert isinstance(a, ak.layout.VirtualArray)
    assert len(d) == 0
    b = a[1]
    assert isinstance(b, ak.layout.RecordArray)
    assert len(d) >= 1
    assert ak.to_list(b) == [{"x": 3.3, "y": [3, 3, 3]}, {"x": 4.4, "y": [4, 4, 4, 4]}]
    d.clear()

    a = virtualarray[[False, True, True]]
    assert isinstance(a, ak.layout.VirtualArray)
    assert len(d) == 0
    b = a[1]
    assert isinstance(b, ak.layout.RecordArray)
    assert len(d) >= 1
    assert ak.to_list(b) == [{"x": 3.3, "y": [3, 3, 3]}, {"x": 4.4, "y": [4, 4, 4, 4]}]
    d.clear()

    a = virtualarray["x"]
    assert isinstance(a, ak.layout.VirtualArray)
    assert len(d) == 0
    b = a[2]
    assert isinstance(b, ak.layout.NumpyArray)
    assert len(d) >= 1
    assert ak.to_list(b) == [3.3, 4.4]
    d.clear()

    a = virtualarray["y"]
    assert isinstance(a, ak.layout.VirtualArray)
    assert len(d) == 0
    b = a[2]
    assert isinstance(b, (ak.layout.ListArray64, ak.layout.ListOffsetArray64))
    assert len(d) >= 1
    assert ak.to_list(b) == [[3, 3, 3], [4, 4, 4, 4]]
    d.clear()

    a = virtualarray[::2, 1]
    assert isinstance(a, (ak.layout.RecordArray, ak.layout.IndexedArray64))
    assert len(d) >= 1
    assert ak.to_list(a) == [{"x": 1.1, "y": [1]}, {"x": 4.4, "y": [4, 4, 4, 4]}]
    d.clear()


def test_iter():
    generator = ak.layout.ArrayGenerator(
        fcn, form=ak.forms.NumpyForm([], 8, "d"), length=5
    )
    d = ak._util.MappingProxy({})
    cache = ak.layout.ArrayCache(d)
    virtualarray = ak.layout.VirtualArray(generator, cache)

    assert len(d) == 0
    it = iter(virtualarray)
    assert len(d) == 1
    d.clear()
    assert len(d) == 0
    assert next(it) == 1.1
    assert len(d) == 0
    assert list(it) == [2.2, 3.3, 4.4, 5.5]
    assert len(d) == 0


def test_nested_virtualness():
    counter = [0, 0]

    content = ak.layout.NumpyArray(
        np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
    )

    def materialize1():
        counter[1] += 1
        return content

    generator1 = ak.layout.ArrayGenerator(
        materialize1, form=content.form, length=len(content)
    )
    virtual1 = ak.layout.VirtualArray(generator1)

    offsets = ak.layout.Index64(np.array([0, 3, 3, 5, 6, 10], dtype=np.int64))
    listarray = ak.layout.ListOffsetArray64(offsets, virtual1)

    def materialize2():
        counter[0] += 1
        return listarray

    generator2 = ak.layout.ArrayGenerator(
        materialize2, form=listarray.form, length=len(listarray)
    )
    virtual2 = ak.layout.VirtualArray(generator2)

    assert counter == [0, 0]

    tmp1 = virtual2[2]
    assert isinstance(tmp1, ak.layout.VirtualArray)
    assert counter == [1, 0]

    tmp2 = tmp1[1]
    assert tmp2 == 4.4
    assert counter == [1, 1]


def test_highlevel():
    array = ak.virtual(lambda: [[1.1, 2.2, 3.3], [], [4.4, 5.5]])
    assert isinstance(array.layout, ak.layout.VirtualArray)
    assert ak.to_list(array) == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]

    counter = [0]

    def generate():
        counter[0] += 1
        return [[1.1, 2.2, 3.3], [], [4.4, 5.5]]

    array = ak.virtual(
        generate,
        length=3,
        form={"class": "ListOffsetArray64", "offsets": "i64", "content": "float64"},
    )
    assert counter[0] == 0

    assert len(array) == 3
    assert counter[0] == 0

    assert str(ak.type(array)) == "3 * var * float64"
    assert counter[0] == 0

    assert ak.to_list(array[2]) == [4.4, 5.5]
    assert counter[0] == 1
