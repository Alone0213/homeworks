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
vector<node> s;
int cnt;
vector<int> num;//原矩阵中每列非零元的个数
vector<int> pospercol;
signed main()
{
    printf("请输入行数和列数，两者中间空一格：\n");
    cin >> n >> m;
    printf("请输入矩阵：\n");
    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= m; j++)
        {
            cin >> in;
            if (in)
            {
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
    for(auto i:t){
        printf("%d %d %d\n",i.r,i.c,i.val);
    }
    puts("");
    for(auto i:s){
        printf("%d %d %d\n",i.r,i.c,i.val);
    }
    return 0;
}