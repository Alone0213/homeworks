-- ============================================================
-- 家具城进销存管理系统 数据库脚本
-- 数据库名称：FurnitureDB
-- ============================================================

-- ==================== 1. 创建数据库 ====================
CREATE DATABASE IF NOT EXISTS FurnitureDB
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE FurnitureDB;

-- ==================== 2. 创建基础表 ====================

-- 2.1 家具类型表
CREATE TABLE IF NOT EXISTS FurnitureCategory (
    CategoryID       INT AUTO_INCREMENT PRIMARY KEY COMMENT '家具类型编号',
    CategoryName     VARCHAR(50)  NOT NULL UNIQUE COMMENT '类型名称',
    Description      VARCHAR(200) DEFAULT NULL COMMENT '类型描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='家具类型表';

-- 2.2 供应商信息表
CREATE TABLE IF NOT EXISTS Supplier (
    SupplierID       INT AUTO_INCREMENT PRIMARY KEY COMMENT '供应商编号',
    SupplierName     VARCHAR(100) NOT NULL COMMENT '供应商名称',
    ContactPerson    VARCHAR(50)  DEFAULT NULL COMMENT '联系人',
    Phone            VARCHAR(20)  NOT NULL COMMENT '联系电话',
    Address          VARCHAR(200) DEFAULT NULL COMMENT '地址',
    Email            VARCHAR(100) DEFAULT NULL COMMENT '邮箱'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='供应商信息表';

-- 2.3 客户信息表
CREATE TABLE IF NOT EXISTS Customer (
    CustomerID       INT AUTO_INCREMENT PRIMARY KEY COMMENT '客户编号',
    CustomerName     VARCHAR(100) NOT NULL COMMENT '客户名称',
    Phone            VARCHAR(20)  NOT NULL COMMENT '联系电话',
    Address          VARCHAR(200) DEFAULT NULL COMMENT '地址',
    Email            VARCHAR(100) DEFAULT NULL COMMENT '邮箱'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户信息表';

-- 2.4 家具信息表
CREATE TABLE IF NOT EXISTS Furniture (
    FurnitureID      INT AUTO_INCREMENT PRIMARY KEY COMMENT '家具编号',
    FurnitureName    VARCHAR(100) NOT NULL COMMENT '家具名称',
    CategoryID       INT          NOT NULL COMMENT '所属类型编号',
    SupplierID       INT          NOT NULL COMMENT '供应商编号',
    UnitPrice        DECIMAL(10,2) NOT NULL COMMENT '单价',
    Stock            INT          NOT NULL DEFAULT 0 COMMENT '当前库存数量',
    Description      VARCHAR(500) DEFAULT NULL COMMENT '家具描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='家具信息表';

-- 2.5 入库记录表
CREATE TABLE IF NOT EXISTS WarehouseEntry (
    EntryID          INT AUTO_INCREMENT PRIMARY KEY COMMENT '入库编号',
    FurnitureID      INT          NOT NULL COMMENT '家具编号',
    EntryDate        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入库日期',
    Quantity         INT          NOT NULL COMMENT '入库数量',
    UnitPrice        DECIMAL(10,2) NOT NULL COMMENT '入库单价',
    TotalAmount      DECIMAL(12,2) GENERATED ALWAYS AS (Quantity * UnitPrice) STORED COMMENT '入库总金额',
    Remarks          VARCHAR(200) DEFAULT NULL COMMENT '备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='入库记录表';

-- 2.6 销售记录表
CREATE TABLE IF NOT EXISTS Sales (
    SaleID           INT AUTO_INCREMENT PRIMARY KEY COMMENT '销售编号',
    FurnitureID      INT          NOT NULL COMMENT '家具编号',
    CustomerID       INT          NOT NULL COMMENT '客户编号',
    SaleDate         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '销售日期',
    Quantity         INT          NOT NULL COMMENT '销售数量',
    UnitPrice        DECIMAL(10,2) NOT NULL COMMENT '销售单价',
    TotalAmount      DECIMAL(12,2) GENERATED ALWAYS AS (Quantity * UnitPrice) STORED COMMENT '销售总金额',
    Remarks          VARCHAR(200) DEFAULT NULL COMMENT '备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='销售记录表';

-- 2.7 收款记录表
CREATE TABLE IF NOT EXISTS Receipt (
    ReceiptID        INT AUTO_INCREMENT PRIMARY KEY COMMENT '收款编号',
    SaleID           INT          NOT NULL COMMENT '关联销售编号',
    ReceiptDate      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '收款日期',
    Amount           DECIMAL(12,2) NOT NULL COMMENT '收款金额',
    PaymentMethod    VARCHAR(30)  DEFAULT '现金' COMMENT '支付方式（现金/刷卡/转账/支付宝/微信）',
    Remarks          VARCHAR(200) DEFAULT NULL COMMENT '备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收款记录表';

-- ==================== 3. 建立参照完整性约束（外键） ====================

-- 3.1 家具表 → 家具类型表
ALTER TABLE Furniture
    ADD CONSTRAINT FK_Furniture_Category
    FOREIGN KEY (CategoryID) REFERENCES FurnitureCategory(CategoryID)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- 3.2 家具表 → 供应商表
ALTER TABLE Furniture
    ADD CONSTRAINT FK_Furniture_Supplier
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- 3.3 入库表 → 家具表
ALTER TABLE WarehouseEntry
    ADD CONSTRAINT FK_WarehouseEntry_Furniture
    FOREIGN KEY (FurnitureID) REFERENCES Furniture(FurnitureID)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- 3.4 销售表 → 家具表
ALTER TABLE Sales
    ADD CONSTRAINT FK_Sales_Furniture
    FOREIGN KEY (FurnitureID) REFERENCES Furniture(FurnitureID)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- 3.5 销售表 → 客户表
ALTER TABLE Sales
    ADD CONSTRAINT FK_Sales_Customer
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- 3.6 收款表 → 销售表
ALTER TABLE Receipt
    ADD CONSTRAINT FK_Receipt_Sales
    FOREIGN KEY (SaleID) REFERENCES Sales(SaleID)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- ==================== 4. 创建触发器 ====================

-- 4.1 入库后自动增加库存
DELIMITER //

CREATE TRIGGER trg_WarehouseEntry_AfterInsert
AFTER INSERT ON WarehouseEntry
FOR EACH ROW
BEGIN
    UPDATE Furniture
    SET Stock = Stock + NEW.Quantity
    WHERE FurnitureID = NEW.FurnitureID;
END//

-- 4.2 删除入库记录时自动扣减库存
CREATE TRIGGER trg_WarehouseEntry_AfterDelete
AFTER DELETE ON WarehouseEntry
FOR EACH ROW
BEGIN
    UPDATE Furniture
    SET Stock = Stock - OLD.Quantity
    WHERE FurnitureID = OLD.FurnitureID;
END//

-- 4.3 修改入库记录时自动调整库存（先还原旧值，再增加新值）
CREATE TRIGGER trg_WarehouseEntry_AfterUpdate
AFTER UPDATE ON WarehouseEntry
FOR EACH ROW
BEGIN
    UPDATE Furniture
    SET Stock = Stock - OLD.Quantity + NEW.Quantity
    WHERE FurnitureID = NEW.FurnitureID;
END//

-- 4.4 销售后自动减少库存
CREATE TRIGGER trg_Sales_AfterInsert
AFTER INSERT ON Sales
FOR EACH ROW
BEGIN
    UPDATE Furniture
    SET Stock = Stock - NEW.Quantity
    WHERE FurnitureID = NEW.FurnitureID;
END//

-- 4.5 删除销售记录时自动增加库存（还原）
CREATE TRIGGER trg_Sales_AfterDelete
AFTER DELETE ON Sales
FOR EACH ROW
BEGIN
    UPDATE Furniture
    SET Stock = Stock + OLD.Quantity
    WHERE FurnitureID = OLD.FurnitureID;
END//

-- 4.6 修改销售记录时自动调整库存
CREATE TRIGGER trg_Sales_AfterUpdate
AFTER UPDATE ON Sales
FOR EACH ROW
BEGIN
    UPDATE Furniture
    SET Stock = Stock + OLD.Quantity - NEW.Quantity
    WHERE FurnitureID = NEW.FurnitureID;
END//

DELIMITER ;

-- ==================== 5. 创建存储过程 ====================

-- 存储过程：统计某段时间内各种商品的入库数量和销售数量
-- 参数：startDate 开始日期, endDate 结束日期
DELIMITER //

CREATE PROCEDURE sp_InventoryStatistics(
    IN startDate DATETIME,
    IN endDate   DATETIME
)
BEGIN
    SELECT
        f.FurnitureID          AS '家具编号',
        f.FurnitureName        AS '家具名称',
        fc.CategoryName        AS '家具类型',
        s.SupplierName         AS '供应商',
        IFNULL(in_stats.TotalInQty, 0)  AS '入库总数量',
        IFNULL(sale_stats.TotalSaleQty, 0) AS '销售总数量',
        f.UnitPrice            AS '当前单价',
        f.Stock                AS '当前库存'
    FROM Furniture f
    LEFT JOIN FurnitureCategory fc ON f.CategoryID = fc.CategoryID
    LEFT JOIN Supplier s ON f.SupplierID = s.SupplierID
    LEFT JOIN (
        SELECT FurnitureID, SUM(Quantity) AS TotalInQty
        FROM WarehouseEntry
        WHERE EntryDate BETWEEN startDate AND endDate
        GROUP BY FurnitureID
    ) in_stats ON f.FurnitureID = in_stats.FurnitureID
    LEFT JOIN (
        SELECT FurnitureID, SUM(Quantity) AS TotalSaleQty
        FROM Sales
        WHERE SaleDate BETWEEN startDate AND endDate
        GROUP BY FurnitureID
    ) sale_stats ON f.FurnitureID = sale_stats.FurnitureID
    ORDER BY f.FurnitureID;
END//

DELIMITER ;

-- ==================== 6. 插入测试数据 ====================

-- 6.1 家具类型
INSERT INTO FurnitureCategory (CategoryName, Description) VALUES
('沙发', '各类布艺/皮质沙发'),
('床', '各类双人/单人床'),
('餐桌', '各类餐桌及配套桌椅'),
('书桌', '各类办公/学习书桌'),
('柜子', '衣柜/书柜/储物柜等'),
('椅子', '各类座椅/休闲椅');

-- 6.2 供应商
INSERT INTO Supplier (SupplierName, ContactPerson, Phone, Address, Email) VALUES
('光明家具厂', '张经理', '13800138001', '广东省佛山市顺德区乐从镇', 'gm@guangming.com'),
('红星家具集团', '李总', '13900139002', '江苏省苏州市相城区', 'hongxing@163.com'),
('大自然家居', '王经理', '13700137003', '浙江省杭州市余杭区', 'nature@nature.com'),
('北欧风尚家具', '赵经理', '13600136004', '上海市青浦区', 'beiou@beiou.com');

-- 6.3 客户
INSERT INTO Customer (CustomerName, Phone, Address, Email) VALUES
('李明', '13888880001', '北京市朝阳区', 'liming@qq.com'),
('王芳', '13999990002', '上海市浦东新区', 'wangfang@163.com'),
('张伟', '13777770003', '广州市天河区', 'zhangwei@gmail.com'),
('四季酒店', '40088880001', '深圳市南山区', 'siji@hotel.com'),
('阳光地产公司', '0755-88889999', '东莞市南城区', 'yg@yg.com');

-- 6.4 家具
INSERT INTO Furniture (FurnitureName, CategoryID, SupplierID, UnitPrice, Stock, Description) VALUES
('真皮三人沙发', 1, 1, 3800.00, 10, '进口头层牛皮，实木框架'),
('布艺双人沙发', 1, 2, 2200.00, 15, '棉麻面料，高回弹海绵'),
('实木双人床', 2, 3, 4500.00, 8, '北美白橡木，环保清漆'),
('现代简约大床', 2, 4, 3200.00, 12, 'E0级板材，简约设计'),
('大理石餐桌（1.5m）', 3, 2, 2800.00, 10, '天然大理石，实木桌腿'),
('实木书桌', 4, 3, 1800.00, 20, '进口胡桃木，手工打磨'),
('四门衣柜', 5, 1, 5200.00, 6, '实木框架，推拉门设计'),
('办公椅', 6, 4, 800.00, 25, '人体工学设计，升降旋转'),
('休闲躺椅', 6, 2, 1500.00, 10, '可调节角度，舒适靠垫'),
('茶几', 1, 3, 1200.00, 18, '钢化玻璃面，实木边框');

-- 6.5 入库记录
INSERT INTO WarehouseEntry (FurnitureID, EntryDate, Quantity, UnitPrice, Remarks) VALUES
(1, '2024-01-05 09:00:00', 20, 3200.00, '首次进货'),
(2, '2024-01-06 10:00:00', 25, 1800.00, '新款到货'),
(3, '2024-01-08 11:00:00', 15, 3800.00, '厂家促销'),
(4, '2024-01-10 14:00:00', 18, 2600.00, NULL),
(5, '2024-01-12 09:30:00', 15, 2200.00, '新年采购'),
(6, '2024-01-15 10:00:00', 30, 1400.00, NULL),
(7, '2024-01-18 13:00:00', 10, 4500.00, '高端系列'),
(8, '2024-02-01 09:00:00', 40, 600.00, '批量采购'),
(9, '2024-02-05 14:00:00', 20, 1200.00, NULL),
(10, '2024-02-10 10:00:00', 25, 900.00, '新款茶几');

-- 6.6 销售记录
INSERT INTO Sales (FurnitureID, CustomerID, SaleDate, Quantity, UnitPrice, Remarks) VALUES
(1, 1, '2024-01-20 15:00:00', 1, 3800.00, '家庭使用'),
(2, 2, '2024-01-22 16:00:00', 2, 2200.00, '新房装修'),
(5, 4, '2024-02-01 10:00:00', 5, 2800.00, '酒店采购'),
(3, 3, '2024-02-05 11:00:00', 1, 4500.00, '主卧配置'),
(6, 1, '2024-02-10 14:00:00', 2, 1800.00, '书房布置'),
(8, 5, '2024-02-15 09:00:00', 10, 800.00, '办公区批量'),
(10, 2, '2024-03-01 16:00:00', 2, 1200.00, '客厅配置'),
(9, 3, '2024-03-05 15:00:00', 1, 1500.00, '阳台休闲'),
(4, 4, '2024-03-10 10:00:00', 3, 3200.00, '酒店套房'),
(2, 5, '2024-03-15 14:00:00', 3, 2200.00, '员工宿舍');

-- 6.7 收款记录
INSERT INTO Receipt (SaleID, ReceiptDate, Amount, PaymentMethod, Remarks) VALUES
(1, '2024-01-20 15:30:00', 3800.00, '微信', '已付清'),
(2, '2024-01-22 16:20:00', 4400.00, '刷卡', '全款'),
(3, '2024-02-01 11:00:00', 14000.00, '转账', '对公转账'),
(4, '2024-02-05 11:30:00', 4500.00, '现金', '已付清'),
(5, '2024-02-10 14:30:00', 3600.00, '支付宝', NULL),
(6, '2024-02-15 09:30:00', 8000.00, '转账', '月结'),
(7, '2024-03-01 16:30:00', 2400.00, '微信', '已付清'),
(8, '2024-03-05 15:20:00', 1500.00, '现金', NULL),
(9, '2024-03-10 10:30:00', 9600.00, '转账', '部分付款'),
(10, '2024-03-15 14:30:00', 6600.00, '刷卡', '全款');

-- ==================== 7. 创建常用视图 ====================

-- 7.1 家具库存视图
CREATE OR REPLACE VIEW v_FurnitureStock AS
SELECT
    f.FurnitureID,
    f.FurnitureName,
    fc.CategoryName,
    s.SupplierName,
    f.UnitPrice,
    f.Stock,
    f.Description
FROM Furniture f
JOIN FurnitureCategory fc ON f.CategoryID = fc.CategoryID
JOIN Supplier s ON f.SupplierID = s.SupplierID;

-- 7.2 销售明细视图
CREATE OR REPLACE VIEW v_SalesDetail AS
SELECT
    sa.SaleID,
    f.FurnitureName,
    c.CustomerName,
    sa.SaleDate,
    sa.Quantity,
    sa.UnitPrice,
    sa.TotalAmount,
    sa.Remarks
FROM Sales sa
JOIN Furniture f ON sa.FurnitureID = f.FurnitureID
JOIN Customer c ON sa.CustomerID = c.CustomerID;

-- 7.3 收款明细视图
CREATE OR REPLACE VIEW v_ReceiptDetail AS
SELECT
    r.ReceiptID,
    f.FurnitureName,
    c.CustomerName,
    sa.SaleDate,
    r.ReceiptDate,
    r.Amount,
    r.PaymentMethod,
    r.Remarks
FROM Receipt r
JOIN Sales sa ON r.SaleID = sa.SaleID
JOIN Furniture f ON sa.FurnitureID = f.FurnitureID
JOIN Customer c ON sa.CustomerID = c.CustomerID;

-- ==================== 8. 创建统计查询样例 ====================

-- 调用存储过程示例（取消注释即可使用）：
-- CALL sp_InventoryStatistics('2024-01-01 00:00:00', '2024-03-31 23:59:59');

-- 查看当前库存
-- SELECT * FROM v_FurnitureStock ORDER BY Stock;

-- 查看低库存商品（库存 < 5）
-- SELECT * FROM v_FurnitureStock WHERE Stock < 5;
