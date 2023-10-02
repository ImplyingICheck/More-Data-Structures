#  Copyright 2023 The More Data Structures Authors. All Rights Reserved.
#
#  This file is part of More Data Structures.
#
#  More Data Structures is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  More Data Structures is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#  details. You should have received a copy of the GNU General Public License
#  along with More Data Structures. If not, see <https://www.gnu.org/licenses/>.
#
#  Copyright (c) 2023 More Data Structures Authors
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
"""A Trie data structure with various helper function.

Insertion, deletion, and find are O(k) where k is the length of the argument to
be iterated over.
"""
from __future__ import annotations

from collections.abc import Iterable, Reversible
from typing import Any, Generic, TypeVar


_T = TypeVar('_T')
_S = TypeVar('_S')
_T_co = TypeVar('_T_co', covariant=True)


class Node(Generic[_T]):
  __slots__ = ('data', 'is_terminal', 'children')


class _KNode(Node[_T]):

  def __init__(self, data: _T, is_terminal: bool = False):
    self.data: _T = data
    self.is_terminal: bool = is_terminal
    self.children: dict[_T, _KNode[_T]] = {}


class _KRoot(Node[_T]):

  def __init__(self):
    self.data = 'Root'
    self.is_terminal = True
    self.children: dict[_T, _KNode[_T]] = {}


def _get_last_child(view: Reversible[_T_co]) -> _T_co | None:
  return next(reversed(view), None)


def _prettify(
    root: _KRoot[Any],
    entry_prefix: str = '├── ',
    final_prefix: str = '└── ',
    terminal_suffix: str = '**',
    alignment_width: int = 4,
) -> str:
  """Helper function for pretty printing. Initialises return value storage and
  handles data conversion.

  Args:
    root:
    entry_prefix:
    final_prefix:
    terminal_suffix:
    alignment_width:

  Returns:

  """
  output = [root.data, '\n']
  final_child = _get_last_child(root.children.values())
  for child in root.children.values():
    _prettify_node(
        child,
        entry_prefix=entry_prefix,
        final_prefix=final_prefix,
        terminal_suffix=terminal_suffix,
        alignment_width=alignment_width,
        output=output,
        final_entry=child is final_child,
    )
  return ''.join(map(str, output))


def _prettify_node(
    node: _KNode[_T],
    entry_prefix: str,
    final_prefix: str,
    terminal_suffix: str,
    alignment_width: int,
    output: list[_T | str],
    depth: int = 0,
    final_entry: bool = False,
) -> None:
  prefix = final_prefix if final_entry else entry_prefix
  alignment = len(prefix) + alignment_width * depth
  prefix = prefix.rjust(alignment)
  terminator = terminal_suffix if node.is_terminal else ''
  output.extend([prefix, node.data, terminator, '\n'])
  final_child = _get_last_child(node.children.values())
  for child in node.children.values():
    _prettify_node(
        child,
        entry_prefix=entry_prefix,
        final_prefix=final_prefix,
        terminal_suffix=terminal_suffix,
        alignment_width=alignment_width,
        output=output,
        depth=depth + 1,
        final_entry=child is final_child,
    )


class Trie(Generic[_T]):
  """Representation of a Trie data structure.

  Though arguments are named *string*, any iterable type that supports hashing
  can be used."""

  __slots__ = ('root',)

  def __init__(self):
    self.root: _KRoot[_T] = _KRoot()

  def _traverse(
      self, string: Iterable[_T], add_missing: bool = False
  ) -> _KNode[_T] | _KRoot[_T] | None:
    """

    Args:
      string:
      add_missing:

    Returns:
      If *add_missing* is True, a _KNode or _KRoot will always be returned.
      If *add_missing* is false, a _KNode or _KRoot or None will be returned.

    """
    current_node = self.root
    for letter in string:
      if letter not in current_node.children:
        if add_missing:
          current_node.children[letter] = _KNode(letter)
        else:
          return None
      current_node = current_node.children[letter]
    return current_node

  def insert(self, string: Iterable[_T]) -> None:
    node = self._traverse(string, add_missing=True)
    assert node
    node.is_terminal = True

  def delete(self, string: Iterable[_T]) -> None:
    node = self._traverse(string)
    if node:
      node.is_terminal = False

  def find(self, string: Iterable[_T]) -> bool:
    node = self._traverse(string)
    return node.is_terminal if node else False

  def prettify(
      self,
      entry_prefix: str = '├── ',
      final_prefix: str = '└── ',
      terminal_suffix: str = '**',
      alignment_width: int = 4,
  ) -> str:
    pretty_print = _prettify(
        self.root,
        entry_prefix=entry_prefix,
        final_prefix=final_prefix,
        terminal_suffix=terminal_suffix,
        alignment_width=alignment_width,
    )
    return pretty_print.rstrip()
