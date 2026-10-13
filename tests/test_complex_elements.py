from playwright.sync_api import Page, expect


def test_web_table_update_salary(page: Page):
    page.goto('/webtables')
    user_row = page.locator('tr').filter(has_text='alden@example.com')
    status_cell = user_row.locator('td').nth(4)

    expect(status_cell).to_have_text('12000')

    user_row.locator('[title="Edit"]').click()
    page.locator('#salary').clear()
    page.locator('#salary').type('25000')
    page.get_by_role('button', name='submit').click()

    status_cell = user_row.locator('td').nth(4)
    expect(status_cell).to_have_text('25000')


def test_custom_checkbox_selection(page: Page):
    page.goto('/checkbox')
    page.locator('div[role="treeitem"]').filter(has_text='Home').locator(
        '.rc-tree-switcher'
    ).click()
    page.locator('div[role="treeitem"]').filter(has_text='Downloads').locator(
        '.rc-tree-switcher'
    ).click()
    page.locator('div[role="treeitem"]').filter(has_text='Word File.doc').locator(
        '.rc-tree-checkbox'
    ).click()
    page.locator('div[role="treeitem"]').filter(has_text='Excel File.doc').locator(
        '.rc-tree-checkbox'
    ).click()

    expected_items = ["excelFile", "wordFile", "downloads"]
    expect(page.locator("#result .text-success")).to_have_count(len(expected_items))
    for item in expected_items:
        expect(page.locator("#result")).to_contain_text(item)


def test_react_select_and_slider(page: Page):
    page.goto('/select-menu')

    page.locator('#withOptGroup').click()
    page.get_by_text('Group 2, option 1', exact=True).click()

    expect(page.locator("#withOptGroup")).to_contain_text("Group 2, option 1")

    page.goto('/slider')

    slider = page.locator('#slider')

    box = slider.bounding_box()

    target_x = box['x'] + (box['width'] * 0.84)
    center_y = box['y'] + (box['height'] / 2)

    start_x = box['x'] + (box['width'] * 0.25)

    page.mouse.move(start_x, center_y)
    page.mouse.down()
    page.mouse.move(target_x, center_y)
    page.mouse.up()

    expect(slider).to_have_value('85')

    expect(page.locator('#sliderValue')).to_have_value('85')
