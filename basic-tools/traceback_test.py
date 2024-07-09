import traceback
import io

def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()

try:
    assert False, 'testing assertion'
except Exception as exc:
    error = get_exception_traceback_str(exc)

print("oi", error)
