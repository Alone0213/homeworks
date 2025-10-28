#include<bits/stdc++.h>
using namespace std;

// template<typename T>
class Queue{
public:
    int num;
    Queue* ne;
    Queue() :num(0),ne(nullptr){}
    Queue(int _num) :num(_num),ne(nullptr){}
    void add(int x){
        Queue* p=ne;
        Queue* pre=nullptr;
        if(p)
        do{
            pre=p;
            p=p->ne;
        }while(pre->ne!=ne);
        Queue* s=new Queue(x);
        if(!pre){
            ne=s;
        }else{
            pre->ne=s;
        }
        s->ne=ne;
    }
};
Queue Joseph;
void solve(){
    Queue* p=Joseph.ne;
    Queue* pre=nullptr;
    int i=1;
    while(p->ne!=p){
        if(i==7){
            printf("%d ",p->num);
            pre->ne=p->ne;
            p=pre->ne;
            i=1;
        }
        pre=p;
        p=p->ne;
        i++;
    }
    // printf("%d\n",Joseph.ne->num);
}
signed main(){
    for(int i=1; i<=10; i++){
        Joseph.add(i);
    }
    printf("The order of out:");
    solve();
    return 0;
}