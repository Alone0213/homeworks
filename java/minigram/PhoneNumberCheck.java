import java.util.Scanner;

public class PhoneNumberCheck{
    public static void main(String Args[]){
        String a;
        try (Scanner input = new Scanner(System.in)) {
            a=input.next();
            
            boolean len=false;
            
            int l=a.length();
            if(l==11) len=true;
            
            boolean n=true;
            boolean ini=false;
            boolean sec=true;
            for(int i=0; i<l; i++){
                char c=a.charAt(i);
                if(i==0) if(c=='1') ini=true;
                if(i==1) if(c=='0'||c=='1'||c=='2') sec=false;
                if(c<'0'||c>'9') n=false;
            }
            
            if(len&&n&&ini&&sec){
                System.out.println("该手机号合法\n");
            }else{
                System.out.println("该手机号不合法\n");
            }
        }
    }
}