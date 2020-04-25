# secret key for generating tokens
SECRET_KEY = 'super-secret-password'

# upload folder (must be a folder in the "./app" directory)
UPLOAD_FOLDER = 'tmp_attachments'

# allowed extensions
ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])

# maximum size of upload
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
