public class Student {
    public String stuID;
    private int score;
    public Student() {}
    public Student(String stuID) {
        this.stuID = stuID;
    }
    public final void setScore(int score) throws ScoreException {
        if (score < 0 || score > 100) {
            throw new ScoreException("成绩" + score + "不合法！成绩必须在0-100分之间。");
        }
        this.score = score;
    }
    public Student(String stuID, int score) throws ScoreException {
        this.stuID = stuID;
        setScore(score);
    }
    public int getScore() {
        return score;
    }
    public void displayInfo() {
        System.out.println("学号：" + stuID + "，成绩：" + score);
    }
}