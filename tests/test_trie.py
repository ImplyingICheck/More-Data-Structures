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
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
import pytest

from data_structures import trie

ROOT_DATA = 'Root'


@pytest.fixture
def fixture_trie():
  return trie.Trie()


@pytest.fixture
def fixture_test_word():
  return 'Hello World!'


def generate_expected_prettify(
    word: str, final_prefix: str, terminal_suffix: str, alignment_width: int
) -> str:
  """Function generates output equivalent to that of a Trie containing a single
  word."""
  output = [ROOT_DATA, '\n']
  for depth, letter in enumerate(word):
    output.append(' ' * alignment_width * depth)
    # Every letter uses a final_prefix as none have more than one child
    output.append(final_prefix)
    output.append(letter)
    output.append('\n')
  # Removes the trailing newline and adds the terminal suffix
  output[-1] = terminal_suffix
  return ''.join(output)


class TestTrie:

  def test_init_empty_parameters(self):
    assert trie.Trie()

  def test_insert_well_formed(self, fixture_trie, fixture_test_word):
    fixture_trie.insert(fixture_test_word)
    assert fixture_trie.find(fixture_test_word)

  def test_insert_substring_marked_as_terminal(self, fixture_trie):
    sut = fixture_trie
    sut.insert('Hello')
    sut.insert('Hell')
    assert fixture_trie.find('Hell')

  def test_insert_none_raises_type_error(self, fixture_trie):
    sut = fixture_trie
    with pytest.raises(TypeError):
      sut.insert(None)

  def test_insert_empty_string(self, fixture_trie):
    sut = fixture_trie
    sut.insert('')

  def test_delete(self, fixture_trie, fixture_test_word):
    sut = fixture_trie
    sut.insert(fixture_test_word)
    sut.delete(fixture_test_word)
    assert not sut.find(fixture_test_word)

  def test_find_well_formed(self, fixture_trie, fixture_test_word):
    sut = fixture_trie
    sut.insert(fixture_test_word)
    assert sut.find(fixture_test_word)

  def test_find_empty_string_true(self, fixture_trie):
    sut = fixture_trie
    assert sut.find('')

  def test_prettify_empty_trie(self, fixture_trie):
    sut = fixture_trie
    assert sut.prettify()

  def test_prettify_empty_trie_prints_root(self, fixture_trie):
    sut = fixture_trie
    assert sut.prettify() == ROOT_DATA

  def test_prettify_well_formed_trie(self, fixture_trie, fixture_test_word):
    sut = fixture_trie
    sut.insert(fixture_test_word)
    assert sut.prettify()

  def test_prettify_returns_string(self, fixture_trie):
    sut = fixture_trie
    assert isinstance(sut.prettify(), str)

  def test_prettify_nested_structure(self, fixture_trie, fixture_test_word):
    entry_prefix = '├── '
    final_prefix = '└── '
    terminal_suffix = '**'
    alignment_width = 4
    sut = fixture_trie
    sut.insert(fixture_test_word)
    actual_output = sut.prettify(
        entry_prefix=entry_prefix,
        final_prefix=final_prefix,
        terminal_suffix=terminal_suffix,
        alignment_width=alignment_width,
    )
    expected_output = generate_expected_prettify(
        fixture_test_word, final_prefix, terminal_suffix, alignment_width
    )
    assert actual_output == expected_output
