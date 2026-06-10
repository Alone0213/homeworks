#include<bits/stdc++.h>
using namespace std;

typedef struct Treenode{
    int val;
    Treenode *l;
    Treenode *r;
    int num;
    Treenode(){val=0;this->l=nullptr;this->r=nullptr;num=0;}
    Treenode(int _val){val=_val;this->l=nullptr;this->r=nullptr;num=0;}
}BST;
int tMin(Treenode *T){
    if(T==nullptr){
        return -1;
    }
    while(T->l!=nullptr){
        T=T->l;
    }
    return T->val;
}
int tMax(Treenode *T){
    if(T==nullptr){
        return -1;
    }
    while(T->r!=nullptr){
        T=T->r;
    }
    return T->val;
}

void inSert(int v,Treenode * &rt){
    if(!rt){
        rt=new Treenode(v);
        return;
    }
    if(v==rt->val){
        rt->num++;
        return;
    }else if(v>rt->val) inSert(v,rt->r);
    else inSert(v,rt->l);
}
int find(int v,Treenode *rt){
    if(!rt){
        return -1;
    }
    if(v==rt->val){
        return 1;
    }else if(v>rt->val) return find(v,rt->r);
    else return find(v,rt->l);
}
signed main(){
    BST *t=nullptr;
    int a[11]={0,5,4,6,3,7,2,8,1,9,0};
    for(int i=1; i<=10; i++){
        inSert(a[i],t);
    }
    printf("查一下有没有11:\n");
    printf("%d\n",find(11,t));
    printf("最大最小值：\n");
    printf("%d %d\n",tMax(t),tMin(t));
    inSert(11,t);
    printf("查一下有没有11:\n");
    printf("%d\n",find(11,t));
    return 0;
}