import subprocess
import sys
import os

def run_all():
    # Bước 1: Chạy nhận diện từ Camera (Tạo CamResult.txt)
    print("🚀 BƯỚC 1: Khởi động AI nhận diện phương tiện từ Camera...")
    if os.path.exists("FromCamera.py"):
        subprocess.run([sys.executable, "FromCamera.py"])
    else:
        print("❌ Lỗi: Không tìm thấy file FromCamera.py")
        return

    # Bước 2: Chạy thuật toán tìm đường (Tạo Answer.txt)
    print("\n🚀 BƯỚC 2: Đang phân tích đa nguồn (Camera + GPS) và tối ưu lộ trình...")
    if os.path.exists("main.py"):
        subprocess.run([sys.executable, "main.py"])
    else:
        print("❌ Lỗi: Không tìm thấy file main.py")
        return

    # Bước 3: Kiểm tra và hiển thị kết quả
    if os.path.exists("Answer.txt"):
        print("\n" + "="*50)
        print("🏁 TẤT CẢ ĐÃ HOÀN TẤT!")
        print("📄 Kết quả chi tiết đã được ghi vào file: Answer.txt")
        print("="*50)
        # Tự động mở file kết quả để xem (Windows)
        os.startfile("Answer.txt") 
    else:
        print("\n❌ Lỗi hệ thống: Không thể tạo file Answer.txt")

if __name__ == "__main__":
    run_all()