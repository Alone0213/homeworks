public class CountdownThread extends Thread {
    public void run1() {
        try {
            for (int i = 10; i > 0; i--) {
                System.out.println(i);
                Thread.sleep(500);
            }
        } catch (InterruptedException e) {
            System.out.println("Countdown interrupted");
        }
    }
}
