import networkx as nx
import os

def read_simple_data(file_path):
    """Đọc dữ liệu từ các file .txt (Cam, Gps, Location)"""
    data = {}
    if not os.path.exists(file_path):
        print(f"❌ Lỗi: Không tìm thấy file {file_path}")
        return data
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 2:
                    key = parts[0].strip().upper()
                    value = parts[1].strip()
                    # Nếu là dữ liệu số thì chuyển sang float, nếu không giữ nguyên string
                    try:
                        data[key] = float(value)
                    except ValueError:
                        data[key] = value
    return data

def solve_traffic_system():
    # 1. Thu thập dữ liệu
    cam_data = read_simple_data("CamResult.txt")
    gps_data = read_simple_data("GpsResult.txt")
    loc_map = read_simple_data("location.txt")
    
    if not cam_data or not gps_data:
        print("\n⚠️ HỆ THỐNG THIẾU DỮ LIỆU ĐẦU VÀO")
        return

    # 2. Thiết lập sơ đồ mạng lưới
    edges = [
        ('A', 'F'), ('F', 'G'), ('B', 'E'), ('E', 'H'), ('C', 'D'), ('D', 'I'),
        ('A', 'B'), ('B', 'C'), ('F', 'E'), ('E', 'D'), ('G', 'H'), ('H', 'I')
    ]

    G = nx.Graph()
    alpha, beta = 0.6, 0.4 

    for u, v in edges:
        if all(node in cam_data and node in gps_data for node in [u, v]):
            avg_cam = (cam_data[u] + cam_data[v]) / 2
            avg_gps = (gps_data[u] + gps_data[v]) / 2
            weight = (avg_cam * alpha) + (avg_gps * beta)
            G.add_edge(u, v, weight=weight)
        else:
            G.add_edge(u, v, weight=999.0)

    # 3. Tìm và xử lý lộ trình
    try:
        all_paths = list(nx.all_simple_paths(G, source='A', target='I'))
        path_options = []
        for path in all_paths:
            cost = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
            path_options.append((path, cost))

        path_options.sort(key=lambda x: x[1])

        # 4. Ghi kết quả ra Answer.txt với tên địa điểm thực tế
        with open("Answer.txt", "w", encoding="utf-8") as f:
            f.write("=== BÁO CÁO ĐIỀU PHỐI GIAO THÔNG TỔNG THỂ ===\n")
            f.write(f"{'XẾP HẠNG':<12} | {'LỘ TRÌNH CHI TIẾT':<60} | {'ĐỘ TẮC'}\n")
            f.write("-" * 90 + "\n")

            for i, (path, cost) in enumerate(path_options):
                rank = "🏆 BEST" if i == 0 else f"Option {i+1}"
                
                # Chuyển đổi chữ cái sang tên địa điểm từ loc_map
                named_path = [loc_map.get(node, node) for node in path]
                route_str = " -> ".join(named_path)
                
                f.write(f"{rank:<12} | {route_str:<60} | {cost:>10.2f}\n")

            f.write("-" * 90 + "\n")
            best_named_path = " -> ".join([loc_map.get(node, node) for node in path_options[0][0]])
            f.write(f"👉 LỜI KHUYÊN: Lộ trình tối ưu nhất là {best_named_path}\n")

        print(f"✅ Đã hoàn tất! Lộ trình tốt nhất: {best_named_path}")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    solve_traffic_system()