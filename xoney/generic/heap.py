# Copyright 2022 Vladyslav Kochetov. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from __future__ import annotations


from typing import TypeVar
from typing import Iterable

import copy

T: TypeVar = TypeVar("T")


class Heap:
    _members: list[T]

    def __init__(self, members: Iterable[T] | None = None):
        if members is None:
            members = []
        self._members = list(members)

    def __iter__(self):
        member: T
        for member in self._members:
            yield member

    def add(self, new: T) -> None:
        self._members.append(new)

    def remove(self, member: T) -> None:
        member_in_heap: T

        for member_in_heap in self._members:
            if member == member_in_heap:
                self._members.remove(member_in_heap)
                break

    def get_members(self) -> list[T]:
        """
        :return: Copies of all members in the heap.
        """
        return copy.deepcopy(self._members)

    def __len__(self) -> int:
        return len(self._members)

    def __contains__(self, item) -> bool:
        for level in self._members:
            if level == item:
                return True
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self._members)})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Heap):
            raise TypeError(f"To compare object with <Heap>, "
                            "this object must be of type <Heap>")
        return self._members == other._members
