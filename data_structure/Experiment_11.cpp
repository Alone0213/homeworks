#include<bits/stdc++.h>
using namespace std;
struct node{
    int ls,rs,val,num;
    bool operator<(const node &A) const{
        return val>A.val;
    }
}tr[10<<2];
int cnt;
priority_queue<node> q;
void print(int s){
    printf("number:%d value:%d\n",tr[s].num,tr[s].val);
    printf("node[%d]`s left son: ",tr[s].num);
    if(tr[s].ls) print(tr[s].ls);
    else printf("NULL\n");
    printf("node[%d]`s right son: ",tr[s].num);
    if(tr[s].rs) print(tr[s].rs);
    else printf("NULL\n");
    return;
}
signed main(){
    for(int i=1; i<=4; i++){
        tr[++cnt]=node{0,0,i,i};
        q.push(tr[i]);
    }
    while(q.size()>1){
        node m1=q.top();q.pop();
        node m2=q.top();q.pop();
        tr[++cnt]=node{m1.num,m2.num,m1.val+m2.val,cnt};
        q.push(tr[cnt]);
    }
    print(cnt);
    return 0;
}