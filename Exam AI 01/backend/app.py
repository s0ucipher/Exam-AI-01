import os
import subprocess
import sys

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from organizer import organize_folder, organize_sources, save_organized_copy


load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app": "NeuroSort AI"})


def _normalize_selected_path(path):
    normalized = path.strip()
    if normalized != "/":
        normalized = normalized.rstrip("/")
    return normalized


def _run_macos_dialog(script):
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )

    if result.returncode != 0:
        raise ValueError("Selection cancelled.")

    return [_normalize_selected_path(line) for line in result.stdout.splitlines() if line.strip()]


def _select_files_with_macos_dialog():
    script = """
set selectedItems to choose file with prompt "Select files for NeuroSort AI" with multiple selections allowed
set output to ""
repeat with selectedItem in selectedItems
    set output to output & POSIX path of selectedItem & linefeed
end repeat
return output
"""
    return _run_macos_dialog(script)


def _select_folders_with_macos_dialog():
    script = """
set selectedItems to choose folder with prompt "Select folders for NeuroSort AI" with multiple selections allowed
set output to ""
repeat with selectedItem in selectedItems
    set output to output & POSIX path of selectedItem & linefeed
end repeat
return output
"""
    return _run_macos_dialog(script)


def _select_destination_with_macos_dialog():
    script = 'POSIX path of (choose folder with prompt "Select an output folder for NeuroSort AI")'
    return _run_macos_dialog(script)[0]


def _select_files_with_tkinter():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected_paths = filedialog.askopenfilenames(title="Select files for NeuroSort AI")
    root.destroy()

    if not selected_paths:
        raise ValueError("Selection cancelled.")

    return [_normalize_selected_path(path) for path in selected_paths]


def _select_folder_with_tkinter(title):
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected_path = filedialog.askdirectory(title=title)
    root.destroy()

    if not selected_path:
        raise ValueError("Selection cancelled.")

    return _normalize_selected_path(selected_path)


@app.route("/select-folder", methods=["GET"])
@app.route("/api/select-folder", methods=["GET"])
def select_folder():
    try:
        if sys.platform == "darwin":
            selected_path = _select_destination_with_macos_dialog()
        else:
            selected_path = _select_folder_with_tkinter("Select a folder for NeuroSort AI")
        return jsonify({"path": selected_path})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(f"Error selecting folder: {str(error)}")
        return jsonify({"error": "Could not open the folder picker."}), 500


@app.route("/select-files", methods=["GET"])
@app.route("/api/select-files", methods=["GET"])
def select_files():
    try:
        if sys.platform == "darwin":
            selected_paths = _select_files_with_macos_dialog()
        else:
            selected_paths = _select_files_with_tkinter()
        return jsonify({"paths": selected_paths})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(f"Error selecting files: {str(error)}")
        return jsonify({"error": "Could not open the file picker."}), 500


@app.route("/select-folders", methods=["GET"])
@app.route("/api/select-folders", methods=["GET"])
def select_folders():
    try:
        if sys.platform == "darwin":
            selected_paths = _select_folders_with_macos_dialog()
        else:
            selected_paths = [_select_folder_with_tkinter("Select a folder for NeuroSort AI")]
        return jsonify({"paths": selected_paths})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(f"Error selecting folders: {str(error)}")
        return jsonify({"error": "Could not open the folder picker."}), 500


@app.route("/select-destination", methods=["GET"])
@app.route("/api/select-destination", methods=["GET"])
def select_destination():
    try:
        if sys.platform == "darwin":
            selected_path = _select_destination_with_macos_dialog()
        else:
            selected_path = _select_folder_with_tkinter("Select an output folder for NeuroSort AI")
        return jsonify({"path": selected_path})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(f"Error selecting destination: {str(error)}")
        return jsonify({"error": "Could not open the destination picker."}), 500


@app.route("/organize", methods=["POST"])
@app.route("/api/organize", methods=["POST"])
def organize():
    data = request.json or {}
    sources = data.get("sources")
    path = data.get("path", "")
    destination_path = data.get("destinationPath") or None
    sort_by = data.get("sortBy", "name")
    apply_changes = bool(data.get("applyChanges", False))

    try:
        if sources:
            result = organize_sources(
                sources,
                sort_by=sort_by,
                apply_changes=apply_changes,
                destination_path=destination_path,
            )
        else:
            result = organize_folder(path, sort_by=sort_by, apply_changes=apply_changes)
        return jsonify(result)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(f"Error organizing folder: {str(error)}")
        return jsonify({"error": "An error occurred while organizing files."}), 500


@app.route("/save-organized", methods=["POST"])
@app.route("/api/save-organized", methods=["POST"])
def save_organized():
    data = request.json or {}
    sources = data.get("sources") or []
    sort_by = data.get("sortBy", "name")
    destination_path = data.get("destinationPath") or None
    save_mode = data.get("saveMode", "downloads")

    try:
        result = save_organized_copy(
            sources,
            sort_by=sort_by,
            destination_path=destination_path,
            save_mode=save_mode,
        )
        return jsonify(result)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(f"Error saving organized files: {str(error)}")
        return jsonify({"error": "An error occurred while saving organized files."}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5050"))
    app.run(host="0.0.0.0", debug=True, port=port, use_reloader=False)
