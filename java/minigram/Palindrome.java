import java.util.Scanner;

public class Palindrome {
    public static void main(String[] args) {
        String a;
        try (Scanner input = new Scanner(System.in)) {
            a=input.next();
            int len=a.length();
            for(int i=len-1; i>=0; i--){
                char c=a.charAt(i);
                System.out.printf("%c",c);
            }
        }
    }
}
