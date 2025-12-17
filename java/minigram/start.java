import java.util.Scanner;


public class start {
    public static void main(String[] args) {
        // String txt=input.next();
        try ( // System.out.println("Hello World\n");
                Scanner input = new Scanner(System.in)) {
            // String txt=input.next();
            int n;
            
            System.out.println("请输入数组元素个数：");
            n=input.nextInt();
            final int N=10000007+123;
            int[] array=new int[N];
            for(int i=1; i<=n; i++){
                array[i]=input.nextInt();
            }
            for(int i=1; i<=n; i++){
                System.out.println(array[i]);
            }
        }
    }
}
