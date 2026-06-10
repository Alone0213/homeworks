"""
家具城进销存管理系统 — Flask Web 应用
=======================================
技术栈: Flask + SQLite + Bootstrap 5 + Jinja2
数据库引擎: SQLite (可无缝切换 MySQL)

核心功能:
  7张数据表的 CRUD 操作
  入库/销售自动更新库存 (应用层实现触发器逻辑)
  库存盘点视图
  时间段入库/销售统计
"""

import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "furniture_management_secret_key_2024"

# ── 数据库路径 ──
DB_PATH = os.path.join(os.path.dirname(__file__), "furniture.db")


# ==================== 数据库层封装 ====================
def get_db():
    """获取数据库连接 (每次请求独立)"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  # 启用外键约束
    return conn


def init_db():
    """初始化数据库 — 建表 + 预置测试数据"""
    conn = get_db()
    cur = conn.cursor()

    # ── 1. 建表 (与 MySQL 版本保持语义一致) ──
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS FurnitureCategory (
            CategoryID   INTEGER PRIMARY KEY AUTOINCREMENT,
            CategoryName TEXT NOT NULL UNIQUE,
            Description  TEXT
        );

        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierID    INTEGER PRIMARY KEY AUTOINCREMENT,
            SupplierName  TEXT NOT NULL,
            ContactPerson TEXT,
            Phone         TEXT NOT NULL,
            Address       TEXT,
            Email         TEXT
        );

        CREATE TABLE IF NOT EXISTS Customer (
            CustomerID   INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerName TEXT NOT NULL,
            Phone        TEXT NOT NULL,
            Address      TEXT,
            Email        TEXT
        );

        CREATE TABLE IF NOT EXISTS Furniture (
            FurnitureID   INTEGER PRIMARY KEY AUTOINCREMENT,
            FurnitureName TEXT NOT NULL,
            CategoryID    INTEGER NOT NULL REFERENCES FurnitureCategory(CategoryID),
            SupplierID    INTEGER NOT NULL REFERENCES Supplier(SupplierID),
            UnitPrice     REAL NOT NULL,
            Stock         INTEGER NOT NULL DEFAULT 0,
            Description   TEXT
        );

        CREATE TABLE IF NOT EXISTS WarehouseEntry (
            EntryID     INTEGER PRIMARY KEY AUTOINCREMENT,
            FurnitureID INTEGER NOT NULL REFERENCES Furniture(FurnitureID),
            EntryDate   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            Quantity    INTEGER NOT NULL,
            UnitPrice   REAL NOT NULL,
            Remarks     TEXT
        );

        CREATE TABLE IF NOT EXISTS Sales (
            SaleID      INTEGER PRIMARY KEY AUTOINCREMENT,
            FurnitureID INTEGER NOT NULL REFERENCES Furniture(FurnitureID),
            CustomerID  INTEGER NOT NULL REFERENCES Customer(CustomerID),
            SaleDate    TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            Quantity    INTEGER NOT NULL,
            UnitPrice   REAL NOT NULL,
            Remarks     TEXT
        );

        CREATE TABLE IF NOT EXISTS Receipt (
            ReceiptID     INTEGER PRIMARY KEY AUTOINCREMENT,
            SaleID        INTEGER NOT NULL REFERENCES Sales(SaleID),
            ReceiptDate   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            Amount        REAL NOT NULL,
            PaymentMethod TEXT DEFAULT '现金',
            Remarks       TEXT
        );
    """)

    # ── 2. 预置测试数据 (仅首次) ──
    if cur.execute("SELECT COUNT(*) FROM FurnitureCategory").fetchone()[0] == 0:
        cur.executescript("""
            INSERT INTO FurnitureCategory VALUES
            (1,'沙发','各类布艺/皮质沙发'),
            (2,'床','各类双人/单人床'),
            (3,'餐桌','各类餐桌及配套桌椅'),
            (4,'书桌','各类办公/学习书桌'),
            (5,'柜子','衣柜/书柜/储物柜等'),
            (6,'椅子','各类座椅/休闲椅');

            INSERT INTO Supplier VALUES
            (1,'光明家具厂','张经理','13800138001','广东省佛山市顺德区','gm@guangming.com'),
            (2,'红星家具集团','李总','13900139002','江苏省苏州市相城区','hongxing@163.com'),
            (3,'大自然家居','王经理','13700137003','浙江省杭州市余杭区','nature@nature.com'),
            (4,'北欧风尚家具','赵经理','13600136004','上海市青浦区','beiou@beiou.com');

            INSERT INTO Customer VALUES
            (1,'李明','13888880001','北京市朝阳区','liming@qq.com'),
            (2,'王芳','13999990002','上海市浦东新区','wangfang@163.com'),
            (3,'张伟','13777770003','广州市天河区','zhangwei@gmail.com'),
            (4,'四季酒店','40088880001','深圳市南山区','siji@hotel.com'),
            (5,'阳光地产公司','0755-88889999','东莞市南城区','yg@yg.com');

            INSERT INTO Furniture VALUES
            (1,'真皮三人沙发',1,1,3800.00,10,'进口头层牛皮，实木框架'),
            (2,'布艺双人沙发',1,2,2200.00,15,'棉麻面料，高回弹海绵'),
            (3,'实木双人床',2,3,4500.00,8,'北美白橡木，环保清漆'),
            (4,'现代简约大床',2,4,3200.00,12,'E0级板材，简约设计'),
            (5,'大理石餐桌(1.5m)',3,2,2800.00,10,'天然大理石，实木桌腿'),
            (6,'实木书桌',4,3,1800.00,20,'进口胡桃木，手工打磨'),
            (7,'四门衣柜',5,1,5200.00,6,'实木框架，推拉门设计'),
            (8,'办公椅',6,4,800.00,25,'人体工学设计，升降旋转'),
            (9,'休闲躺椅',6,2,1500.00,10,'可调节角度，舒适靠垫'),
            (10,'茶几',1,3,1200.00,18,'钢化玻璃面，实木边框');

            INSERT INTO WarehouseEntry VALUES
            (1,1,'2024-01-05 09:00:00',20,3200.00,'首次进货'),
            (2,2,'2024-01-06 10:00:00',25,1800.00,'新款到货'),
            (3,3,'2024-01-08 11:00:00',15,3800.00,'厂家促销'),
            (4,4,'2024-01-10 14:00:00',18,2600.00,NULL),
            (5,5,'2024-01-12 09:30:00',15,2200.00,'新年采购'),
            (6,6,'2024-01-15 10:00:00',30,1400.00,NULL),
            (7,7,'2024-01-18 13:00:00',10,4500.00,'高端系列'),
            (8,8,'2024-02-01 09:00:00',40,600.00,'批量采购'),
            (9,9,'2024-02-05 14:00:00',20,1200.00,NULL),
            (10,10,'2024-02-10 10:00:00',25,900.00,'新款茶几');

            INSERT INTO Sales VALUES
            (1,1,1,'2024-01-20 15:00:00',1,3800.00,'家庭使用'),
            (2,2,2,'2024-01-22 16:00:00',2,2200.00,'新房装修'),
            (3,5,4,'2024-02-01 10:00:00',5,2800.00,'酒店采购'),
            (4,3,3,'2024-02-05 11:00:00',1,4500.00,'主卧配置'),
            (5,6,1,'2024-02-10 14:00:00',2,1800.00,'书房布置'),
            (6,8,5,'2024-02-15 09:00:00',10,800.00,'办公区批量'),
            (7,10,2,'2024-03-01 16:00:00',2,1200.00,'客厅配置'),
            (8,9,3,'2024-03-05 15:00:00',1,1500.00,'阳台休闲'),
            (9,4,4,'2024-03-10 10:00:00',3,3200.00,'酒店套房'),
            (10,2,5,'2024-03-15 14:00:00',3,2200.00,'员工宿舍');

            INSERT INTO Receipt VALUES
            (1,1,'2024-01-20 15:30:00',3800.00,'微信','已付清'),
            (2,2,'2024-01-22 16:20:00',4400.00,'刷卡','全款'),
            (3,3,'2024-02-01 11:00:00',14000.00,'转账','对公转账'),
            (4,4,'2024-02-05 11:30:00',4500.00,'现金','已付清'),
            (5,5,'2024-02-10 14:30:00',3600.00,'支付宝',NULL),
            (6,6,'2024-02-15 09:30:00',8000.00,'转账','月结'),
            (7,7,'2024-03-01 16:30:00',2400.00,'微信','已付清'),
            (8,8,'2024-03-05 15:20:00',1500.00,'现金',NULL),
            (9,9,'2024-03-10 10:30:00',9600.00,'转账','部分付款'),
            (10,10,'2024-03-15 14:30:00',6600.00,'刷卡','全款');
        """)

    conn.commit()
    conn.close()


# ==================== 核心业务逻辑 ====================

def update_stock_after_entry(furniture_id, old_qty=0, new_qty=0):
    """
    入库后自动更新库存 (替代 MySQL 触发器的功能)
    应用层实现，保证跨数据库兼容
    """
    conn = get_db()
    conn.execute(
        "UPDATE Furniture SET Stock = Stock - ? + ? WHERE FurnitureID = ?",
        (old_qty, new_qty, furniture_id),
    )
    conn.commit()
    conn.close()


def update_stock_after_sale(furniture_id, old_qty=0, new_qty=0):
    """
    销售后自动更新库存 (替代 MySQL 触发器的功能)
    应用层实现，保证跨数据库兼容
    """
    conn = get_db()
    conn.execute(
        "UPDATE Furniture SET Stock = Stock + ? - ? WHERE FurnitureID = ?",
        (old_qty, new_qty, furniture_id),
    )
    conn.commit()
    conn.close()


# ==================== 路由 — 页面 ====================

@app.route("/")
def index():
    """仪表盘首页"""
    conn = get_db()
    stats = {
        "categories": conn.execute("SELECT COUNT(*) FROM FurnitureCategory").fetchone()[0],
        "suppliers": conn.execute("SELECT COUNT(*) FROM Supplier").fetchone()[0],
        "customers": conn.execute("SELECT COUNT(*) FROM Customer").fetchone()[0],
        "furniture": conn.execute("SELECT COUNT(*) FROM Furniture").fetchone()[0],
        "entries": conn.execute("SELECT COUNT(*) FROM WarehouseEntry").fetchone()[0],
        "sales": conn.execute("SELECT COUNT(*) FROM Sales").fetchone()[0],
        "receipts": conn.execute("SELECT COUNT(*) FROM Receipt").fetchone()[0],
        "total_stock": conn.execute("SELECT SUM(Stock) FROM Furniture").fetchone()[0],
        "low_stock": conn.execute("SELECT COUNT(*) FROM Furniture WHERE Stock < 5").fetchone()[0],
        # 收支统计
        "total_income": conn.execute(
            "SELECT COALESCE(SUM(Quantity * UnitPrice), 0) FROM Sales"
        ).fetchone()[0],
        "total_expense": conn.execute(
            "SELECT COALESCE(SUM(Quantity * UnitPrice), 0) FROM WarehouseEntry"
        ).fetchone()[0],
        "total_receipt": conn.execute(
            "SELECT COALESCE(SUM(Amount), 0) FROM Receipt"
        ).fetchone()[0],
        "sales_count": conn.execute("SELECT COUNT(*) FROM Sales").fetchone()[0],
        "entry_count": conn.execute("SELECT COUNT(*) FROM WarehouseEntry").fetchone()[0],
    }
    conn.close()
    return render_template("index.html", stats=stats)


# ── 家具类型 CRUD ──
@app.route("/categories")
def list_categories():
    conn = get_db()
    rows = conn.execute("SELECT * FROM FurnitureCategory ORDER BY CategoryID").fetchall()
    conn.close()
    return render_template("categories.html", rows=rows)

@app.route("/categories/add", methods=["POST"])
def add_category():
    conn = get_db()
    try:
        conn.execute("INSERT INTO FurnitureCategory (CategoryName, Description) VALUES (?,?)",
                      (request.form["name"], request.form["desc"]))
        conn.commit()
        flash("家具类型添加成功", "success")
    except Exception as e:
        flash(f"添加失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_categories"))

@app.route("/categories/delete/<int:id>")
def delete_category(id):
    conn = get_db()
    try:
        conn.execute("DELETE FROM FurnitureCategory WHERE CategoryID=?", (id,))
        conn.commit()
        flash("删除成功", "success")
    except Exception as e:
        flash(f"删除失败 (可能被家具引用): {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_categories"))


# ── 供应商 CRUD ──
@app.route("/suppliers")
def list_suppliers():
    conn = get_db()
    rows = conn.execute("SELECT * FROM Supplier ORDER BY SupplierID").fetchall()
    conn.close()
    return render_template("suppliers.html", rows=rows)

@app.route("/suppliers/add", methods=["POST"])
def add_supplier():
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO Supplier (SupplierName, ContactPerson, Phone, Address, Email) VALUES (?,?,?,?,?)",
            (request.form["name"], request.form["contact"], request.form["phone"],
             request.form["address"], request.form["email"]))
        conn.commit()
        flash("供应商添加成功", "success")
    except Exception as e:
        flash(f"添加失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_suppliers"))

@app.route("/suppliers/delete/<int:id>")
def delete_supplier(id):
    conn = get_db()
    try:
        conn.execute("DELETE FROM Supplier WHERE SupplierID=?", (id,))
        conn.commit()
        flash("删除成功", "success")
    except Exception as e:
        flash(f"删除失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_suppliers"))


# ── 客户 CRUD ──
@app.route("/customers")
def list_customers():
    conn = get_db()
    rows = conn.execute("SELECT * FROM Customer ORDER BY CustomerID").fetchall()
    conn.close()
    return render_template("customers.html", rows=rows)

@app.route("/customers/add", methods=["POST"])
def add_customer():
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO Customer (CustomerName, Phone, Address, Email) VALUES (?,?,?,?)",
            (request.form["name"], request.form["phone"],
             request.form["address"], request.form["email"]))
        conn.commit()
        flash("客户添加成功", "success")
    except Exception as e:
        flash(f"添加失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_customers"))

@app.route("/customers/delete/<int:id>")
def delete_customer(id):
    conn = get_db()
    try:
        conn.execute("DELETE FROM Customer WHERE CustomerID=?", (id,))
        conn.commit()
        flash("删除成功", "success")
    except Exception as e:
        flash(f"删除失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_customers"))


# ── 家具 CRUD (关联类型和供应商) ──
@app.route("/furniture")
def list_furniture():
    conn = get_db()
    rows = conn.execute("""
        SELECT f.*, c.CategoryName, s.SupplierName
        FROM Furniture f
        JOIN FurnitureCategory c ON f.CategoryID = c.CategoryID
        JOIN Supplier s ON f.SupplierID = s.SupplierID
        ORDER BY f.FurnitureID
    """).fetchall()
    categories = conn.execute("SELECT * FROM FurnitureCategory").fetchall()
    suppliers = conn.execute("SELECT * FROM Supplier").fetchall()
    conn.close()
    return render_template("furniture.html", rows=rows, categories=categories, suppliers=suppliers)

@app.route("/furniture/add", methods=["POST"])
def add_furniture():
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO Furniture (FurnitureName, CategoryID, SupplierID, UnitPrice, Stock, Description) VALUES (?,?,?,?,?,?)",
            (request.form["name"], request.form["category"], request.form["supplier"],
             request.form["price"], request.form["stock"], request.form["desc"]))
        conn.commit()
        flash("家具添加成功", "success")
    except Exception as e:
        flash(f"添加失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_furniture"))

@app.route("/furniture/delete/<int:id>")
def delete_furniture(id):
    conn = get_db()
    try:
        conn.execute("DELETE FROM Furniture WHERE FurnitureID=?", (id,))
        conn.commit()
        flash("删除成功", "success")
    except Exception as e:
        flash(f"删除失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_furniture"))


# ── 入库管理 (自动更新库存) ──
@app.route("/warehouse")
def list_warehouse_entries():
    conn = get_db()
    rows = conn.execute("""
        SELECT w.*, f.FurnitureName
        FROM WarehouseEntry w
        JOIN Furniture f ON w.FurnitureID = f.FurnitureID
        ORDER BY w.EntryID DESC
    """).fetchall()
    furniture = conn.execute("SELECT * FROM Furniture ORDER BY FurnitureName").fetchall()
    categories = conn.execute("SELECT * FROM FurnitureCategory ORDER BY CategoryName").fetchall()
    suppliers = conn.execute("SELECT * FROM Supplier ORDER BY SupplierName").fetchall()
    conn.close()
    return render_template("warehouse.html", rows=rows, furniture=furniture,
                           categories=categories, suppliers=suppliers)

@app.route("/warehouse/add", methods=["POST"])
def add_warehouse_entry():
    conn = get_db()
    try:
        fid = int(request.form["furniture"])
        qty = int(request.form["quantity"])
        price = float(request.form["price"])
        cur = conn.execute("SELECT UnitPrice FROM Furniture WHERE FurnitureID=?", (fid,))
        f = cur.fetchone()
        if not f:
            flash("家具不存在", "danger")
            conn.close()
            return redirect(url_for("list_warehouse_entries"))
        conn.execute(
            "INSERT INTO WarehouseEntry (FurnitureID, EntryDate, Quantity, UnitPrice, Remarks) VALUES (?, datetime('now','localtime'), ?, ?, ?)",
            (fid, qty, price, request.form.get("remarks", "")))
        # ★ 应用层模拟触发器：入库 → 增加库存
        conn.execute("UPDATE Furniture SET Stock = Stock + ? WHERE FurnitureID = ?", (qty, fid))
        conn.commit()
        flash(f"入库成功，库存已自动增加 {qty}", "success")
    except Exception as e:
        flash(f"入库失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_warehouse_entries"))

@app.route("/warehouse/delete/<int:id>")
def delete_warehouse_entry(id):
    conn = get_db()
    try:
        row = conn.execute("SELECT FurnitureID, Quantity FROM WarehouseEntry WHERE EntryID=?", (id,)).fetchone()
        if row:
            # ★ 应用层模拟触发器：删除入库 → 回退库存
            conn.execute("UPDATE Furniture SET Stock = Stock - ? WHERE FurnitureID = ?",
                         (row["Quantity"], row["FurnitureID"]))
            conn.execute("DELETE FROM WarehouseEntry WHERE EntryID=?", (id,))
            conn.commit()
            flash("入库记录已删除，库存已自动回退", "success")
    except Exception as e:
        flash(f"删除失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_warehouse_entries"))


# ── 快速创建 API (AJAX，用于入库弹窗内联创建) ──

@app.route("/api/supplier/quick_add", methods=["POST"])
def api_quick_add_supplier():
    """快速创建供应商，返回 JSON {success, id, name}"""
    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO Supplier (SupplierName, ContactPerson, Phone, Address, Email) VALUES (?,?,?,?,?)",
            (request.form["name"], request.form.get("contact", ""),
             request.form["phone"], request.form.get("address", ""),
             request.form.get("email", "")))
        conn.commit()
        new_id = cur.lastrowid
        return {"success": True, "id": new_id, "name": request.form["name"]}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


@app.route("/api/furniture/quick_add", methods=["POST"])
def api_quick_add_furniture():
    """快速创建家具，返回 JSON {success, id, name}"""
    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO Furniture (FurnitureName, CategoryID, SupplierID, UnitPrice, Stock, Description) VALUES (?,?,?,?,0,?)",
            (request.form["name"], request.form["category"], request.form["supplier"],
             request.form["price"], request.form.get("desc", "")))
        conn.commit()
        new_id = cur.lastrowid
        return {"success": True, "id": new_id, "name": request.form["name"]}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


@app.route("/api/customer/quick_add", methods=["POST"])
def api_quick_add_customer():
    """快速创建客户，返回 JSON {success, id, name}"""
    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO Customer (CustomerName, Phone, Address, Email) VALUES (?,?,?,?)",
            (request.form["name"], request.form["phone"],
             request.form.get("address", ""), request.form.get("email", "")))
        conn.commit()
        new_id = cur.lastrowid
        return {"success": True, "id": new_id, "name": request.form["name"]}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


# ── 销售管理 (自动更新库存) ──
@app.route("/sales")
def list_sales():
    conn = get_db()
    rows = conn.execute("""
        SELECT s.*, f.FurnitureName, c.CustomerName
        FROM Sales s
        JOIN Furniture f ON s.FurnitureID = f.FurnitureID
        JOIN Customer c ON s.CustomerID = c.CustomerID
        ORDER BY s.SaleID DESC
    """).fetchall()
    furniture = conn.execute("SELECT * FROM Furniture ORDER BY FurnitureName").fetchall()
    customers = conn.execute("SELECT * FROM Customer ORDER BY CustomerName").fetchall()
    categories = conn.execute("SELECT * FROM FurnitureCategory ORDER BY CategoryName").fetchall()
    suppliers = conn.execute("SELECT * FROM Supplier ORDER BY SupplierName").fetchall()
    conn.close()
    return render_template("sales.html", rows=rows, furniture=furniture, customers=customers,
                           categories=categories, suppliers=suppliers)

@app.route("/sales/add", methods=["POST"])
def add_sale():
    conn = get_db()
    try:
        fid = int(request.form["furniture"])
        cid = int(request.form["customer"])
        qty = int(request.form["quantity"])
        price = float(request.form["price"])
        cur = conn.execute("SELECT Stock FROM Furniture WHERE FurnitureID=?", (fid,))
        f = cur.fetchone()
        if not f:
            flash("家具不存在", "danger")
            conn.close()
            return redirect(url_for("list_sales"))
        if f["Stock"] < qty:
            flash(f"库存不足！当前库存: {f['Stock']}，需要: {qty}", "danger")
            conn.close()
            return redirect(url_for("list_sales"))
        conn.execute(
            "INSERT INTO Sales (FurnitureID, CustomerID, SaleDate, Quantity, UnitPrice, Remarks) VALUES (?, ?, datetime('now','localtime'), ?, ?, ?)",
            (fid, cid, qty, price, request.form.get("remarks", "")))
        # ★ 应用层模拟触发器：销售 → 减少库存
        conn.execute("UPDATE Furniture SET Stock = Stock - ? WHERE FurnitureID = ?", (qty, fid))
        conn.commit()
        flash(f"销售成功，库存已自动减少 {qty}", "success")
    except Exception as e:
        flash(f"销售失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_sales"))

@app.route("/sales/delete/<int:id>")
def delete_sale(id):
    conn = get_db()
    try:
        row = conn.execute("SELECT FurnitureID, Quantity FROM Sales WHERE SaleID=?", (id,)).fetchone()
        if row:
            conn.execute("UPDATE Furniture SET Stock = Stock + ? WHERE FurnitureID = ?",
                         (row["Quantity"], row["FurnitureID"]))
            conn.execute("DELETE FROM Sales WHERE SaleID=?", (id,))
            conn.commit()
            flash("销售记录已删除，库存已自动回退", "success")
    except Exception as e:
        flash(f"删除失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_sales"))


# ── 收款管理 ──
@app.route("/receipts")
def list_receipts():
    conn = get_db()
    rows = conn.execute("""
        SELECT r.*, f.FurnitureName, c.CustomerName
        FROM Receipt r
        JOIN Sales s ON r.SaleID = s.SaleID
        JOIN Furniture f ON s.FurnitureID = f.FurnitureID
        JOIN Customer c ON s.CustomerID = c.CustomerID
        ORDER BY r.ReceiptID DESC
    """).fetchall()
    sales = conn.execute("""
        SELECT s.SaleID, f.FurnitureName, c.CustomerName,
               s.Quantity * s.UnitPrice AS TotalAmount,
               s.SaleDate
        FROM Sales s
        JOIN Furniture f ON s.FurnitureID = f.FurnitureID
        JOIN Customer c ON s.CustomerID = c.CustomerID
        ORDER BY s.SaleID
    """).fetchall()
    conn.close()
    return render_template("receipts.html", rows=rows, sales=sales)


@app.route("/api/sale/paid/<int:sale_id>")
def api_sale_paid(sale_id):
    """AJAX: 查询某销售的已收总金额"""
    conn = get_db()
    row = conn.execute(
        "SELECT COALESCE(SUM(Amount), 0) AS paid FROM Receipt WHERE SaleID=?", (sale_id,)
    ).fetchone()
    conn.close()
    return {"paid": row["paid"]}


@app.route("/receipts/add", methods=["POST"])
def add_receipt():
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO Receipt (SaleID, ReceiptDate, Amount, PaymentMethod, Remarks) VALUES (?, datetime('now','localtime'), ?, ?, ?)",
            (request.form["sale"], request.form["amount"],
             request.form["method"], request.form.get("remarks", "")))
        conn.commit()
        flash("收款记录添加成功", "success")
    except Exception as e:
        flash(f"添加失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_receipts"))

@app.route("/receipts/delete/<int:id>")
def delete_receipt(id):
    conn = get_db()
    try:
        conn.execute("DELETE FROM Receipt WHERE ReceiptID=?", (id,))
        conn.commit()
        flash("删除成功", "success")
    except Exception as e:
        flash(f"删除失败: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("list_receipts"))


# ── 库存盘点视图 ──
@app.route("/stock")
def stock_view():
    conn = get_db()
    rows = conn.execute("""
        SELECT f.*, c.CategoryName, s.SupplierName
        FROM Furniture f
        JOIN FurnitureCategory c ON f.CategoryID = c.CategoryID
        JOIN Supplier s ON f.SupplierID = s.SupplierID
        ORDER BY f.FurnitureID
    """).fetchall()
    conn.close()
    return render_template("stock.html", rows=rows)


# ── 统计查询 (模拟存储过程) ──
@app.route("/statistics", methods=["GET", "POST"])
def statistics():
    """时间段入库/销售统计 —— 对应 MySQL 存储过程 sp_InventoryStatistics"""
    results = None
    start_date = end_date = ""
    if request.method == "POST":
        start_date = request.form["start"]
        end_date = request.form["end"] + " 23:59:59"
        conn = get_db()
        results = conn.execute("""
            SELECT
                f.FurnitureID,
                f.FurnitureName,
                fc.CategoryName,
                s.SupplierName,
                COALESCE(in_stats.total_in, 0) AS total_in,
                COALESCE(sale_stats.total_sale, 0) AS total_sale,
                f.UnitPrice,
                f.Stock
            FROM Furniture f
            JOIN FurnitureCategory fc ON f.CategoryID = fc.CategoryID
            JOIN Supplier s ON f.SupplierID = s.SupplierID
            LEFT JOIN (
                SELECT FurnitureID, SUM(Quantity) AS total_in
                FROM WarehouseEntry
                WHERE EntryDate BETWEEN ? AND ?
                GROUP BY FurnitureID
            ) in_stats ON f.FurnitureID = in_stats.FurnitureID
            LEFT JOIN (
                SELECT FurnitureID, SUM(Quantity) AS total_sale
                FROM Sales
                WHERE SaleDate BETWEEN ? AND ?
                GROUP BY FurnitureID
            ) sale_stats ON f.FurnitureID = sale_stats.FurnitureID
            ORDER BY f.FurnitureID
        """, (start_date, end_date, start_date, end_date)).fetchall()
        conn.close()
    return render_template("statistics.html", results=results, start=start_date, end=end_date)


if __name__ == "__main__":
    init_db()
    print("=" * 50)
    print("  家具城进销存管理系统")
    print("  访问地址: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)
