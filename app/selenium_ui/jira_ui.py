from extension.jira import extension_ui  # noqa F401
from selenium_ui.jira import modules


# this action should be the first one
def test_0_selenium_a_login(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.login(jira_webdriver, jira_datasets)


def test_1_selenium_view_project_summary(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.view_project_summary(jira_webdriver, jira_datasets)


def test_1_selenium_browse_projects_list(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.browse_projects_list(jira_webdriver, jira_datasets)


def test_1_selenium_browse_boards_list(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.browse_boards_list(jira_webdriver, jira_datasets)


def test_1_selenium_create_issue(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.create_issue(jira_webdriver, jira_datasets)


def test_1_selenium_edit_issue(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.edit_issue(jira_webdriver, jira_datasets)


def test_1_selenium_save_comment(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.save_comment(jira_webdriver, jira_datasets)


def test_1_selenium_search_jql(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.search_jql(jira_webdriver, jira_datasets)


def test_1_selenium_view_backlog_for_scrum_board(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.view_backlog_for_scrum_board(jira_webdriver, jira_datasets)


def test_1_selenium_view_scrum_board(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.view_scrum_board(jira_webdriver, jira_datasets)


def test_1_selenium_view_kanban_board(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.view_kanban_board(jira_webdriver, jira_datasets)


def test_1_selenium_view_dashboard(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.view_dashboard(jira_webdriver, jira_datasets)


def test_1_selenium_view_issue(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.view_issue(jira_webdriver, jira_datasets)


def test_1_selenium_view_chats_page(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.jira_admin_login(jira_webdriver)
    extension_ui.view_chats(jira_webdriver, jira_datasets)


def test_1_selenium_create_chat(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.create_chat(jira_webdriver, jira_datasets)


def test_1_selenium_add_user(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.add_user_to_chat(jira_webdriver, jira_datasets)


def test_1_selenium_remove_user_from_chat(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.delete_users_from_chat(jira_webdriver, jira_datasets)


def test_1_selenium_delete_chat(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.delete_chat(jira_webdriver, jira_datasets)


# this action should be the last one
def test_2_selenium_z_log_out(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.log_out(jira_webdriver, jira_datasets)
