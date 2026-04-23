from ultralytics import YOLO
import cv2
import os

def process_traffic_fast():
    # 1. Khởi tạo
    model = YOLO("yolo26s.pt")
    VEHICLE_CLASSES = [2, 3, 5, 7] 
    save_path = r"C:\CODE\CamResult.txt"
    video_files = ['a.mp4', 'b.mp4', 'c.mp4', 'd.mp4', 'e.mp4', 'f.mp4', 'g.mp4', 'h.mp4', 'i.mp4']
    results_summary = {}

    print("⚡ Đang khởi động chế độ xử lý siêu tốc (Fast Mode - 5x)...")

    for video_name in video_files:
        if not os.path.exists(video_name):
            print(f"⚠️ Không tìm thấy: {video_name}")
            continue
        
        cap = cv2.VideoCapture(video_name)
        total_vehicles = 0
        analyzed_frames = 0
        frame_idx = 0
        
        print(f"🎬 Phân tích {video_name}...", end=" ", flush=True)
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            
            # Chỉ xử lý mỗi frame thứ 5 để tăng tốc 5 lần
            if frame_idx % 5 == 0:
                results = model.predict(frame, classes=VEHICLE_CLASSES, conf=0.3, verbose=False)
                total_vehicles += len(results[0].boxes)
                analyzed_frames += 1
            
            frame_idx += 1
            
        cap.release()
        
        avg_vehicles = total_vehicles / analyzed_frames if analyzed_frames > 0 else 0
        point_name = video_name.split('.')[0].upper()
        results_summary[point_name] = round(avg_vehicles, 2)
        print(f"Hoàn tất (TB: {results_summary[point_name]})")

    # 2. Ghi kết quả và ép lưu xuống đĩa (flush)
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write("BAO CAO LUU LUONG GIAO THONG TU CAMERA\n")
            f.write("-" * 40 + "\n")
            f.write(f"{'Diem Nut':<10} | {'So xe trung binh':<20}\n")
            f.write("-" * 40 + "\n")
            
            for point in sorted(results_summary.keys()):
                f.write(f"{point:<10} | {results_summary[point]:<20}\n")
            
            f.flush() # Ép hệ điều hành ghi dữ liệu ngay lập tức
            os.fsync(f.fileno()) # Đảm bảo file không bị trống khi chương trình kết thúc
            
        print(f"\n✅ Đã xuất dữ liệu thành công ra: {save_path}")
    except Exception as e:
        print(f"❌ Lỗi ghi file: {e}")

if __name__ == "__main__":
    process_traffic_fast()