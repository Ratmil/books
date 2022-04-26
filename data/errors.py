ERROR_UNKNOWN=-1
ERROR_OK=0
ERROR_INVALID_BOOK_TITLE=1
ERROR_INVALID_BOOK_ISBN=2
ERROR_INVALID_USER_NAME=3
ERROR_INVALID_COMMENT_SUBJECT=4
ERROR_INVALID_COMMENT_TEXT=5
ERROR_COMMENT_NOT_FOUND=6
ERROR_BOOK_NOT_FOUND=7
ERROR_SAVING_BOOK=8
 
ERRORS_LIST = ["No error",
               "Book title too short",
               "ISBN too short",
               "User name too short",
               "Comment subject is too short",
               "Comment text is too short, 30 characters or more",
               "Comment not found",
               "Book not found"]

def getErrorMsg(error_code: int, error_msg=""):
    if error_code >= 0 and error_code < len(ERRORS_LIST):
        return {
            'error_code': error_code,
            'error_msg': ERRORS_LIST[error_code]
        }
    else:
        return {
            'error_code': error_code,
            'error_msg': error_msg
        }