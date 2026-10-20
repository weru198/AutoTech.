import os
import tempfile


def get_temp_files():
    """
    Scan the Windows temporary directory and return
    files that can potentially be cleaned.
    """

    temp_folder = tempfile.gettempdir()

    files = []

    for root, dirs, filenames in os.walk(temp_folder):

        for filename in filenames:

            file_path = os.path.join(root, filename)

            try:
                if os.path.isfile(file_path):

                    size = os.path.getsize(file_path)

                    files.append({
                        "name": filename,
                        "path": file_path,
                        "size": size
                    })

            except (PermissionError, OSError):
                continue

    return files


def get_cleanup_summary():
    """
    Return a summary of temporary files.
    """

    files = get_temp_files()

    total_size = sum(
        file["size"]
        for file in files
    )

    return {
        "temp_folder": tempfile.gettempdir(),
        "file_count": len(files),
        "total_size": total_size,
        "files": files
    }


def format_size(size):

    if size < 1024:
        return f"{size} B"

    if size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"

    if size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"

    return f"{size / (1024 ** 3):.2f} GB"


def clean_selected_files(selected_paths):
    """
    Remove only selected files inside the system temp directory.
    Skips directories, inaccessible files, and paths outside temp.
    """

    import os
    import tempfile

    temp_root = os.path.realpath(tempfile.gettempdir())
    results = {
        "deleted": 0,
        "skipped": 0,
        "errors": []
    }

    for path in selected_paths:

        try:
            real_path = os.path.realpath(path)

            # Ensure the file is inside the temp directory.
            if os.path.commonpath([temp_root, real_path]) != temp_root:
                results["skipped"] += 1
                continue

            # Only remove regular files, not directories or links.
            if os.path.islink(path) or not os.path.isfile(path):
                results["skipped"] += 1
                continue

            os.remove(path)
            results["deleted"] += 1

        except (OSError, ValueError):
            results["skipped"] += 1
            results["errors"].append(os.path.basename(path))

    return results

if __name__ == "__main__":
    main()