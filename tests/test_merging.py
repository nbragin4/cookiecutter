"""
tests_merging.

Test formerly known from a unittest residing in test_generate.py named
TestMerge.tests_merging
"""
from scaffoldrom.merging import merger


manifest = {
    "list": [
        {
            "value": "default"
        }
    ],
    "multilist": [
        "one", "two", "three"
    ]
}
values = {
    "list": [
        {
            "one": "1"
        },
        {
            "two": "2"
        },
        {
            "three": "3"
        },
        {
            "four": "4",
            "value": "custom"
        }
    ],
    "multilist": [
        "x", "y", "z", "w"
    ]

}
expected_result = {
    "list": [
        {
            "one": "1",
            "value": "default"
        },
        {
            "two": "2",
            "value": "default"
        },
        {
            "three": "3",
            "value": "default"
        },
        {
            "four": "4",
            "value": "custom"
        }
    ],
    "multilist": [
        "x", "y", "z", "w"
    ]
}

def test_merging_merger():
    """test yaml loading"""
    result = merger.merge(manifest.copy(), values)
    assert result == expected_result
