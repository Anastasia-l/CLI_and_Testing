import flet as ft
import argparse
import io
import contextlib
import file_manager_interface


# Flet app
def main(page: ft.Page):
    page.title = "File Manager GUI"
    page.vertical_alignment = "center"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # File picker
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.update()

    # Command via dropdown
    command_dropdown = ft.Dropdown(label="Choose command", options=[
        ft.dropdown.Option("copy"),
        ft.dropdown.Option("count"),
        ft.dropdown.Option("find"),
        ft.dropdown.Option("creation_date"),
        ft.dropdown.Option("rename_file_with_date"),
        ft.dropdown.Option("rename_folder_with_date"),
        ft.dropdown.Option("rename_files_with_date"),
        ft.dropdown.Option("remove"),
        ft.dropdown.Option("analyze"),
    ],
    width=300,
    )

    command_dropdown_container = ft.Container(
        content=command_dropdown,
        padding=ft.padding.only(right=50)
    )

    # Input Fields
    filename_input = ft.TextField(label="Filename", width=300, visible=False)
    directory_input = ft.TextField(label="Directory name", width=300, visible=False)
    destination_directory_input = ft.TextField(label="Destination directory", width=300, visible=False)
    pattern_input = ft.TextField(label="Pattern", width=300, visible=False)
    full_path_input = ft.TextField(label="Full path to the file", width=300, visible=False)
    folder_path_input = ft.TextField(label="Path to Folder", width=300, visible=False)
    recursive_checkbox = ft.Checkbox(label="Recursive", visible=False)

    pattern_input_container = ft.Container(
        content=pattern_input,
        padding=ft.padding.only(right=50)
    )

    recursive_checkbox_container = ft.Container(
        content=recursive_checkbox,
        padding=ft.padding.only(left=431)
    )

    # Icons for file and folder selection
    filename_icon = ft.IconButton(
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(),
        visible=False,
    )

    directory_icon = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: file_picker.get_directory_path(),
        visible=False,
    )
    destination_directory_icon = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: file_picker.get_directory_path(),
        visible=False,
    )

    folder_icon = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: file_picker.get_directory_path(),
        visible=False
    )
    full_path_icon = ft.IconButton(
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(),
        visible=False,
    )

    # Output Field
    output_field = ft.Text("", size=18, color="blue")

    # Functions to show or hide fields based on the commands chosen
    # Define rows
    filename_row = ft.Row([filename_input, filename_icon], alignment=ft.MainAxisAlignment.CENTER, visible=False)
    directory_row = ft.Row([directory_input, directory_icon], alignment=ft.MainAxisAlignment.CENTER, visible=False)
    folder_row = ft.Row([folder_path_input, folder_icon], alignment=ft.MainAxisAlignment.CENTER, visible=False)
    destination_row = ft.Row([destination_directory_input, destination_directory_icon],
                             alignment=ft.MainAxisAlignment.CENTER, visible=False)
    full_path_row = ft.Row([full_path_input, full_path_icon], alignment=ft.MainAxisAlignment.CENTER, visible=False)

    def update_input_fields(e):
        command = command_dropdown.value
        filename_row.visible = command in ["copy", "remove"]
        directory_row.visible = command in ["count", "remove", "analyze", "find"]
        folder_row.visible = command in ["rename_folder_with_date", "rename_files_with_date"]
        destination_row.visible = command in ["copy"]
        filename_input.visible = command in ["copy", "remove"]
        full_path_row.visible = command in ["creation_date", "rename_file_with_date"]
        full_path_icon.visible = command in ["creation_date", "rename_file_with_date"]
        filename_icon.visible = command in ["copy", "remove"]
        full_path_input.visible = command in ["creation_date", "rename_file_with_date"]
        destination_directory_input.visible = command in ["copy"]
        destination_directory_icon.visible = command in ["copy"]
        directory_input.visible = command in ["count", "remove", "analyze", "find"]
        directory_icon.visible = command in ["copy", "count", "remove", "analyze", "find"]
        pattern_input.visible = command in ["find"]
        folder_path_input.visible = command in ["copy", "rename_folder_with_date", "rename_files_with_date"]
        folder_icon.visible = command in ["rename_folder_with_date", "rename_files_with_date"]
        recursive_checkbox.visible = command in ["rename_files_with_date"]
        page.update()

    command_dropdown.on_change = update_input_fields

    # Functions to execute the command
    def execute_command(e):
        command = command_dropdown.value
        args = argparse.Namespace(
            command=command,
            filename=filename_input.value,
            directory_name=directory_input.value,
            directory=directory_input.value,
            pattern=pattern_input.value,
            full_path=full_path_input.value,
            folder_path=folder_path_input.value,
            destination_path=destination_directory_input.value,
            recursive=recursive_checkbox.value,
        )
        print(f"Args: {args}")

        # Create print output
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            file_manager_interface.handle_command(args)

        # Display the output in the GUI
        output_field.value = output.getvalue()
        page.update()

    # Button to execute the command
    execute_button = ft.ElevatedButton("Execute", on_click=execute_command)
    execute_button_container = ft.Container(
        content=execute_button,
        padding=ft.padding.only(right=80)
    )

    # Handle file_picker results
    def handle_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            filename_input.value = e.files[0].name
            full_path_input.value = e.files[0].path
        if e.path:
            directory_input.value = e.path
            folder_path_input.value = e.path
            destination_directory_input.value = e.path
        page.update()

    file_picker.on_result = handle_file_picker_result

    # Add controls to the page
    content = ft.Column(
        [
            command_dropdown_container,
            filename_row,
            directory_row,
            destination_row,
            pattern_input_container,
            full_path_row,
            folder_row,
            recursive_checkbox_container,
            execute_button_container,
            output_field,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(content)


# Run the app
ft.app(target=main)
