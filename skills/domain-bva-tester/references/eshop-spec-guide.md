# Hướng Dẫn Đặc Tả Kỹ Thuật & Nghiệp Vụ Hệ Thống EShop

Tài liệu tham chiếu chuyên sâu dành cho Tester và AI khi thiết kế test case cho hệ thống **EShop SUT** (`https://github.com/ttbhanh/eshop-sut`).

---

## 1. Kiến Trúc Tổng Quan & Môi Trường

Hệ thống EShop là một nền tảng thương mại điện tử đa nền tảng gồm 4 tầng thành phần:

| Thành phần | Công nghệ | Cổng / URL | Trách nhiệm chính |
|---|---|---|---|
| **Backend API** | Node.js, Express, SQLite3, JWT | `http://localhost:3000` | Cung cấp RESTful API, xác thực JWT, tính toán logic giỏ hàng & coupon, máy trạng thái đơn hàng |
| **Frontend Web** | React 18, Vite, Tailwind CSS, Axios | `http://localhost:5173` | Giao diện người mua hàng: xem hàng, giỏ hàng, đặt hàng, áp coupon, lịch sử đơn |
| **Web Admin** | React 18, Vite, Tailwind CSS | `http://localhost:5174` | Giao diện quản trị viên: thống kê dashboard, CRUD sản phẩm/danh mục/coupon, import CSV, quản lý đơn |
| **Mobile App** | React Native, Expo | IP LAN cổng 8081 | Ứng dụng di động cho khách hàng, tương thích Android / iOS |

### Tài khoản mặc định & CSDL (SQLite)
- **Admin**: `admin@eshop.com` / `Admin123!` (Role: `admin`)
- **User test**: `test@eshop.com` / `Test1234!` (Role: `user`)
- **Bảng CSDL cốt lõi**:
  - `users`: `id, name, email, password, role, login_attempts, locked_until, reset_token, shipping_address, phone`
  - `categories`: `id, name`
  - `products`: `id, name, price, description, imageUrl, category_id`
  - `coupons`: `id, code, type ('percent'|'fixed'), discount_value, min_order_amount, expired_at, is_active, max_uses_per_user`
  - `coupon_usage`: `id, coupon_id, user_id, used_at`
  - `orders`: `id, user_id, total_amount, status ('pending'|'confirmed'|'shipping'|'delivered'|'canceled'), shipping_address, created_at`

---

## 1.1 Bốn Tính Năng Trọng Tâm Được Chọn Cho Đồ Án (Selected HW02 Features)

Theo thỏa thuận phân công nhóm và yêu cầu đề bài HW02, bộ test case tập trung kiểm thử 4 tính năng sau:

1. **Pool A: FR-06 — Xem chi tiết sản phẩm (Product Detail View)**
   - **Tệp nguồn SUT:** `frontend-web/src/pages/ProductDetail.jsx`, Backend `server.js` (`GET /api/products/:id`)
   - **Yêu cầu nghiệp vụ:**
     - Hiển thị đầy đủ: Ảnh lớn, Tên, Giá (`₫`), Mô tả, Danh mục (FR-06).
     - Ô nhập số lượng: chỉ nhận số nguyên dương, tối thiểu là 1 (`quantity >= 1`).
     - Bấm nút "Thêm vào giỏ hàng": phản hồi trực quan (toast/badge cập nhật).
     - Breadcrumb điều hướng tại trang chi tiết (FR-23).
     - Nút hành động tích cực dùng màu xanh dương `bg-blue-600` (FR-21).
   - **Lỗi triển khai thực tế trên SUT (Bugs to catch):**
     - *Bug #1:* Nút "Thêm vào giỏ hàng" bị lỗi click đúp (`if (clickCount === 0) return;`) — bấm lần đầu không thêm vào giỏ!
     - *Bug #2:* Ô số lượng `<input type="number">` không chặn số âm, 0, hoặc số thập phân.
     - *Bug #3:* Nút "Thêm vào giỏ hàng" có màu xanh lá (`bg-green-600`), vi phạm FR-21 (phải là xanh dương).
     - *Bug #4:* Không hiển thị tên Danh mục của sản phẩm trên UI (vi phạm FR-06).
     - *Bug #5:* Thiếu thanh điều hướng Breadcrumb (vi phạm FR-23).

2. **Pool B: FR-11 — Xem lịch sử đơn hàng người dùng (Order History View)**
   - **Tệp nguồn SUT:** `frontend-web/src/pages/Profile.jsx`, Backend `server.js` (`GET /api/orders/my-orders`, `PUT /api/orders/:id/cancel`)
   - **Yêu cầu nghiệp vụ:**
     - Chỉ xem được đơn hàng của chính tài khoản đang đăng nhập (User isolation).
     - Hiển thị: Mã đơn (#id), Ngày đặt, Tổng tiền (`₫`), Trạng thái hiện tại.
     - Trạng thái phải dịch sang tiếng Việt rõ ràng và phân biệt màu sắc (`pending`: vàng, `confirmed`: chàm, `shipping`: xanh dương, `delivered`: xanh lá, `canceled`: đỏ).
     - Nút Hủy đơn: Chỉ cho phép hủy khi đơn ở `pending` hoặc `confirmed`. Khi đơn đã sang `shipping`, người dùng **không** được phép tự hủy (chỉ Admin mới có quyền theo FR-10).
   - **Lỗi triển khai thực tế trên SUT (Bugs to catch):**
     - *Bug #1:* Giao diện Web hiển thị nút "Hủy đơn" cho cả đơn đang ở trạng thái `shipping` (`o.status !== "delivered" && o.status !== "canceled"`).
     - *Bug #2:* Backend `server.js` dòng 329 chỉ chặn hủy khi `delivered` hoặc `canceled`, cho phép User gửi API hủy thành công cả đơn hàng `shipping`! (Vi phạm nghiêm trọng State Machine FR-10).

3. **Pool C: FR-15 — Quản lý sản phẩm CRUD trong Web Admin (Product CRUD)**
   - **Tệp nguồn SUT:** `frontend-admin/src/App.jsx`, Backend `server.js` (`GET/POST/PUT/DELETE /api/products`)
   - **Yêu cầu nghiệp vụ:**
     - Admin có thể Thêm / Xem / Sửa / Xóa sản phẩm.
     - Ràng buộc Tên sản phẩm: bắt buộc, tối đa 255 ký tự.
     - Ràng buộc Giá sản phẩm: bắt buộc, phải là số dương (`price > 0`).
     - Danh mục: bắt buộc, phải chọn từ danh mục có sẵn (`category_id`).
     - Ràng buộc tính độc lập: Khi sửa một sản phẩm, chỉ sản phẩm đó bị thay đổi — các sản phẩm khác phải giữ nguyên.
     - Kiểm soát quyền: Bắt buộc có token Admin (FR-12).
   - **Lỗi triển khai thực tế trên SUT (Bugs to catch):**
     - *Bug #1 (Mass Update State):* Khi Admin sửa tên một sản phẩm và lưu thành công, code frontend `App.jsx` chạy `products.map(p => ({ ...p, name: productForm.name }))` làm biến đổi tên của TẤT CẢ sản phẩm trong danh sách hiển thị thành tên của sản phẩm vừa sửa!
     - *Bug #2:* Frontend Form không có validation độ dài 255 ký tự cho tên sản phẩm và không chặn giá 0 hoặc số âm trước khi submit.

4. **Pool D: Lịch sử đơn hàng trên Mobile (Order History in Mobile Device Context)**
   - **Tệp nguồn SUT:** `frontend-mobile/App.js` (Component `renderProfile`, `fetchOrders`, `cancelOrder`)
   - **Yêu cầu nghiệp vụ:**
     - Người dùng đăng nhập xem được toàn bộ danh sách đơn hàng của mình.
     - Hiển thị ngày đặt, tổng tiền, trạng thái đơn hàng tiếng Việt.
     - Nút hủy đơn: Chỉ hiển thị khi đơn ở `pending` hoặc `confirmed`.
   - **Các kịch bản kiểm thử đặc thù di động (Mobile Heuristics):**
     - *Kịch bản mất mạng / Offline:* Khi mất kết nối hoặc IP server không phản hồi, `fetchOrders` bắt lỗi và gán `setOrders([])` dẫn đến màn hình hiện "Bạn chưa có đơn hàng nào." thay vì hiển thị thông báo lỗi mạng kèm nút "Thử lại" (Retry).
     - *Kịch bản thiếu Pull-to-refresh:* Màn hình không có `RefreshControl` để kéo xuống làm mới danh sách đơn khi backend cập nhật trạng thái mới.
     - *Kịch bản đối chiếu Web vs Mobile:* Trên Mobile, nút "Hủy đơn" được ẩn khi đơn ở `shipping` (`o.status === "pending" || o.status === "confirmed"`), trong khi trên Web lại hiển thị! Sự không nhất quán này chứng minh lỗi logic ở tầng Web/Backend.
     - *Kịch bản gián đoạn cuộc gọi / Background:* Khi đang ở màn hình lịch sử đơn hàng, chuyển app sang background hoặc nhận cuộc gọi rồi quay lại -> Ứng dụng phải duy trì token và danh sách đơn.

---

## 2. Danh Mục Yêu Cầu 4 Phân Hệ (Pool A, B, C, D)

### Pool A — Xác Thực, Người Dùng, Danh Mục & Sản Phẩm (Storefront)

- **FR-01: Đăng ký tài khoản**
  - Trường bắt buộc: Họ Tên (`name`), Email (`email`), Mật khẩu (`password`), Xác nhận mật khẩu (`confirmPassword`).
  - Định dạng Email: theo RFC 5322 (`user@domain.com`), tính duy nhất (unique) trong hệ thống.
  - Chính sách mật khẩu mạnh: Tối thiểu 8 ký tự, có ít nhất 1 chữ hoa (`A-Z`), 1 chữ thường (`a-z`), 1 chữ số (`0-9`) và 1 ký tự đặc biệt (`@$!%*?&`).
  - Xác nhận mật khẩu: Phải khớp 100% với mật khẩu đã nhập.
  - Thành công: Chuyển hướng sang `/login`.
  - *Điểm lỗi tiềm ẩn trong code thực tế:* `Register.jsx` dùng regex `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/` (đòi hỏi khoảng trắng `\s` thay vì ký tự đặc biệt) và thiếu trường Xác nhận mật khẩu trên UI!

- **FR-02: Đăng nhập & Khóa tài khoản (Account Lockout)**
  - Đầu vào: Email và Mật khẩu.
  - Đăng nhập sai: Bộ đếm `login_attempts` tăng đúng 1 đơn vị mỗi lần thất bại.
  - Cơ chế khóa: Khi đăng nhập sai từ **3 lần liên tiếp trở lên**, tài khoản bị tạm khóa **30 giây** (`locked_until`).
  - Phản hồi: Thông báo chung an toàn (không lộ email hay mật khẩu sai), báo rõ tài khoản đang bị khóa nếu trong thời gian phạt.
  - Thành công: Trả về JWT Token, reset `login_attempts = 0`, lưu token và role.
  - *Điểm lỗi tiềm ẩn trong code thực tế:* `Login.jsx` hiển thị nhãn "Username" thay vì "Email", tiêu đề trang ghi "Đăng Ký", nút bấm là "Sign In", input mật khẩu để `type="text"`.

- **FR-03: Quên mật khẩu & Đặt lại mật khẩu (2 bước)**
  - Bước 1: Nhập Email -> sinh mã OTP ngẫu nhiên 6 chữ số -> hiển thị Step Indicator "Bước 1 / 2" và nút "Quay lại đăng nhập".
  - Bước 2: Nhập OTP, Mật khẩu mới, Xác nhận mật khẩu mới. Kiểm tra khớp mật khẩu và chính sách mật khẩu mạnh.
  - Ràng buộc: OTP chỉ hợp lệ cho đúng Email yêu cầu, bị vô hiệu sau khi đổi thành công.

- **FR-04: Quản lý hồ sơ cá nhân (Profile)**
  - Cho phép cập nhật: Họ Tên, Số điện thoại (bắt đầu bằng `0`, dài 10–11 chữ số), Địa chỉ giao hàng mặc định.
  - Không cho phép: Thay đổi Email qua UI, sửa đổi thuộc tính `role` (phải giữ nguyên `user`).

- **FR-05: Danh sách & Tìm kiếm sản phẩm**
  - Hiển thị lưới (grid): Ảnh sản phẩm (có thẻ `alt`), Tên sản phẩm, Giá (định dạng `₫` có phân cách hàng nghìn, vd `30.000.000 ₫`).
  - Tìm kiếm theo tên sản phẩm: Không render HTML từ khóa (phòng chống XSS).
  - Trạng thái: Loading spinner khi tải; Empty state khi không có kết quả.
  - Cấu trúc trang: Duy nhất 1 thẻ `<h1>` trên toàn bộ trang.

- **FR-06: Chi tiết sản phẩm**
  - Hiển thị: Ảnh lớn, Tên, Giá, Mô tả, Tên danh mục.
  - Ô số lượng: Chỉ nhận số nguyên dương, tối thiểu là 1.
  - Thao tác: Bấm "Thêm vào giỏ hàng" phải có phản hồi trực quan (Toast hoặc Badge cập nhật).

---

### Pool B — Giỏ Hàng & Thanh Toán (Cart & Checkout)

- **FR-07: Giỏ hàng (Shopping Cart)**
  - Các cột dữ liệu: Sản phẩm, Đơn giá, Số lượng (+ / -), Thành tiền, Thao tác.
  - Hành vi thêm trùng: Tăng số lượng của sản phẩm đó, không thêm dòng mới.
  - Xóa sản phẩm: Bắt buộc bật popup xác nhận (confirm dialog).
  - Điều hướng: Nút "Tiếp tục mua sắm" quay về trang chủ.
  - Nhãn tổng tiền: Bắt buộc là **"Tổng cộng"** (không phải "Tổng tạm tính").
  - Giỏ hàng rỗng: Hiển thị hình minh họa và thông điệp rỗng thân thiện.

- **FR-08: Thanh toán (Checkout)**
  - Điều kiện: Bắt buộc đã đăng nhập (`token` hợp lệ).
  - Tính toán tổng tiền: Server backend phải tự tính toán lại dựa trên ID sản phẩm và số lượng trong CSDL, **không chấp nhận `total_amount` gửi từ client**.
  - Ràng buộc UI: Tổng tiền không cho phép sửa trực tiếp.
  - Thành công: Xóa sạch giỏ hàng client và tạo đơn hàng ở trạng thái `pending`.
  - *Điểm lỗi tiềm ẩn trong code thực tế:* `Checkout.jsx` cho phép user sửa ô `editableTotal` và server backend nhận `total_amount` từ body client!

- **FR-09: Mã giảm giá (Discount Coupon — 5 điều kiện C1..C5)**
  Mã coupon chỉ được áp dụng khi thỏa mãn đồng thời cả 5 điều kiện:
  1. **C1 (Tồn tại & Active):** Mã có trong bảng `coupons` và `is_active = 1`.
  2. **C2 (Còn hạn):** Ngày áp dụng `< expired_at`.
  3. **C3 (Đủ ngưỡng đơn):** Tổng tiền giỏ hàng `total_amount >= min_order_amount`.
  4. **C4 (Đã đăng nhập):** User đã xác thực có JWT token.
  5. **C5 (Chưa hết lượt):** Số lần user đã dùng mã `< max_uses_per_user`.
  - Công thức giảm giá:
    - `percent`: `discount = total * discount_value / 100`
    - `fixed`: `discount = discount_value`
    - `final_amount = max(0, total - discount)`
  - Dữ liệu mẫu kiểm thử:
    - `SAVE10` (percent 10%, min 300.000 ₫, hạn 2099-12-31, 1 lần/user)
    - `BIGBUY` (fixed 50.000 ₫, min 500.000 ₫, hạn 2099-12-31, 1 lần/user)
    - `VIP100` (fixed 100.000 ₫, min 300.000 ₫, hạn 2099-12-31, 2 lần/user)
    - `EXPIRED` (percent 20%, min 100.000 ₫, hạn 2020-01-01, 1 lần/user)

- **FR-10: Máy trạng thái đơn hàng (Order State Machine)**
  - 5 trạng thái: `pending` -> `confirmed` -> `shipping` -> `delivered`.
  - Nhánh hủy: `pending` -> `canceled`; `confirmed` -> `canceled`.
  - Trạng thái kết thúc (Final States): `delivered` và `canceled` không thể chuyển đổi đi đâu.
  - Phân quyền hủy:
    - User và Admin: được hủy khi đơn ở `pending` hoặc `confirmed`.
    - Khi đơn ở `shipping`: User **không** được hủy; chỉ Admin mới có quyền thao tác.
  - Bắt lỗi: Mọi chuyển đổi nhảy cóc hoặc đảo ngược (ví dụ `delivered` -> `pending`, `shipping` -> `confirmed`) đều phải bị từ chối với mã lỗi 400.

- **FR-11: Lịch sử đơn hàng (User)**
  - Phân quyền: User chỉ xem đơn của chính mình.
  - Hiển thị: Mã đơn, Ngày đặt, Tổng tiền, Trạng thái (dịch sang tiếng Việt, màu sắc phân biệt).

---

### Pool C — Quản Trị Hệ Thống (Web Admin)

- **FR-12: Kiểm soát truy cập (Access Control)**
  - Mọi API quản trị (`/api/admin/*`, `POST/PUT/DELETE /api/products`, `/api/categories`, `/api/coupons`) bắt buộc kiểm tra: (1) Token hợp lệ, (2) Claim `role === 'admin'`.
  - Truy cập bằng tài khoản thường (`role: 'user'`) hoặc không token phải bị trả về `401 Unauthorized` hoặc `403 Forbidden`.

- **FR-13: Báo cáo Thống kê (Dashboard)**
  - Tổng doanh thu: **Chỉ cộng dồn `total_amount` của các đơn hàng có `status === 'delivered'`**.
  - Các đơn `pending`, `confirmed`, `shipping`, `canceled` không được tính vào doanh thu.

- **FR-14 & FR-15: Quản lý Danh mục & Sản phẩm (CRUD)**
  - Tên danh mục / Tên sản phẩm: bắt buộc, không được để trống, tên sản phẩm tối đa 255 ký tự.
  - Giá sản phẩm: bắt buộc, phải là số dương (`price > 0`). Không chấp nhận 0, số âm, hoặc chuỗi không phải số.
  - Khi sửa một sản phẩm, tính độc lập phải được bảo đảm (không làm ảnh hưởng sản phẩm khác).

- **FR-16: Import Sản phẩm từ file CSV**
  - Định dạng: Tệp đuôi `.csv`, dòng đầu tiên là header chuẩn `name,price,description,imageUrl,category_id`.
  - Chuẩn RFC 4180: Hỗ trợ trường chứa dấu phẩy khi được bọc trong dấu ngoặc kép `""`.
  - Xác thực dữ liệu dòng: `name` không rỗng, `price` là số dương, `category_id` tồn tại.
  - Tính nguyên tử (Atomic / All-or-Nothing Rollback): Nếu có bất kỳ dòng nào bị lỗi (dù ở dòng cuối cùng), toàn bộ thao tác import phải bị rollback, không một sản phẩm nào được lưu vào CSDL.
  - Báo cáo: Hiển thị số dòng thành công, số dòng thất bại và chi tiết lỗi.

- **FR-17: Quản lý Mã giảm giá (Coupon CRUD)**
  - Ràng buộc: `code` là duy nhất, `discount_value > 0`, `min_order_amount >= 0`, `max_uses_per_user >= 1`.

- **FR-18 & FR-19: Quản lý Đơn hàng & Người dùng**
  - Admin không được phép tự xóa tài khoản của chính mình (`id === current_admin_id`).
  - Địa chỉ giao hàng khi render trong bảng Admin phải được escape an toàn (chống Stored XSS).

---

### Pool D — Ứng Dụng Di Động (React Native / Mobile App)

- **FR-20: Kiểm thử ứng dụng trong môi trường di động**
  - Đầy đủ tính năng người dùng: Danh mục, Chi tiết, Đăng nhập, Giỏ hàng, Đặt hàng, Hủy đơn.
  - **Các kịch bản đặc thù của môi trường Mobile**:
    1. *Gián đoạn hệ thống (Interruptions)*: Cuộc gọi đến, tin nhắn đẩy, chuyển đổi ứng dụng khi đang ở bước thanh toán hoặc nhập OTP.
    2. *Bàn phím ảo (Virtual Keyboard)*: Bàn phím che khuất nút "Thanh toán" hoặc ô "Mật khẩu" mà màn hình không cuộn được (KeyboardAvoidingView).
    3. *Kết nối mạng yếu / Mất mạng đột ngột*: Mất kết nối khi đang gửi request thanh toán, timeout, retry không gây nhân đôi đơn hàng (Idempotency).
    4. *Kích thước màn hình & Cảm ứng*: Vùng chạm (touch target) tối thiểu 44x44 dp, tràn viền màn hình (Safe Area Notch / Dynamic Island).
    5. *Đồng bộ trạng thái*: Giỏ hàng và lịch sử đơn hàng đồng bộ chính xác với Backend web.

---

## 3. Tiêu Chuẩn Giao Diện & Bảo Mật (GUI & Security Standards)

| Mã | Tên tiêu chuẩn | Quy tắc kiểm tra cốt lõi |
|---|---|---|
| **FR-21** | Tiêu chuẩn GUI chung | Giao diện 100% tiếng Việt; nút Submit/Mua màu xanh dương, nút Hủy màu đỏ; đơn vị tiền tệ `₫` phân cách hàng nghìn; đúng 1 thẻ `<h1>` mỗi trang; Tab order từ trên xuống, trái sang phải |
| **FR-22** | Form Requirements | Trường bắt buộc có dấu `*`; email dùng `type="email"`; mật khẩu dùng `type="password"`; thông báo lỗi hiển thị **phía trên** nút submit; form đa bước có Step Indicator |
| **FR-23** | Navigation Requirements | Thanh navbar highlight trang đang active; icon Giỏ hàng có badge số lượng; nút đăng xuất ghi đúng chữ "Đăng xuất"; Breadcrumb ở các trang con |
| **FR-24** | Feedback & State | Toast/Badge sau khi thêm giỏ; Dialog xác nhận khi xóa sản phẩm; Empty State có icon và thông điệp; Ảnh có thuộc tính `alt` |
| **SEC-01** | Lưu mật khẩu | Không lưu plaintext, phải hash an toàn |
| **SEC-02..03** | Xác thực & Phân quyền | Kiểm tra JWT token và claim role admin ở tầng backend |
| **SEC-04..05** | Chống XSS & SQLi | Escape dữ liệu user trên DOM; Dùng Parameterized Query trong SQLite |
| **SEC-06..07** | Chống giả mạo role & OTP | Chặn cập nhật role từ payload client; OTP đủ độ dài ngẫu nhiên và hết hạn |
