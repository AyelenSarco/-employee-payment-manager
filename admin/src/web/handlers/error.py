from flask import render_template 

def handle_error(code, message, description):
    error = {
        "code": code,
        "message": message,
        "description": description
    }
    return render_template("error.html", error=error), code

# 400 Handler- Bad request
def bad_request(e):
    return handle_error(400, "Bad Request", "Your request is invalid. Please verify the information and try again.")

# 404 Handler- Not found
def not_found(error):
    return handle_error(404, "Not Found", "The page you’re looking for couldn’t be found.")

# 401 Handler - Unauthorized
def unauthorized(e):
    return handle_error(401, "Unauthorized", "You’re not authorized to view this page.")

# 403 Handler - Forbidden
def forbidden(e):
    return handle_error(403, "Forbidden", "You don’t have permission to access this resource.")

# 500 Handler- Internal Server Error
def internal_error(e):
    return handle_error(500, "Internal Server Error", "An internal server error occurred. Please try again later.")

# 504 Handler - Timeout
def timeout(e):
    return handle_error(504, "Timeout Error", "The operation timed out and was cancelled. Please try again.")

def register_error_handlers(app):
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)
    app.register_error_handler(504, timeout)
    

