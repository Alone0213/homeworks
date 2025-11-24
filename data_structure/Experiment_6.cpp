#include <bits/stdc++.h>
using namespace std;

int n, m;
int in;
struct node
{
    int r, c;
    int val;
};
vector<node> t;
int cnt;
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
            }
        }
    }

    return 0;
}