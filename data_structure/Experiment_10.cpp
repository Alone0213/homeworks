#include<bits/stdc++.h>
using namespace std;
struct node{
    int val;
    bool no_empty;
    bool visited;
    int ls,rs;
};
node tr[1<<10];
queue<int> q;
void solve(int rt){
    q.push(rt);
    tr[rt].visited=true;
    while(!q.empty()){
        int h=q.front();
        q.pop();
        if(tr[tr[h].ls].no_empty) q.push(tr[h].ls);
        if(tr[tr[h].rs].no_empty) q.push(tr[h].rs);
        printf("%d ",h);
        tr[h].visited=1;
    }
}
signed main(){
    for(int i=1; i<=10; i++)
        tr[i]=node{i,true,false,i<<1,i<<1|1};
    solve(1);
    return 0;
}