# Copyright (c) 2025 <Godwin peter. O>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#  Project: pepper-local
#  Author: Godwin peter. O (me@godwin.dev)
#  Created At: Thu 09 Jan 2025 13:26:09
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Thu 09 Jan 2025 13:26:09

import dataclasses
from enum import Enum
import json
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.declarative import DeclarativeMeta


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        # if dataclasses.is_dataclass(o):
        #     return dataclasses.asdict(o)
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, set):
            return sorted(o)
        elif isinstance(o, Enum):
            return o.name
        elif isinstance(o.__class__, DeclarativeMeta):
            dict = {}
            # Remove invalid fields and just get the column attributes
            columns = [x for x in dir(o) if not x.startswith("_") and x != "metadata"]
            for column in columns:
                value = o.__getattribute__(column)

                try:
                    json.dumps(value)
                    dict[column] = value
                except TypeError:
                    if isinstance(value, datetime):
                        dict[column] = value.__str__()
                    else:
                        dict[column] = None
            return dict
        # elif isinstance(o.__class__, DeclarativeMeta):
        #     for relationship in o.__mapper__.relationships.items():
        #         if isinstance(relationship.__getattribute__("backref"), tuple):
        #             raise ValueError(
        #                 f'{o.__class__} oect has a "backref" relationship '
        #                 "that would cause an infinite loop!"
        #             )
        #     dictionary = {}
        #     column_names = [column.name for column in o.__table__.columns]
        #     for key in column_names:
        #         value = o.__getattribute__(key)
        #         if isinstance(value, datetime):
        #             value = o.isoformat()
        #         elif isinstance(value, Decimal):
        #             value = float(value)
        #         elif isinstance(value, set):
        #             value = sorted(value)
        #         dictionary[key] = value
        #     for key in [
        #         attribute
        #         for attribute in dir(o)
        #         if not attribute.startswith("_")
        #         and attribute != "metadata"
        #         and attribute not in column_names
        #     ]:
        #         value = o.__getattribute__(key)
        #         dictionary[key] = value
        #     return dictionary

        print(f"======>>> {o} <<<=====")

        return json.JSONEncoder.default(self, o)


def new_alchemy_encoder(revisit_self=False, fields_to_expand=[]):
    _visited_os = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if o in _visited_os:
                        return None
                    _visited_os.append(o)

                # go through each field in this SQLalchemy class
                fields = {}
                for field in [
                    x for x in dir(o) if not x.startswith("_") and x != "metadata"
                ]:
                    val = o.__getattribute__(field)

                    # is this field another SQLalchemy oect, or a list of SQLalchemy oects?
                    if isinstance(val.__class__, DeclarativeMeta) or (
                        isinstance(val, list)
                        and len(val) > 0
                        and isinstance(val[0].__class__, DeclarativeMeta)
                    ):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field] = None
                            continue

                    fields[field] = val
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, o)

    return AlchemyEncoder
