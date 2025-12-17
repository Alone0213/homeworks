public class PrintCharTask implements Runnable{
    private final char _chr;
    private final String _str;
    public PrintCharTask(char chr,String str) {
        this._chr=chr;
        this._str=str;
    }
    
    public char get_chr() {
        return _chr;
    }

    public String get_str() {
        return _str;
    }

    @Override
    public void run(){
        for(int i=1; i<=10; i++){
            System.out.printf("%s:%c\n",_str,_chr);
            try {
                Thread.sleep(400);
            } catch (InterruptedException e) {
                System.out.println("error\n");
            }
        }
    }
}
