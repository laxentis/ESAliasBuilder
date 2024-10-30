import logging

import dearpygui.dearpygui as dpg

from alias import AliasFile, Alias
from esData import functions

file: AliasFile = AliasFile()
logging.basicConfig(level=logging.WARNING)

dpg.create_context()


# dpg.show_item_registry()


def select_callback(sender: int, _appdata: None, userdata: str):
    """
    Callback for selecting a table entry
    :param sender: id of the clicked item
    :param _appdata: not used, required for dearpygui compatibility
    :param userdata: alias designator
    :return:
    """
    entry = file.aliases[userdata]
    logging.debug('Selected entry ' + userdata + ' sender: ' + str(sender))
    dpg.set_value('edit_alias_alias', entry.alias)
    dpg.set_value('edit_alias_english', entry.english)
    dpg.set_value('edit_alias_polish', entry.polish)
    dpg.show_item('edit_alias_dialog')
    row = dpg.get_item_parent(sender)
    file.aliases.pop(entry.alias, None)
    dpg.delete_item(row)


def add_alias_to_table(table_tag: str, alias: Alias):
    """
    Adds an alias to a table
    :param table_tag: DPG tag of the table
    :param alias: alias to add
    :return:
    """
    with dpg.table_row(parent=table_tag, tag=f"alias_{alias.alias}"):
        a = dpg.add_selectable(label=alias.alias, span_columns=True, callback=select_callback)
        dpg.set_item_user_data(a, alias.alias)
        e = dpg.add_selectable(label=alias.english, span_columns=True, callback=select_callback)
        dpg.set_item_user_data(e, alias.english)
        p = dpg.add_selectable(label=alias.polish, span_columns=True, callback=select_callback)
        dpg.set_item_user_data(p, alias.polish)


def file_load_callback(_sender, app_data):
    """
    Callback for loading an alias file
    :param _sender: not used, needed for DPG compatibility
    :param app_data: data returned by file dialog
    :return:
    """
    global file
    file.read_file(app_data['file_path_name'])
    # file.print_aliases()
    for alias in file.aliases:
        add_alias_to_table("alias_table", file.aliases[alias])
    dpg.hide_item('load_file_button')
    dpg.show_item('clear_file_button')  # dpg.show_item('save_as_button')  # dpg.show_item('add_alias_button')


def file_clear_callback(_sender, _app_data):
    """
    Callback for clearing an alias file
    :return:
    """
    global file
    file = AliasFile()
    dpg.delete_item('alias_table', children_only=True)
    dpg.hide_item('clear_file_button')
    # dpg.hide_item('add_alias_button')
    # dpg.hide_item('save_as_button')
    dpg.show_item('load_file_button')


def save_file_callback(_sender, app_data):
    """
    Callback for saving an alias file
    :param _sender: not used, needed for DPG compatibility
    :param app_data: data returned by file dialog
    :return:
    """
    global file
    file.save_to_file(app_data['file_path_name'])


with dpg.file_dialog(show=False, callback=file_load_callback, tag='file_dialog_id', width=500, height=500):
    dpg.add_file_extension(".txt")

with dpg.file_dialog(show=False, tag='save_file_dialog', width=500, height=500, callback=save_file_callback):
    dpg.add_file_extension(".txt")

dpg.create_viewport(title='EuroScope Alias Builder')

with dpg.window(tag="Primary Window"):
    with dpg.table(tag="alias_table", header_row=True, row_background=True, borders_innerH=True, borders_innerV=True,
                   borders_outerH=True, borders_outerV=True, policy=dpg.mvTable_SizingStretchProp):
        dpg.add_table_column(label="Alias")
        dpg.add_table_column(label="English")
        dpg.add_table_column(label="Polish")
    with dpg.group(horizontal=True):
        dpg.add_button(label='Load file', callback=lambda: dpg.show_item('file_dialog_id'), tag='load_file_button',
                       show=True)
        dpg.add_button(label='Add alias', show=True, tag='add_alias_button',
                       callback=lambda: dpg.show_item('add_alias_dialog'))
        dpg.add_button(label='Clear file', callback=file_clear_callback, tag='clear_file_button', show=False)
        dpg.add_button(label='Save as', tag='save_as_button', show=True,
                       callback=lambda: dpg.show_item('save_file_dialog'))


def clear_add_alias_dialog_callback(_sender, _app_data):
    dpg.set_value('add_alias_alias', "")
    dpg.set_value('add_alias_english', "")
    dpg.set_value('add_alias_polish', "")
    dpg.hide_item('add_alias_dialog')


def add_alias_callback(sender, app_data):
    global file
    alias = dpg.get_value('add_alias_alias')
    english = dpg.get_value('add_alias_english')
    polish = dpg.get_value('add_alias_polish')
    entry = Alias(alias, english, polish)
    file.aliases[alias] = entry
    add_alias_to_table("alias_table", entry)
    clear_add_alias_dialog_callback(sender, app_data)


def combo_changed_callback(_sender, app_data):
    description = functions[app_data]
    dpg.set_value("alias_add_function_description", description)


def add_to_text(_sender, _app_data, user_data):
    text = dpg.get_value(user_data)
    function = dpg.get_value("add_alias_function")
    text += function
    dpg.set_value(user_data, text)


with dpg.window(label='Add Alias', tag='add_alias_dialog', modal=True, show=False, width=1000, height=350):
    dpg.add_input_text(label="Alias", tag="add_alias_alias")
    dpg.add_input_text(label="English", tag="add_alias_english")
    dpg.add_input_text(label="Polish", tag="add_alias_polish")
    with dpg.group(horizontal=True):
        with dpg.group():
            dpg.add_combo(label="Function", items=list(functions.keys()), tag="add_alias_function",
                          callback=combo_changed_callback, )
            dpg.add_text(tag="alias_add_function_description")
        with dpg.group():
            dpg.add_button(label="Add EN", callback=add_to_text, user_data="add_alias_english")
            dpg.add_button(label="Add PL", callback=add_to_text, user_data="add_alias_polish")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Add", callback=add_alias_callback)
        dpg.add_button(label="Cancel", callback=clear_add_alias_dialog_callback)


def edit_alias_callback(sender, app_data):
    global file
    alias = dpg.get_value('edit_alias_alias')
    english = dpg.get_value('edit_alias_english')
    polish = dpg.get_value('edit_alias_polish')
    entry = Alias(alias, english, polish)
    file.aliases[alias] = entry
    add_alias_to_table("alias_table", entry)
    clear_add_alias_dialog_callback(sender, app_data)


def add_to_text_edit(_sender, _app_data, user_data):
    text = dpg.get_value(user_data)
    function = dpg.get_value("edit_alias_function")
    text += function
    dpg.set_value(user_data, text)


def combo_changed_callback_edit(_sender, app_data):
    description = functions[app_data]
    dpg.set_value("alias_edit_function_description", description)


with dpg.window(label='Edit alias', show=False, tag='edit_alias_dialog', width=1000, height=350):
    dpg.add_input_text(label="Alias", tag="edit_alias_alias")
    dpg.add_input_text(label="English", tag="edit_alias_english")
    dpg.add_input_text(label="Polish", tag="edit_alias_polish")
    with dpg.group(horizontal=True):
        with dpg.group():
            dpg.add_combo(label="Function", items=list(functions.keys()), tag="edit_alias_function",
                          callback=combo_changed_callback_edit, )
            dpg.add_text(tag="alias_edit_function_description")
        with dpg.group():
            dpg.add_button(label="Add EN", callback=add_to_text_edit, user_data="edit_alias_english")
            dpg.add_button(label="Add PL", callback=add_to_text_edit, user_data="edit_alias_polish")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Add", callback=edit_alias_callback)
        dpg.add_button(label="Cancel", callback=lambda: dpg.hide_item('edit_alias_dialog'))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Primary Window', True)
dpg.start_dearpygui()
dpg.destroy_context()
