#include<cstdio>
using namespace std;
int m = 0;//移动次数计数变量m
void Move(int n, char A, char B, char C)
{//A为当前所在的塔，B是辅助塔，C是目标塔。
    m++;
    if (n == 1){// 设置移动盘子的结束条件,如果A当前还有一个盘子那么就把他直接移动到C
        printf("%c -> %c\n", A, C);
    }else{// 否则开始递归
        Move(n - 1, A, C, B); // 递归， 将A上编号为1至n-1的圆盘移到B, C做辅助塔；
        printf("%c -> %c\n", A, C);// 直接将编号为n的圆盘从A移到C;
        Move(n - 1, B, A, C); // 递归， 将B上编号为1至n-1的圆盘移到C, A做辅助塔
    }
}
int n;
int main(){
    printf("请输入盘子数：");
    scanf("%d", &n);
    Move(n, 'A', 'B', 'C');
    printf("移动次数：%d次", m);
    return 0;
}