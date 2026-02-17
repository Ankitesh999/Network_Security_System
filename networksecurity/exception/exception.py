import sys

class custom_exception(Exception):
    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = custom_exception.get_detailed_error_message(error_message=error_message, error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_message: str, error_detail) -> str:
        _, _, exc_tb = error_detail.exc_info()
        if exc_tb is None:
            return f"Error occurred with message: {error_message}"
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        detailed_message = f"Error occurred in file: {file_name} at line: {line_number} with message: {error_message}"
        return detailed_message

    def __str__(self):
        return self.error_message

if __name__ == "__main__":
    import sys
    try:
        try:
            # Deliberately cause an error to have real exception context
            x = 1 / 0
        except Exception as e:
            raise custom_exception("This is a custom exception", sys) from e
    except custom_exception as e:
        print(e)