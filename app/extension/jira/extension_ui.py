import random

from selenium_ui.conftest import print_timing
from selenium_ui.constants.jira_data_key import NOTIFICATION_TYPES, AUTHORIZED_TELEGRAM_USERS
from selenium_ui.jira.pages.chats import Chats
from selenium_ui.jira.pages.pages import Login
from selenium_ui.jira.pages.popups.edit_chat_popup import EditChatPopup
from selenium_ui.jira.pages.popups.сreate_сhat_popup import CreateChatPopup
from util.conf import JIRA_SETTINGS

CURRENT_SESSION = "current_session"
PROJECT_KEY = "project_key"


def jira_admin_login(webdriver):
    login_page = Login(webdriver)
    login_page.delete_all_cookies()

    @print_timing("selenium_app_specific_user_login")
    def measure():
        login_page.go_to()
        login_page.set_credentials(username=JIRA_SETTINGS.admin_login, password=JIRA_SETTINGS.admin_password)
        if login_page.is_first_login():
            login_page.first_login_setup()
        if login_page.is_first_login_second_page():
            login_page.first_login_second_page_setup()
        login_page.wait_for_page_loaded()

    measure()


def view_chats(webdriver, datasets):
    chats_page = Chats(webdriver, project_key=_get_project_key(datasets))

    @print_timing("selenium_social_jira:view_chats")
    def measure():
        chats_page.go_to()
        chats_page.wait_for_page_loaded()

    measure()


def create_chat(webdriver, datasets):
    chats_page = Chats(webdriver, project_key=_get_project_key(datasets))
    create_chat_popup = CreateChatPopup(webdriver, datasets[NOTIFICATION_TYPES])

    @print_timing("selenium_social_jira:open_create_chat_popup")
    def sub_measure():
        chats_page.open_create_chat_popup()
        create_chat_popup.wait_for_page_loaded()

    sub_measure()

    @print_timing("selenium_social_jira:fill_and_submit_create_chat_form")
    def measure():
        create_chat_popup.create_project_chat()
        create_chat_popup.confirm_create()
        create_chat_popup.wait_until_page_invisible()

    measure()

    @print_timing("selenium_social_jira:display_chat_in_table")
    def measure_add_chat():
        chats_page.wait_until_visible_project_chat()

    measure_add_chat()


def delete_chat(webdriver, datasets):
    chats_page = Chats(webdriver, project_key=_get_project_key(datasets))
    view_chats(webdriver, datasets)
    row_id = chats_page.get_row_id()

    @print_timing("selenium_social_jira:delete_chat")
    def sub_measure():
        chats_page.delete_project_chat_by_row_id(row_id)

    sub_measure()

    @print_timing("selenium_social_jira:chat_not_displayed_in_table")
    def measure():
        chats_page.wait_until_invisible_project_chat_by_row_id(row_id)

    measure()


def add_user_to_chat(webdriver, datasets):
    chats_page = Chats(webdriver, project_key=_get_project_key(datasets))
    edit_chat_popup = EditChatPopup(webdriver, datasets[NOTIFICATION_TYPES])
    authorized_user_name = random.choice(datasets[AUTHORIZED_TELEGRAM_USERS])[0]

    _open_edit_chat_popup(webdriver, datasets)

    @print_timing("selenium_social_jira:fill_and_submit_update_chat_form")
    def measure():
        edit_chat_popup.add_user(authorized_user_name)
        edit_chat_popup.confirm_update()
        edit_chat_popup.wait_until_page_invisible()
        chats_page.wait_for_page_loaded()

    measure()


def delete_users_from_chat(webdriver, datasets):
    chats_page = Chats(webdriver, project_key=_get_project_key(datasets))
    edit_chat_popup = EditChatPopup(webdriver, datasets[NOTIFICATION_TYPES])

    _open_edit_chat_popup(webdriver, datasets)

    @print_timing("selenium_social_jira:remove_users_from_chat_and_submit")
    def measure():
        edit_chat_popup.remove_all_users()
        edit_chat_popup.confirm_update()
        edit_chat_popup.wait_until_page_invisible()
        chats_page.wait_for_page_loaded()

    measure()


def _open_edit_chat_popup(webdriver, datasets):
    chats_page = Chats(webdriver, project_key=_get_project_key(datasets))
    edit_chat_popup = EditChatPopup(webdriver, datasets[NOTIFICATION_TYPES])
    view_chats(webdriver, datasets)
    row_id = chats_page.get_row_id()

    @print_timing("selenium_social_jira:open_edit_chat_popup")
    def measure():
        chats_page.open_edit_project_chat_popup_by_row_id(row_id)
        edit_chat_popup.wait_for_page_loaded()

    measure()


def _get_project_key(datasets):
    return datasets[CURRENT_SESSION][PROJECT_KEY]
