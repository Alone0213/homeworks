#include<bits/stdc++.h>
using namespace std;
const int N=1e3+23;
int a[N],b[N];
void merge(int x1[],int x2[]){
    bool s=0;
    for(int i=1; i<=x2[0]; i++){
        s=0;
        for(int j=1; j<=x1[0]; j++){
            if(x1[j]==x2[i]){
                s=1; break;
            }
        }
        if(s) continue;
        else x1[++x1[0]]=x2[i];
    }
}
signed main(){
    cin >> a[0]; for(int i=1; i<=a[0]; i++) cin >> a[i];
    cin >> b[0]; for(int i=1; i<=b[0]; i++) cin >> b[i];
    merge(a,b);
    for(int i=1; i<=a[0]; i++){
        printf("%d ",a[i]);
    }
    return 0;
}