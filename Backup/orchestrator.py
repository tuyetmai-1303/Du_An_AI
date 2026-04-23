import networkx as nx
import os

def read_data(file_path):
    """Hàm đọc dữ liệu từ file kết quả (hỗ trợ cả Cam và Gps)"""
    data = {}
    if not os.path.exists(file_path):
        return data
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 2:
                    try:
                        name = parts[0].strip().upper()
                        value = float(parts[1].strip())
                        data[name] = value
                    except ValueError:
                        continue
    return data

def run_system_and_export():
    print("--- 🚦 ĐANG KHỞI CHẠY HỆ THỐNG ĐIỀU PHỐI TỔNG THỂ ---")
    
    # 1. Thu thập dữ liệu từ các file kết quả
    cam_data = read_data("CamResult.txt")
    gps_data = read_data("GpsResult.txt")

    if not cam_data or not gps_data:
        print("❌ Lỗi: Không thể đọc dữ liệu từ CamResult.txt hoặc GpsResult.txt")
        return

    # 2. Thiết lập sơ đồ mạng lưới (Edges) dựa trên hình ảnh sơ đồ 9 nút
    connections = [
        ('A', 'F'), ('F', 'G'), ('B', 'E'), ('E', 'H'), ('C', 'D'), ('D', 'I'),
        ('A', 'B'), ('B', 'C'), ('F', 'E'), ('E', 'D'), ('G', 'H'), ('H', 'I')
    ]

    G = nx.Graph()
    alpha, beta = 0.6, 0.4 # 60% Camera, 40% GPS

    for u, v in connections:
        if u in cam_data and v in cam_data and u in gps_data and v in gps_data:
            avg_cam = (cam_data[u] + cam_data[v]) / 2
            avg_gps = (gps_data[u] + gps_data[v]) / 2
            weight = (avg_cam * alpha) + (avg_gps * beta)
            G.add_edge(u, v, weight=weight)
        else:
            G.add_edge(u, v, weight=999.0)

    # 3. Tìm tất cả lộ trình và tính toán chi phí
    try:
        all_paths = list(nx.all_simple_paths(G, source='A', target='I'))
        path_options = []
        for path in all_paths:
            cost = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
            path_options.append((path, cost))

        # Sắp xếp từ tốt nhất đến tệ nhất
        path_options.sort(key=lambda x: x[1])

        # 4. Xuất kết quả ra file Answer.txt
        with open("Answer.txt", "w", encoding="utf-8") as f:
            f.write("=== KẾT QUẢ PHÂN TÍCH LỘ TRÌNH TỐI ƯU ===\n")
            f.write(f"{'HẠNG':<10} | {'LỘ TRÌNH CHI TIẾT':<35} | {'ĐỘ TẮC'}\n")
            f.write("-" * 65 + "\n")
            
            for i, (path, cost) in enumerate(path_options):
                rank = "🏆 BEST" if i == 0 else f"Option {i+1}"
                route_str = " -> ".join(path)
                f.write(f"{rank:<10} | {route_str:<35} | {cost:.2f}\n")
            
            f.write("-" * 65 + "\n")
            f.write(f"👉 LỜI KHUYÊN: Đi theo lộ trình {' -> '.join(path_options[0][0])}\n")

        print("✅ Đã xuất kết quả thành công ra file Answer.txt")
        print(f"🌟 Lộ trình tốt nhất: {' -> '.join(path_options[0][0])}")

    except Exception as e:
        print(f"❌ Có lỗi xảy ra trong quá trình xử lý: {e}")

if __name__ == "__main__":
    run_system_and_export()