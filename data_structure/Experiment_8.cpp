#include<iostream>
using namespace std;

struct node{
    int val;
    int r,c;
    node *right,*down;
    node *left,*up;
};
struct Crosslist{
    node **rhead,**chead;
    int rnum,cnum,trnum;//row,column,true
};
void add_ele(int r,int c,int val,Crosslist &k){
    node *p=new node;
    p->r=r;p->c=c;p->val=val;
    p->right=p->down=p->up=p->left=nullptr;
    node *pre=nullptr;
    node *cur=k.rhead[r];
    while(cur){
        pre=cur;
        if(cur->c>=c) break;
        cur=cur->right;
    }
    if(pre==nullptr){
        k.rhead[r]=p;
    }else{
        if(!cur){
            pre->right=p;
            p->left=pre;
        }else if(cur->c==c){
            cur->val+=val;
        }else{
            pre->right=p;
            p->right=cur;
            cur->left=p;
            p->left=pre;
        }
    }
    pre=nullptr;cur=k.chead[c];
    while(cur){
        pre=cur;
        if(cur->r>=r) break;
        cur=cur->down;
    }
    if(pre==nullptr){
        k.chead[c]=p;
    }else{
        if(!cur){
            pre->down=p;
            p->up=pre;
        }else if(cur->r==r){
        }else{
            pre->down=p;
            p->down=cur;
            cur->up=p;
            p->up=pre;
        }
    }
}
Crosslist k1,k2;
void CLr(Crosslist &k){
    cin >> k.rnum >> k.cnum >> k.trnum;
    k.rhead= new node *[k.rnum];
    k.chead= new node *[k.cnum];
    for(int i=1; i<=k.rnum; i++) k.rhead[i]=nullptr;
    for(int i=1; i<=k.cnum; i++) k.chead[i]=nullptr;
    int r,c,val;
    for(int i=1; i<=k.trnum; i++){
        cin >> r >> c >> val;
        add_ele(r,c,val,k);
    }
}
void add(Crosslist &a1,Crosslist &a2){
    if(a1.cnum==a2.cnum&&a1.rnum==a2.rnum){
        for(int i=1; i<=a1.rnum; i++){
            node *cur=a1.rhead[i];
            while(cur){
                add_ele(cur->r,cur->c,cur->val,a2);
                cur=cur->right;
            }
        }
    }
}
void CLprint(Crosslist &a){
    for(int i=1; i<=a.rnum; i++){
        node *cur=a.rhead[i];//I_th row
        while(cur){
            printf("%d %d %d\n",cur->r,cur->c,cur->val);
            cur=cur->right;
        }
    }
}
signed main(){
    freopen("inp.txt","r",stdin);
    CLr(k1);
    CLr(k2);
    add(k1,k2);
    CLprint(k2);
    return 0;
}