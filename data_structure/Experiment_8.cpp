#include<iostream>
using namespace std;

struct node{
    int val;
    int r,c;
    struct node *right,*down;
};
struct Crosslist{
    node *rhead,*chead;
    int rnum,cnum,trnum;//row,column,true
};

Crosslist k1,k2;
void CLr(Crosslist &k){
    cin >> k.rnum >> k.cnum >> k.trnum;
    k.rhead=NULL;
    k.chead=NULL;
    int a,b,c;
    while(scanf("%d %d %d",&a,&b,&c)!=EOF){
        
    }
}
signed main(){
    CLr(k1);CLr(k2);
    return 0;
}