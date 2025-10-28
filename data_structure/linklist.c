#include<stdio.h>
const int N=2e5+213;

typedef struct node{
    int data;//valve
    struct node *ne;//pointer
}listnode;
int cnt;

listnode *now;

listnode *create_new_node(int x){
    listnode *newnode=(int*)malloc(sizeof(int));
    newnode->data=x;
    newnode->ne=NULL;
    return newnode;
}

void pushback(listnode **v,int x){
    listnode *newmb=create_new_node(x);;
    if(*v==NULL){
        *v=newmb;
    }else{
        listnode *tail=*v;
        while(tail->ne!=NULL){
            tail=tail->ne;
        }
        tail->ne=newmb;
    }
}

void print(struct node L){
    struct node *nw;
    nw=&L;
    while(nw!=NULL){
        printf("%d ",nw->data);
        nw=nw->ne;
    }
}
listnode Head;
signed main(){
    
    for(int i=1; i<=10; i++){
        add(i);
    }
    return 0;
}


