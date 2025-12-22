import configparser
import os
import pathlib

CURRENT_FILE_PATH = pathlib.Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE_PATH.parent.parent
CONFIG_FILE_PATH = PROJECT_ROOT / 'config.ini'

SCREENSHOT_ON = False


def load_config():
    """
    Đọc file config.ini và cập nhật biến global SCREENSHOT_ON.
    """
    global SCREENSHOT_ON
    config = configparser.ConfigParser()

    print(f"DEBUG: Đường dẫn file dự kiến: {CONFIG_FILE_PATH}")

    # --- ĐOẠN CODE KIỂM TRA MỚI ---
    files_read = config.read(CONFIG_FILE_PATH)
    
    if not files_read:
        # Nếu danh sách file đọc được trống, tức là file không được tìm thấy
        print(f"❌ Error: Không thể đọc file cấu hình. Đường dẫn có vẻ sai hoặc file trống. Path: {CONFIG_FILE_PATH}")
        SCREENSHOT_ON = False
        return
    # -----------------------------
    
    try:
        # Nếu đọc thành công (files_read không rỗng)
        
        # Kiểm tra xem Section có tồn tại không
        if not config.has_section('Settings'):
            print("❌ Error: Section [Settings] không tồn tại trong file config.ini.")
            SCREENSHOT_ON = False 
            return

        # Lấy giá trị boolean 
        SCREENSHOT_ON = config.getboolean('Settings', 'screenshot_on', fallback=False)
        
        raw_value = config.get('Settings', 'screenshot_on', fallback='False')
        print(f"DEBUG: Giá trị thô đọc được: '{raw_value}'")

        print(f"✅ Config loaded: SCREENSHOT_ON = {SCREENSHOT_ON}")

    except configparser.Error as e:
        print(f"❌ Error parsing config file: Lỗi cú pháp trong file. {e}")
        SCREENSHOT_ON = False


# Gọi hàm để load cấu hình khi module được import
load_config()