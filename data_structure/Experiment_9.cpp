#include<bits/stdc++.h>
using namespace std;
struct node{
    int val;
    bool no_empty;
    bool visited;
    int ls,rs;
};
node tr[1<<10];
stack<int> k;
void solve(){
    printf("中序遍历结果：");
    int top;
    k.push(1);
    while(!k.empty()){
        top=k.top();
        if(tr[tr[top].ls].no_empty){
            if(!tr[tr[top].ls].visited){
                k.push(tr[top].ls);
                continue;
            }
        }
        if(!tr[top].visited){
            printf("%d ",top);
            tr[top].visited=1;
        }
        if(tr[tr[top].rs].no_empty){
            if(!tr[tr[top].rs].visited){
                k.push(tr[top].rs);
                continue;
            }
        }
        k.pop();
    }
}
signed main(){
    for(int i=1; i<=10; i++)
        tr[i]=node{i,true,false,i<<1,i<<1|1};
    while(!k.empty()) k.pop();
    solve();
    return 0;
}