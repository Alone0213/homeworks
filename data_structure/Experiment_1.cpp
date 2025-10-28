#include<bits/stdc++.h>
using namespace std;

template <typename T>
class trigroup{
private:
    T e1,e2,e3;
public:
    T init(T a1,T a2,T a3){//?????
        e1=a1;e2=a2;e3=a3;
        return true;
    }
    T Max(){//??????
        T maxx=max(e1,e2);
        return max(maxx,e3);
    }
    T Min(){//????§³?
        T minn=min(e1,e2);
        return min(minn,e3);
    }
    T modify(int i,T val){//????i???
        switch (i){
            case 1:
            e1=val;
            break;

            case 2:
            e2=val;
            break;

            case 3:
            e3=val;
            break;
        }
        return true;
    }
    bool isrising(){//?§Ø?????????
        return e3>=e2&&e2>=e1;
    }
    bool isdropping(){//?§Ø?????????
        return e2<=e1&&e3<=e2;
    }
    void print(){
        printf("%d %d %d\n",e1,e2,e3);
    }
};
int c1,c2,c3;

signed main(){
    trigroup<int> a;
    printf("?????????????????????????\n");
    cin >> c1 >> c2 >> c3;
    a.init(c1,c2,c3);
    printf("????????§³???");
    cout << a.Max() << " " << a.Min() << endl;
    printf("???????????????????");
    int n,m;
    cin >> n >> m;
    a.modify(n,m);
    printf("????????§³???");
    cout << a.Max() << " " << a.Min() << endl;
    puts("");
    printf("??????????:");
    a.print();
    printf("????????\n");
    cout << a.isdropping() << endl;
    printf("????????\n");
    cout << a.isrising() << endl;
    return 0;
}
