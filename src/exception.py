import sys       # Any exception is getting controlled sys library will have that information.
                #The sys module gives access to system-specific functions and variables.      
#_, _, exc_tb = “ignore first two values, store only the traceback object in exc_tb.”
#It’s purely tuple unpacking syntax, _ is a placeholder for unused values.

def error_message_details(error,error_detail: sys):  #error_detail: sys parameter-This is just the sys module passed into the function.t is used to call sys.exc_info().
    _,_,exc_tb = error_detail.exc_info()
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        exc_tb.tb_frame.f_code.co_filename,
        exc_tb.tb_lineno,str(error)
    )
    return error_message

#error_message_details - This formats a detailed error message from an exception.
#BUT it only works if an exception has already occurred — otherwise sys.exc_info() will return (None, None, None) and there’s no traceback to fetch.
#This function does not raise or handle exceptions by itself; it just formats info about a caught exception.)    

class CustomException(Exception):    # Custom exception class that inherits from the built-in Exception class.
    def __init__(self,error_message,error_detail: sys):
        super().__init__(error_message)  # Call the parent class constructor with the error message.
        self.error_message = error_message_details(error_message,error_detail)  # Store the formatted error message.

def __str__(self):
    return self.error_message

# class CustomException - This wraps the exception into a custom class.
#It allows you to raise the exception again but with a detailed, formatted message.
#he __str__ method ensures that when you print the exception, you see the detailed message.
#_str__ method in Python is called when you convert an object to a string