import networkx as nx
import os

def read_simple_data(file_path):
    """Đọc dữ liệu từ file .txt, tự động lọc tiêu đề và lỗi định dạng"""
    data = {}
    if not os.path.exists(file_path):
        print(f"❌ Lỗi: Không tìm thấy file {file_path}")
        return data
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 2:
                    name = parts[0].strip().upper()
                    val_str = parts[1].strip()
                    try:
                        data[name] = float(val_str)
                    except ValueError:
                        continue 
    return data

def solve_traffic_system():
    # 1. Đọc dữ liệu từ 2 nguồn (Camera và GPS)
    cam_data = read_simple_data("CamResult.txt")
    gps_data = read_simple_data("GpsResult.txt")
    
    if not cam_data or not gps_data:
        print("\n⚠️ HỆ THỐNG CHƯA ĐỦ DỮ LIỆU ĐỂ PHÂN TÍCH")
        return

    # 2. Thiết lập sơ đồ mạng lưới 9 nút (A-I)
    edges = [
        ('A', 'F'), ('F', 'G'), ('B', 'E'), ('E', 'H'), ('C', 'D'), ('D', 'I'),
        ('A', 'B'), ('B', 'C'), ('F', 'E'), ('E', 'D'), ('G', 'H'), ('H', 'I')
    ]

    G = nx.Graph()
    alpha, beta = 0.6, 0.4 # Trọng số: Camera 60%, GPS 40%

    # 3. Tính toán trọng số ùn tắc (Fusion Weight)
    for u, v in edges:
        if u in cam_data and v in cam_data and u in gps_data and v in gps_data:
            avg_cam = (cam_data[u] + cam_data[v]) / 2
            avg_gps = (gps_data[u] + gps_data[v]) / 2
            combined_weight = (avg_cam * alpha) + (avg_gps * beta)
            G.add_edge(u, v, weight=combined_weight)
        else:
            G.add_edge(u, v, weight=999.0)

    # 4. Tìm và sắp xếp các lộ trình từ A đến I
    try:
        all_paths = list(nx.all_simple_paths(G, source='A', target='I'))
        path_options = []
        for path in all_paths:
            total_cost = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
            path_options.append((path, total_cost))

        path_options.sort(key=lambda x: x[1])

        # 5. Ghi kết quả ra file Answer.txt (Quan trọng để run_all.py hoạt động)
        with open("Answer.txt", "w", encoding="utf-8") as f:
            f.write("=== BÁO CÁO ĐIỀU PHỐI GIAO THÔNG TỔNG THỂ ===\n")
            f.write(f"{'XẾP HẠNG':<12} | {'LỘ TRÌNH CHI TIẾT':<40} | {'ĐỘ TẮC'}\n")
            f.write("-" * 75 + "\n")

            for i, (path, cost) in enumerate(path_options):
                rank = "🏆 BEST" if i == 0 else f"Option {i+1}"
                route_str = " -> ".join(path)
                f.write(f"{rank:<12} | {route_str:<40} | {cost:>10.2f}\n")

            f.write("-" * 75 + "\n")
            best_route = " -> ".join(path_options[0][0])
            f.write(f"👉 LỜI KHUYÊN: Lộ trình tối ưu nhất là {best_route}\n")

        print(f"✅ Đã phân tích xong. Lộ trình tốt nhất: {best_route}")
        print("📝 Kết quả đã được lưu vào Answer.txt")

    except nx.NetworkXNoPath:
        print("❌ Không tìm thấy đường đi giữa A và I.")
    except Exception as e:
        print(f"❌ Lỗi xử lý: {e}")

if __name__ == "__main__":
    solve_traffic_system()