from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.jira.pages.selectors import ChatsPopupSelectors


class EditChatPopup(BasePage):
    _REMOVE_USER_LINK_LOCATOR = "//div[@id='participants-container']//div[normalize-space(text())='{}']//../a"

    page_loaded_selector = ChatsPopupSelectors.crete_chats_popup

    def __init__(self, driver, notification_types):
        BasePage.__init__(self, driver)
        self.notification_types = notification_types

    def confirm_update(self):
        self.get_element(ChatsPopupSelectors.submit_button).click()

    def add_user(self, user_name):
        self._remove_user_if_added(user_name)
        self.get_element(ChatsPopupSelectors.users_field).send_keys(user_name)
        self.wait_until_any_element_visible(ChatsPopupSelectors.users_autocompile_result)[0].click()

    def remove_all_users(self):
        for participant_user in self.get_elements(ChatsPopupSelectors.participant_users):
            self._remove_user_if_added(participant_user.text.strip())

    def _remove_user_if_added(self, user_name):
        remove_user_link_locator = (By.XPATH, self._REMOVE_USER_LINK_LOCATOR.format(user_name))
        if self.get_elements(remove_user_link_locator):
            self.get_element(remove_user_link_locator).click()
            self.wait_until_invisible(remove_user_link_locator)
