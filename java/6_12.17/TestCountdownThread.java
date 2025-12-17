public class TestCountdownThread {
    public static void main(String args[]){
        CountdownThread r1=new CountdownThread();
        r1.run1();
        CountdownThread r2=new CountdownThread();
        r2.run1();
    }
}
