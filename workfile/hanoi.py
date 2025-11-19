m=0 # 移动次数计数变量m

def Move(n,a,b,c):
    # a为当前所在的塔，b是辅助塔，c是目标塔。
    global m
    m+=1
    if n==1 :# 设置移动盘子的结束条件,如果A当前还有一个盘子那么就把他直接移动到C
        print(f"{a} -> {c}")
    else:# 否则开始递归
        Move(n-1,a,c,b)# 递归， 将A上编号为1至n-1的圆盘移到B, C做辅助塔；
        print(f"{a} -> {c}")# 直接将编号为n的圆盘从A移到C;
        Move(n-1,b,a,c)# 递归， 将B上编号为1至n-1的圆盘移到C, A做辅助塔

print("请输入盘子数:")
t=int(input())
print("流程如下：")
Move(t,'A','B','C')
print(f"一共转移了{m}次")
