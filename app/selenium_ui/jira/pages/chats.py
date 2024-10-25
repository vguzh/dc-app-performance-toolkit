from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.jira.pages.selectors import UrlManager, ChatsSelectors


class Chats(BasePage):
    _DATA_ID_ATTR = "data-id"

    _TITLE_ROW_BY_NAME_LOCATOR = "//*[@headers='chat'][normalize-space(text())='{}']"
    _ROW_BY_NAME_LOCATOR = _TITLE_ROW_BY_NAME_LOCATOR + "/.."
    _ROW_BY_ROW_ID_LOCATOR = "//div[@id='chats-table']//tr[@data-id='{}']"
    _EDIT_CHAT_LINK_LOCATOR = _ROW_BY_ROW_ID_LOCATOR + "//button[contains(@class, 'edit-chat-link')]"
    _DELETE_CHAT_LINK_LOCATOR = _ROW_BY_ROW_ID_LOCATOR + "//a[contains(@class, 'delete-chat-link')]"
    _CONFIRM_DELETE_BUTTON_LOCATOR = _ROW_BY_ROW_ID_LOCATOR + "//button[contains(@class, 'do-delete')]"

    page_loaded_selector = ChatsSelectors.project_chats_table

    def __init__(self, driver, project_key):
        BasePage.__init__(self, driver)
        url_manager = UrlManager(project_key=project_key)
        self.page_url = url_manager.chats_page_url()

    def open_create_chat_popup(self):
        self.get_element(ChatsSelectors.crete_chat_button).click()

    def open_edit_project_chat_popup_by_row_id(self, row_id):
        self.get_element((By.XPATH, self._EDIT_CHAT_LINK_LOCATOR.format(row_id))).click()

    def delete_project_chat_by_row_id(self, row_id):
        self.get_element((By.XPATH, self._DELETE_CHAT_LINK_LOCATOR.format(row_id))).click()
        self.wait_until_visible((By.XPATH, self._CONFIRM_DELETE_BUTTON_LOCATOR.format(row_id))).click()

    def get_row_id(self):
        row_selector = (By.XPATH, self._ROW_BY_NAME_LOCATOR.format(self._get_current_project_name()))
        return self.wait_until_present(row_selector).get_attribute(self._DATA_ID_ATTR)

    def wait_until_visible_project_chat(self):
        self.wait_until_visible((By.XPATH, self._TITLE_ROW_BY_NAME_LOCATOR.format(self._get_current_project_name())))

    def wait_until_invisible_project_chat_by_row_id(self, row_id):
        self.wait_until_invisible((By.XPATH, self._ROW_BY_ROW_ID_LOCATOR.format(row_id)))

    def _get_current_project_name(self):
        return self.wait_until_present(ChatsSelectors.title_chat_link).text.strip()
