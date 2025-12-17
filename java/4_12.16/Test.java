public class Test {
    public static void main(String[] args) {
        System.out.println("========= 学生成绩设置测试 =========\n");
        
        try {
            System.out.println("测试1：设置合法成绩");
            Student stu1 = new Student("2023001");
            stu1.setScore(85);
            stu1.displayInfo();
            System.out.println();
        } catch (ScoreException e) {
            System.out.println("异常信息：" + e.getMessage());
        }
        
        try {
            System.out.println("测试2：设置非法成绩（105分）");
            Student stu2 = new Student("2023002");
            stu2.setScore(105);
            stu2.displayInfo();
            System.out.println();
        } catch (ScoreException e) {
            System.out.println("异常信息：" + e.getMessage() + "\n");
        }
        
        try {
            System.out.println("测试3：设置非法成绩（-10分）");
            Student stu3 = new Student("2023003");
            stu3.setScore(-10);
            stu3.displayInfo();
            System.out.println();
        } catch (ScoreException e) {
            System.out.println("异常信息：" + e.getMessage() + "\n");
        }
        
        try {
            System.out.println("测试4：使用构造方法设置非法成绩（150分）");
            Student stu4 = new Student("2023004", 150);
            stu4.displayInfo();
            System.out.println();
        } catch (ScoreException e) {
            System.out.println("异常信息：" + e.getMessage() + "\n");
        }
        
        try {
            System.out.println("测试5：边界值测试");
            Student stu5 = new Student("2023005", 0);
            stu5.displayInfo();
            
            Student stu6 = new Student("2023006", 100);
            stu6.displayInfo();
            System.out.println();
        } catch (ScoreException e) {
            System.out.println("异常信息：" + e.getMessage() + "\n");
        }
    
        System.out.println("测试6：批量测试多个学生");
        String[] studentIDs = {"2023007", "2023008", "2023009", "2023010"};
        int[] scores = {95, 102, 88, -5};
        
        for (int i = 0; i < studentIDs.length; i++) {
            try {
                Student stu = new Student(studentIDs[i]);
                stu.setScore(scores[i]);
                System.out.println("学生 " + studentIDs[i] + " 成绩设置成功：" + scores[i]);
            } catch (ScoreException e) {
                System.out.println("学生 " + studentIDs[i] + " 成绩设置失败：" + e.getMessage());
            }
        }
        
        System.out.println("\n========= 测试完成 =========");
    }
}
