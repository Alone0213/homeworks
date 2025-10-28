#include<bits/stdc++.h>
using namespace std;

class Monomial{
public:
    int a;
    int x;
    Monomial* ne;
    Monomial() : a(0), x(0), ne(nullptr) {}
    Monomial(int a_val, int x_val, Monomial* next) : a(a_val), x(x_val), ne(next) {}
    int new_ele(int a,int x){
        Monomial* p=ne;
        Monomial* pre=nullptr;
        while(p){
            if(p->x==x){
                p->a+=a;
                return 0;
            }
            pre=p;
            p=p->ne;
        }
        Monomial* s=new Monomial(a,x,nullptr);
        s->a=a;
        s->x=x;
        if(!pre){
            ne=s;
        }else{
            pre->ne=s;
        }
        return 1;
    }
    void print(){
        Monomial* p=ne;
        while(p!=nullptr){
            if(!p->ne) printf("%dx^%d",p->a,p->x);
            else printf("%dx^%d+",p->a,p->x);
            p=p->ne;
        }
        puts("");
        return;
    }
};

int n,m;
int a_in,x_in;
Monomial p1,p2;
Monomial add(Monomial a1,Monomial a2){
    Monomial* p=a2.ne;
    // Monomial* pre=nullptr;
    while(p){
        a1.new_ele(p->a,p->x);
        p=p->ne;
    }
    return a1;
}
signed main(){
    printf("请输入第一个多项式的项数：\n");
    cin >> n;
    printf("请在下方输入每一项的系数和次数（每行仅两个整数）：\n");
    for(int i=1; i<=n; i++){
        cin >> a_in >> x_in;
        p1.new_ele(a_in,x_in);
    }
    printf("第一个多项式：");
    p1.print();
    printf("请输入第二个多项式的项数：\n");
    cin >> m;
    printf("请在下方输入每一项的系数和次数（每行仅两个整数）：\n");
    for(int i=1; i<=m; i++){
        cin >> a_in >> x_in;
        p2.new_ele(a_in,x_in);
    }
    printf("第二个多项式：");
    p2.print();
    add(p1,p2);
    printf("两多项式加和：");
    p1.print();
    return 0;
}