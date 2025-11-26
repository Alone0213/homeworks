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
    node *pre=nullptr,*cur=k.rhead[r];
    while(cur&&cur->c<c){
        pre=cur;
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
    while(cur&&cur->r<r){
        pre=cur;
        cur=cur->down;
    }
    if(pre==nullptr){
        k.chead[c]=p;
    }else{
        if(!cur){
            pre->down=p;
            p->up=pre;
        }else if(cur->r==r){
            cur->val+=val;
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
    k.rhead=NULL;
    k.chead=NULL;
    int r,c,val;
    while(scanf("%d %d %d",&r,&c,&val)!=EOF){
        add_ele(r,c,val,k);
    }
}
void add(Crosslist &a1,Crosslist &a2){
    if(a1.cnum==a2.cnum&&a1.rnum==a2.rnum){
        for(int i=1; i<=a1.rnum; i++){
            node *pre=nullptr,*cur=a1.rhead[i];//I_th row
            while(cur){
                
            }
        }
    }
}
signed main(){
    CLr(k1);CLr(k2);
    add(k1,k2);
    return 0;
}
        // if(cur->r==r){
        //     cur->val+=val;
        //     delete p;
        //     p=nullptr;
        // }else if(cur->r<r){
        //     while(cur&&cur->r<r){
        //         pre=cur;
        //         cur=cur->down;
        //     }
        //     if(!cur){
        //         pre->down=p;
        //         p->up=pre;
        //     }else{
        //         pre->down=p;
        //         p->down=cur;
        //         cur->up=p;
        //         p->up=pre;
        //     }
        // }