#include<bits/stdc++.h>
using namespace std;

int a[11]={0,5,1,2,8,0,4,6,9,3,7};
signed main(){
    int l=1,r=10;
    bool s=1;
    while(l<r&&s){
        s=0;
        for(int i=l; i<r; i++)
            if(a[i]>a[i+1]) swap(a[i],a[i+1]),s=1;
        r--;
        for(int i=r; i>l; i--)
            if(a[i]<a[i-1]) swap(a[i],a[i-1]),s=1;
        l++;
    }
    for(int i=1; i<=10; i++) cout << a[i] << " ";
    return 0;
}