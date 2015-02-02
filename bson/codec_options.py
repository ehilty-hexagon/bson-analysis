# Copyright 2014 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for specifying BSON codec options."""

from collections import MutableMapping

from bson.binary import ALL_UUID_REPRESENTATIONS, PYTHON_LEGACY


class CodecOptions(object):
    """Encapsulates BSON options used in CRUD operations.

    :Parameters:
      - `as_class`: BSON documents returned in queries will be decoded
        to an instance of this class. Must be a subclass of
        :class:`~collections.MutableMapping`. Defaults to :class:`dict`.
      - `tz_aware`: If ``True``, BSON datetimes will be decoded to timezone
        aware instances of :class:`~datetime.datetime`. Otherwise they will be
        naive. Defaults to ``False``.
      - `uuid_representation`: The BSON representation to use when encoding
        and decoding instances of :class:`~uuid.UUID`. Defaults to
        :data:`~bson.binary.PYTHON_LEGACY`.
    """

    __slots__ = ("__as_class", "__tz_aware", "__uuid_rep")

    def __init__(self, as_class=dict,
                 tz_aware=False, uuid_representation=PYTHON_LEGACY):
        if not issubclass(as_class, MutableMapping):
            raise TypeError("document_class must be a "
                            "subclass of MutableMapping")
        if not isinstance(tz_aware, bool):
            raise TypeError("tz_aware must be a boolean")
        if uuid_representation not in ALL_UUID_REPRESENTATIONS:
            raise ValueError("uuid_representation must be a value "
                             "from bson.binary.ALL_UUID_REPRESENTATIONS")

        self.__as_class = as_class
        self.__tz_aware = tz_aware
        self.__uuid_rep = uuid_representation

    @property
    def as_class(self):
        """Read only property for as_class."""
        return self.__as_class

    @property
    def tz_aware(self):
        """Read only property for tz_aware."""
        return self.__tz_aware

    @property
    def uuid_representation(self):
        """Read only property for uuid_representation."""
        return self.__uuid_rep

    def __eq__(self, other):
        if isinstance(other, CodecOptions):
            return (self.__as_class == other.as_class and
                    self.__tz_aware == other.tz_aware and
                    self.__uuid_rep == other.uuid_representation)
        raise NotImplementedError

    def __ne__(self, other):
        return self != other


def _parse_codec_options(options):
    """Parse BSON codec options."""
    as_class = options.get('document_class', dict)
    tz_aware = options.get('tz_aware', False)
    uuid_rep = options.get('uuidrepresentation', PYTHON_LEGACY)
    return CodecOptions(as_class, tz_aware, uuid_rep)