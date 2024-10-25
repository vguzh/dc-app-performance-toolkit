from selenium.webdriver.support.select import Select

from selenium_ui.base_page import BasePage
from selenium_ui.jira.pages.selectors import ChatsPopupSelectors


class CreateChatPopup(BasePage):
    page_loaded_selector = ChatsPopupSelectors.crete_chats_popup

    def __init__(self, driver, notification_types):
        BasePage.__init__(self, driver)
        self.notification_types = notification_types

    def confirm_create(self):
        self.get_element(ChatsPopupSelectors.submit_button).click()

    def create_project_chat(self):
        self._click_project_type()
        self._select_all_notification_types()
        self._click_view_admins_option()

    def _select_all_notification_types(self):
        select = Select(self.get_element(ChatsPopupSelectors.notification_types_select))
        for notification_type in self.notification_types:
            select.select_by_visible_text(notification_type[0])

    def _click_project_type(self):
        self.get_element(ChatsPopupSelectors.project_type_label).click()

    def _click_view_admins_option(self):
        self.get_element(ChatsPopupSelectors.view_admins_label).click()
