# Script to fix permissions in Android package
# This is useful if you encounter permission issues with files

def fix_android_permissions():
    try:
        from jnius import autoclass
        
        # Get Android activity
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        
        # Request permissions
        if activity:
            # Add necessary permission requests here if needed
            pass
            
        return True
    except Exception as e:
        print(f"Error setting Android permissions: {e}")
        return False


# This function is called by main.py when running on Android
def setup_android():
    fix_android_permissions()