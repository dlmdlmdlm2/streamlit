# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
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

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction
from e2e_playwright.shared.app_utils import get_element_by_key


def test_space_elements_exist(app: Page):
    """Test that space elements are rendered with correct dimensions."""
    space_elements = app.get_by_test_id("stSpace")
    # We have multiple space elements in the test app
    expect(space_elements.first).to_be_attached()

    # Verify space elements have no visible content
    first_space = space_elements.first
    expect(first_space).to_have_text("")

    # Check the first two space elements (in vertical layout, so height should be set)
    # First space: st.space("medium") = 2.5rem = 40px height
    first_space = space_elements.nth(0)
    first_space_box = first_space.bounding_box()
    assert first_space_box is not None
    assert int(first_space_box["height"]) == 40  # 2.5rem * 16px = 40px

    # Second space: st.space("large") = 4.25rem = 68px height
    second_space = space_elements.nth(1)
    second_space_box = second_space.bounding_box()
    assert second_space_box is not None
    assert int(second_space_box["height"]) == 68  # 4.25rem * 16px = 68px


def test_horizontal_container_spacing(app: Page, assert_snapshot: ImageCompareFunction):
    """Test horizontal spacing with medium and stretch in a horizontal container."""
    horizontal_container = get_element_by_key(app, "horizontal_container_space")
    expect(horizontal_container).to_be_attached()

    # Snapshot the horizontal container to show medium and stretch spacing
    assert_snapshot(horizontal_container, name="st_space_horizontal_container")


def test_vertical_container_with_stretch(
    app: Page, assert_snapshot: ImageCompareFunction
):
    """Test vertical spacing including stretch in a fixed-height vertical container."""
    vertical_container = get_element_by_key(app, "vertical_container_space")
    expect(vertical_container).to_be_attached()

    # Snapshot shows 25px space, stretch space, and default small space
    assert_snapshot(vertical_container, name="st_space_vertical_container_stretch")


def test_nested_containers_with_space(app: Page, assert_snapshot: ImageCompareFunction):
    """Test that space works correctly in nested containers with different directions."""
    # Get the nested container with outer vertical and inner horizontal
    nested_container = get_element_by_key(app, "nested_container_space")
    expect(nested_container).to_be_attached()

    # Visual snapshot to verify spacing adapts to direction in nested contexts:
    # - Outer container: vertical spacing with large and medium
    # - Inner horizontal container: horizontal stretch spacing
    assert_snapshot(nested_container, name="st_space_nested_containers")
