public class ScoreException extends Exception {
    public ScoreException() {
        super("成绩不合法！成绩必须在0-100分之间。");
    }
    public ScoreException(String message) {
        super(message);
    }
}
