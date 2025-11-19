import java.util.Random;
import java.util.Scanner;

public class b {
    public static void main(String[] args) {
        try (Scanner in = new Scanner(System.in)) {
            int opt=0;
            Random ans= new Random();
            int ansy=ans.nextInt(10)+1;
            int t=0;
            System.out.println("范围1~10");
            while(opt!=-1){
                opt=in.nextInt();
                while(opt==-1) break;
                if(opt>ansy){
                    System.out.println("猜大了");
                }else if(opt<ansy){
                    System.out.println("猜小了");
                }else if(opt==ansy){
                    System.out.println("对了");
                    t++;
                    System.out.println("继续or输入-1退出");
                }
            }
            System.out.printf("你一共猜对了%d个数\n",t);
        }
    }
}
