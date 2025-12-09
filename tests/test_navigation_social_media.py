from pages.login_page import LoginPage


# "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
# 1. Mở trang OrangeHRM Login
# 2. Xác định các biểu tượng mở tab mới
#     * Ở trang login, tìm các biểu tượng (icons) ở footer (ví dụ: LinkedIn, Facebook, Twitter, YouTube – hoặc các icon mạng xã hội đang hiển thị trên trang).
#     * Mỗi biểu tượng khi click vào sẽ mở một tab mới (một Page mới trong Playwright).
# 3. Lần lượt click từng biểu tượng để mở tab mới
#     * Từ trang login, click vào biểu tượng thứ 1 → chờ tab mới mở ra.
#     * Lưu lại đối tượng Page tương ứng với tab mới này (không được bỏ qua, sẽ dùng để chuyển tab sau).
#     * Làm tương tự cho các biểu tượng còn lại cho đến khi:
#         * Tất cả các biểu tượng yêu cầu trong bài tập đã được click,
#         * Và tương ứng là các tab mới đã được mở.
# 4. Verify nội dung heading trên mỗi tab mới
#     * Với mỗi tab mới:
#         * Dùng bring_to_front() để chuyển tab đó thành tab đang active.
#             * Ví dụ: new_page.bring_to_front()
#         * Xác định một heading chính trên trang mới (ví dụ: <h1>, <h2>, hoặc một tiêu đề lớn rõ ràng).
#         * Thực hiện assert:
#             * Kiểm tra heading hiển thị đúng và tồn tại.
#             * Nếu có thể, so sánh text với giá trị mong đợi (ví dụ: “OrangeHRM”, “LinkedIn”, “Facebook”, v.v. – tùy vào trang thực tế).
#     * Sau khi verify xong một tab:
#         * Không đóng tab vội, nhưng hãy đảm bảo bạn có thể chuyển qua lại giữa các tab bằng bring_to_front().
# 5. Quay lại trang chủ OrangeHRM Login để tiếp tục
#     * Sau khi xử lý xong 1 tab, hãy dùng:
#         * login_page.bring_to_front() (hoặc đối tượng Page tương ứng với tab login ban đầu) để quay trở lại tab OrangeHRM login.
#     * Từ tab login:
#         * Tiếp tục mở tab mới từ biểu tượng tiếp theo.
#     * Lặp lại cho đến khi tất cả các biểu tượng yêu cầu trong bài tập:
#         * Đã được click.
#         * Tab tương ứng đã được mở, verify, và có thể switch qua lại bằng bring_to_front()."