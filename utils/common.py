def check_uploaded_files(data):
    files = []
    for field in data:
        if hasattr(field, 'filename'):
            if field.filename:
                files.append(field)
    return files
