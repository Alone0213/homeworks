# 大学数据库实验操作流程 (DBeaver on Windows)

## 一、实验环境准备

1. 确保已安装并启动 DBeaver
2. 连接到 MySQL/MariaDB 数据库服务器（假设为本地实例）
3. 准备执行 SQL 脚本

## 二、数据库与表结构创建脚本

### 步骤1：创建数据库

```sql
-- 如果已存在则删除（可选）
-- DROP DATABASE IF EXISTS university;

-- 创建数据库
CREATE DATABASE university
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE university;
```

### 步骤2：创建11张表（基于教材图2-8和2-9的经典模式）

```sql
-- 1. 系部表
CREATE TABLE department (
    dept_name VARCHAR(20) PRIMARY KEY,
    building VARCHAR(15),
    budget DECIMAL(12,2)
);

-- 2. 教室表
CREATE TABLE classroom (
    building VARCHAR(15),
    room_number VARCHAR(7),
    capacity INT,
    PRIMARY KEY (building, room_number)
);

-- 3. 课程表
CREATE TABLE course (
    course_id VARCHAR(8) PRIMARY KEY,
    title VARCHAR(50),
    dept_name VARCHAR(20),
    credits DECIMAL(2,0),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE SET NULL
);

-- 4. 教师表
CREATE TABLE instructor (
    ID VARCHAR(5) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20),
    salary DECIMAL(8,2),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE SET NULL
);

-- 5. 时间槽表
CREATE TABLE time_slot (
    time_slot_id VARCHAR(4),
    day VARCHAR(1),
    start_time TIME,
    end_time TIME,
    PRIMARY KEY (time_slot_id, day, start_time)
);

-- 6. 节次表
CREATE TABLE section (
    course_id VARCHAR(8),
    sec_id VARCHAR(8),
    semester VARCHAR(6),
    year DECIMAL(4,0),
    building VARCHAR(15),
    room_number VARCHAR(7),
    time_slot_id VARCHAR(4),
    PRIMARY KEY (course_id, sec_id, semester, year),
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (building, room_number) REFERENCES classroom(building, room_number) ON DELETE SET NULL
);

-- 7. 授课表
CREATE TABLE teaches (
    ID VARCHAR(5),
    course_id VARCHAR(8),
    sec_id VARCHAR(8),
    semester VARCHAR(6),
    year DECIMAL(4,0),
    PRIMARY KEY (ID, course_id, sec_id, semester, year),
    FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year) ON DELETE CASCADE,
    FOREIGN KEY (ID) REFERENCES instructor(ID) ON DELETE CASCADE
);

-- 8. 学生表
CREATE TABLE student (
    ID VARCHAR(5) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20),
    tot_cred DECIMAL(3,0) DEFAULT 0,
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE SET NULL
);

-- 9. 选课表
CREATE TABLE takes (
    ID VARCHAR(5),
    course_id VARCHAR(8),
    sec_id VARCHAR(8),
    semester VARCHAR(6),
    year DECIMAL(4,0),
    grade VARCHAR(2),
    PRIMARY KEY (ID, course_id, sec_id, semester, year),
    FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year) ON DELETE CASCADE,
    FOREIGN KEY (ID) REFERENCES student(ID) ON DELETE CASCADE
);

-- 10. 导师表
CREATE TABLE advisor (
    s_ID VARCHAR(5),
    i_ID VARCHAR(5),
    PRIMARY KEY (s_ID),
    FOREIGN KEY (i_ID) REFERENCES instructor(ID) ON DELETE SET NULL,
    FOREIGN KEY (s_ID) REFERENCES student(ID) ON DELETE CASCADE
);

-- 11. 先修课程表
CREATE TABLE prereq (
    course_id VARCHAR(8),
    prereq_id VARCHAR(8),
    PRIMARY KEY (course_id, prereq_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (prereq_id) REFERENCES course(course_id)
);
```

## 三、查询脚本（步骤3-8）

### 步骤3：查询 instructor 和 student 表中的用户ID和不重复名字

```sql
-- 3.1 查询教师表中的ID和名字
SELECT ID, name
FROM instructor
ORDER BY name;

-- 3.2 查询学生表中的ID和名字
SELECT ID, name
FROM student
ORDER BY name;

-- 3.3 查询两个表中所有不重复的名字（假设要合并）
SELECT DISTINCT name 
FROM (
    SELECT name FROM instructor
    UNION
    SELECT name FROM student
) AS all_names
ORDER BY name;
```

### 步骤4：查询来自 "Comp. Sci." 系部的所有学生信息

```sql
SELECT *
FROM student
WHERE dept_name = 'Comp. Sci.'
ORDER BY ID;
```

### 步骤5：查询总学分修够80分及其以上的学生的ID和姓名

```sql
SELECT ID, name, tot_cred
FROM student
WHERE tot_cred >= 80
ORDER BY tot_cred DESC;
```

### 步骤6：按系部归类查询各个系部的教师的平均年收入

```sql
SELECT 
    dept_name,
    COUNT(*) as teacher_count,
    ROUND(AVG(salary), 2) as avg_salary
FROM instructor
WHERE dept_name IS NOT NULL
GROUP BY dept_name
ORDER BY avg_salary DESC;
```

### 步骤7：查询年收入在90000到100000之间的教师名字和工资

```sql
-- 注意：题目是90000到10000，但可能是笔误，假设是90000到100000
SELECT 
    name,
    salary,
    dept_name
FROM instructor
WHERE salary BETWEEN 90000 AND 100000
ORDER BY salary DESC;
```

### 步骤8：查询坐落在 Watson Building 的系部信息

```sql
SELECT 
    dept_name,
    building,
    budget
FROM department
WHERE building = 'Watson'
ORDER BY dept_name;
```

## 四、操作流程说明

### 在 DBeaver 中执行的步骤：

1. **打开 DBeaver**
   
   - 启动 DBeaver 应用程序
   - 确保已建立数据库连接（如 MySQL 连接）

2. **创建数据库和表结构**
   
   - 在 SQL 编辑器中，依次执行步骤1和步骤2的脚本
   - 可以使用 "执行SQL脚本" 按钮（或按 F9）执行每条语句
   - 验证所有表已成功创建

3. **插入测试数据（可选）**
   
   - 如果需要测试查询，可以先插入一些示例数据
   - 示例数据插入脚本（简版）：
     
     ```sql
     -- 插入系部数据
     INSERT INTO department VALUES 
     ('Comp. Sci.', 'Watson', 100000),
     ('Biology', 'Watson', 90000),
     ('Elec. Eng.', 'Taylor', 85000),
     ('Music', 'Packard', 80000),
     ('Finance', 'Painter', 120000),
     ('History', 'Painter', 50000),
     ('Physics', 'Watson', 70000);
     ```
   
   -- 插入教师数据
   INSERT INTO instructor VALUES 
   ('10101', 'Srinivasan', 'Comp. Sci.', 95000),
   ('12121', 'Wu', 'Finance', 90000),
   ('15151', 'Mozart', 'Music', 40000),
   ('22222', 'Einstein', 'Physics', 95000),
   ('32343', 'El Said', 'History', 60000),
   ('33456', 'Gold', 'Physics', 87000),
   ('45565', 'Katz', 'Comp. Sci.', 75000),
   ('58583', 'Califieri', 'History', 62000),
   ('76543', 'Singh', 'Finance', 80000),
   ('76766', 'Crick', 'Biology', 72000),
   ('83821', 'Brandt', 'Comp. Sci.', 92000),
   ('98345', 'Kim', 'Elec. Eng.', 80000);
   
   -- 插入学生数据
   INSERT INTO student VALUES 
   ('00128', 'Zhang', 'Comp. Sci.', 102),
   ('12345', 'Shankar', 'Comp. Sci.', 32),
   ('19991', 'Brandt', 'History', 80),
   ('23121', 'Chavez', 'Finance', 110),
   ('44553', 'Peltier', 'Physics', 56),
   ('45678', 'Levy', 'Physics', 46),
   ('54321', 'Williams', 'Comp. Sci.', 54),
   ('55739', 'Sanchez', 'Music', 38),
   ('70557', 'Snow', 'Physics', 0),
   ('76543', 'Brown', 'Comp. Sci.', 58),
   ('76653', 'Aoi', 'Elec. Eng.', 60),
   ('98765', 'Bourikas', 'Elec. Eng.', 98),
   ('98988', 'Tanaka', 'Biology', 120);
   
   ```
   
   ```

4. **执行查询脚本**
   
   - 在 SQL 编辑器中，依次执行步骤3-8的查询脚本
   - 观察每个查询的结果
   - 可以保存查询结果为CSV文件以便记录

5. **验证结果**
   
   - 检查每个查询是否返回预期结果
   - 如果结果为空，可能需要插入更多测试数据

## 五、注意事项

1. **数据一致性**：插入测试数据时，注意外键约束，先插入父表数据再插入子表数据
2. **SQL语法**：如果使用其他数据库系统（如PostgreSQL），可能需要调整语法
3. **错误处理**：如果执行出错，检查表名、列名是否正确，以及外键约束是否满足
4. **性能优化**：对于大型数据集，可以为经常查询的字段添加索引

## 六、扩展建议

1. **添加索引**以提高查询性能：
   
   ```sql
   -- 为常用查询字段创建索引
   CREATE INDEX idx_student_dept ON student(dept_name);
   CREATE INDEX idx_instructor_salary ON instructor(salary);
   CREATE INDEX idx_department_building ON department(building);
   ```

2. **创建视图**简化常用查询：
   
   ```sql
   -- 创建高学分学生视图
   CREATE VIEW high_credit_students AS
   SELECT ID, name, dept_name, tot_cred
   FROM student
   WHERE tot_cred >= 80;
   ```

3. **添加约束**确保数据完整性：
   
   ```sql
   -- 添加检查约束（如MySQL 8.0+支持）
   ALTER TABLE student
   ADD CONSTRAINT chk_tot_cred CHECK (tot_cred >= 0);
   ```

ALTER TABLE instructor
ADD CONSTRAINT chk_salary CHECK (salary > 0);

```

## 七、实验报告内容建议

完成实验后，建议记录以下内容：

1. 各查询执行的结果
2. 遇到的问题及解决方法
3. 对数据库设计的理解
4. 查询优化建议

这个操作流程涵盖了从创建数据库到执行查询的完整过程，适合在DBeaver环境中进行大学数据库实验。
