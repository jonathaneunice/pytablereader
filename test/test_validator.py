# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

from pytablereader._constant import SourceType
from pytablereader._validator import (
    FileValidator,
    TextValidator,
    UrlValidator,
)
import pytest

import pytablereader as ptr


class Test_FileValidator_validate(object):

    @pytest.mark.parametrize(["value"], [
        ["test"],
    ])
    def test_normal(self, tmpdir, value):
        p_file_path = tmpdir.join(value)

        with open(str(p_file_path), "w") as _f:
            pass

        validator = FileValidator(str(p_file_path))
        assert validator.source_type == SourceType.FILE
        validator.validate()

    @pytest.mark.parametrize(["value", "expected"], [
        [None, ptr.InvalidFilePathError],
        ["", ptr.InvalidFilePathError],
    ])
    def test_exception_null(self, value, expected):
        validator = FileValidator(value)

        with pytest.raises(expected):
            validator.validate()

    @pytest.mark.parametrize(["value", "expected"], [
        ["te\0st", ptr.InvalidFilePathError]
    ])
    def test_exception_invalid_path(self, tmpdir, value, expected):
        validator = FileValidator(value)

        with pytest.raises(expected):
            validator.validate()


class Test_TextValidator_validate(object):

    @pytest.mark.parametrize(["value"], [
        ["test"],
    ])
    def test_normal(self, value):
        validator = TextValidator(value)
        assert validator.source_type == SourceType.TEXT
        validator.validate()

    @pytest.mark.parametrize(["value", "expected"], [
        [None, ptr.EmptyDataError],
        ["", ptr.EmptyDataError],
    ])
    def test_exception(self, value, expected):
        validator = TextValidator(value)

        with pytest.raises(expected):
            validator.validate()


class Test_UrlValidator_validate(object):

    @pytest.mark.parametrize(["value"], [
        ["http://www.google.com"],
        ["https://github.com/"],
    ])
    def test_normal(self, value):
        validator = UrlValidator(value)
        assert validator.source_type == SourceType.URL
        validator.validate()

    @pytest.mark.parametrize(["value", "expected"], [
        [None, ptr.InvalidUrlError],
        ["", ptr.InvalidUrlError],
        ["www.google.com", ptr.InvalidUrlError],
    ])
    def test_exception(self, value, expected):
        validator = UrlValidator(value)

        with pytest.raises(expected):
            validator.validate()
