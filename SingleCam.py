from ultralytics import YOLO
import cv2

# 1. Tải mô hình YOLO26
model = YOLO("yolo26s.pt")

# 2. Định nghĩa các lớp phương tiện (car, motorcycle, bus, truck)
VEHICLE_CLASSES = [2, 3, 5, 7]

# 3. Mở file video
cap = cv2.VideoCapture("a.mp4")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 4. Chạy nhận diện (không dùng show=True ở đây để ta tự vẽ thêm thông báo)
    results = model.predict(frame, classes=VEHICLE_CLASSES, conf=0.3, verbose=False)
    
    # 5. Vẽ khung (Bounding Boxes) lên frame
    # results[0].plot() trả về một hình ảnh đã được vẽ sẵn các khung nhận diện
    annotated_frame = results[0].plot()

    # 6. Tính toán mức độ ùn tắc
    vehicle_count = len(results[0].boxes)
    
    if vehicle_count < 5:
        status = "Thong thoang"
        color = (0, 255, 0)  # Xanh lá
    elif vehicle_count <= 15:
        status = "Mat do vua"
        color = (0, 255, 255) # Vàng
    else:
        status = "UN TAC NGIEM TRONG!"
        color = (0, 0, 255) # Đỏ

    # 7. Vẽ bảng thông báo mức độ ùn tắc lên góc màn hình
    # Tạo một hình chữ nhật nền phía sau chữ cho dễ đọc
    cv2.rectangle(annotated_frame, (10, 10), (450, 120), (0, 0, 0), -1) 
    cv2.putText(annotated_frame, f"So luong xe: {vehicle_count}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(annotated_frame, f"Trang thai: {status}", (20, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # 8. Hiển thị kết quả
    cv2.imshow("YOLO26 - Traffic Congestion Report", annotated_frame)

    # Thoát nếu nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
