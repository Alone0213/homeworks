#include <bits/stdc++.h>
using namespace std;

int n, m;//行与列
int in;
struct node
{
    int r, c;
    int val;
};
vector<node> t;
node s[2500];
int cnt;
int num[50];//原矩阵中每列非零元的个数
int pospercol[50];
int output[50][50];
signed main()
{
    printf("请输入行数和列数，两者中间空一格：\n");
    cin >> n >> m;
    printf("请输入矩阵：\n");
    for (int i = 1; i <= n; i++){
        for (int j = 1; j <= m; j++){
            cin >> in;
            if (in){
                t.push_back({i, j, in});
                num[j]++;
            }
        }
    }
    pospercol[1]=1;
    for(int i=2; i<=m; i++){
        pospercol[i]=pospercol[i-1]+num[i-1];
    }
    for(auto i:t){
        int pos=pospercol[i.c];
        s[pos].c=i.r;
        s[pos].r=i.c;
        s[pos].val=i.val;
        pospercol[i.c]++;
    }
    int l=t.size();
    for(int i=1; i<=l; i++){
        output[s[i].r][s[i].c]=s[i].val;
    }
    for(int i=1; i<=m; i++){
        for(int j=1; j<=n; j++){
            printf("%d ",output[i][j]);
        }
        printf("\n");
    }
    return 0;
}
//传参分为传值和传引用，基本数据类型为传值，引用数据类型为传引用，传值不修改，传引用会对该变量进行修改