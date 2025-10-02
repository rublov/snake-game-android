# Script to fix permissions in Android package
# This is useful if you encounter permission issues with files

def fix_android_permissions() -> bool:
    try:
        from jnius import autoclass

        # Get Android activity
        python_activity = autoclass("org.kivy.android.PythonActivity")
        activity = python_activity.mActivity

        # Request permissions
        if activity:
            # Add necessary permission requests here if needed
            pass

        return True
    except Exception as exc:
        print(f"Error setting Android permissions: {exc}")
        return False


# This function is called by main.py when running on Android
def setup_android() -> None:
    fix_android_permissions()
